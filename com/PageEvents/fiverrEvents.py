from webpageEvents import WebpageEvents
import config
from Utilities.constants import IDMODE
from Utilities.myLogger import logger
import sys
import time
import os
from inputContent import Order
from inputContent import orderItem
from inputContent import orderAttachment


class FiverrEvents(WebpageEvents):
    def __init__(self):
        super(FiverrEvents, self).__init__()

    def destroy(self):
        super(FiverrEvents, self).destroy()

    def login_to_fiverr(self):
        self.navigate(config.baseURL)
        self.enterText(IDMODE.ID, "user_session_login", config.FivUsername.strip())
        self.enterText(IDMODE.ID, "user_session_password", config.FivPassword.strip())
        self.findElement(IDMODE.ID, "user_session_password").submit()
        self.assertLoginSuccessful()

    def assertLoginSuccessful(self):
        try:
            self.waitUntilElementIsPresent(IDMODE.CLASS, "user-menu")
        except:
            raise Exception('Login Unsuccessful' + str(sys.exc_info()))

    def open_sales_page(self):
        self.clickPartialLink("SALES")

    def scrape_order_summary(self):
        ordersTable = self.findElement(IDMODE.CLASS, "db-main-table")
        ordersTable = ordersTable.find_element_by_tag_name("tbody")
        orderRows = ordersTable.find_elements_by_tag_name("tr")
        if "No priority orders to show" in orderRows[0].text:
            return 101      # No Orders
        newOrdersFound = False
        # if not len(orderRows) > 0:
        #     return 101      # No Orders
        for orderRow in orderRows:
            try:
                orderURL = orderRow.find_elements_by_tag_name("td")[3]
            except IndexError:
                continue

            orderURL = orderURL.find_element_by_tag_name("a").get_attribute("href")
            orderNum = orderURL[orderURL.rindex("/")+1:]
            if orderNum in config.ScrapedOrders:
                continue

            currOrder = Order()
            currOrder.orderURL = orderURL
            currOrder.orderNum = orderNum
            currOrder.buyerName = orderRow.find_elements_by_tag_name("td")[2].text.strip()
            currOrder.dueDate = orderRow.find_elements_by_tag_name("td")[4].text.strip()
            currOrder.orderAmount = orderRow.find_elements_by_tag_name("td")[5].text.strip()

            config.Orders.append(currOrder)
            newOrdersFound = True

        if not newOrdersFound:
            return 102      # No New Orders
        else:
            return 1

    def scrape_order_details(self):
        for currOrder in config.Orders:
            self.navigate(currOrder.orderURL)

            orderDetailBox = self.findElement(IDMODE.CLASS, "order-gig-detail")
            orderDetailBox = orderDetailBox.find_element_by_tag_name("tbody")

            items = orderDetailBox.find_elements_by_tag_name("tr")

            for item in items:
                try:
                    if item.get_attribute("class") == "total":
                        continue
                except:
                    logger.exception(sys.exc_info())
                currItem = orderItem()
                currItem.itemName = item.find_elements_by_tag_name("td")[0].text.strip()
                currItem.itemQuantity = item.find_elements_by_tag_name("td")[1].text.strip()
                currItem.itemDuration = item.find_elements_by_tag_name("td")[2].text.strip()
                currItem.itemAmount = item.find_elements_by_tag_name("td")[3].text.strip()

                if currOrder.items is None:
                    currOrder.items = []
                currOrder.items.append(currItem)

            order_messages = self.findElement(IDMODE.CLASS, "order-messages")
            articles = order_messages.find_elements_by_tag_name("article")
            for article in articles:
                try:
                    article_submitter = article.find_element_by_tag_name("h4").text.strip()
                    if article_submitter == currOrder.buyerName:
                        is_article_attachment = False
                        small_sections = article.find_elements_by_tag_name("small")
                        if len(small_sections) > 0:
                            for curr_section in small_sections:
                                if curr_section.text.strip() == "ATTACHMENTS":
                                    is_article_attachment = True
                                    attachmentSection = article.find_element_by_tag_name("aside")
                                    attachmentSection = attachmentSection.find_element_by_tag_name("ul")
                                    attachments = attachmentSection.find_elements_by_tag_name("li")
                                    for attachment in attachments:
                                        currAttachment = orderAttachment()
                                        attachment = attachment.find_element_by_tag_name("a")
                                        currAttachment.attachmentURL = attachment.get_attribute("href")
                                        currAttachment.attachmentTitle = attachment.get_attribute("title")
                                        if currOrder.attachments is None:
                                            currOrder.attachments = []
                                        currOrder.attachments.append(currAttachment)

                            if currOrder.attachments is not None:
                                for attachment in currOrder.attachments:
                                    try:
                                        self.navigate(attachment.attachmentURL)
                                        time.sleep(50)
                                    except:
                                        pass

                        # if not is_article_attachment:
                        if currOrder.message is None:
                            currOrder.message = ""
                        currOrder.message += article.find_element_by_class_name("msg-body").text.strip() + "\n"
                except:
                    logger.exception(sys.exc_info())

        for currOrder in config.Orders:
            if currOrder.attachments is not None:
                for attachment in currOrder.attachments:
                    try:
                        old = config.outputAttachmentsPath + attachment.attachmentTitle
                        new = config.outputAttachmentsPath + currOrder.orderNum + "_" + attachment.attachmentTitle
                        os.rename(old, new)
                        attachment.attachmentTitle = currOrder.orderNum + "_" + attachment.attachmentTitle
                        attachment.attachmentPath = new
                    except:
                        logger.exception(sys.exc_info())
