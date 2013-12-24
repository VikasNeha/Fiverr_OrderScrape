import config
from PageEvents import inputContent
from PageEvents.fiverrEvents import FiverrEvents
from Utilities.myLogger import logger
import sys
from PageEvents import inputContent


def main():
    inputContent.readScrapedOrders()
    ret_value = doOrderScrape()
    return ret_value


def doOrderScrape():
    try:
        fiv = FiverrEvents()
        fiv.login_to_fiverr()
        fiv.open_sales_page()
        ret_value = fiv.scrape_order_summary()
        if ret_value == 1:
            fiv.scrape_order_details()
            inputContent.writeOutputFiles()
            inputContent.writeScrapedOrders()
            inputContent.make_directory_and_move()
        fiv.destroy()
        return ret_value
        # for currOrder in config.Orders:
        #     print "-------"
        #     print currOrder.orderURL
        #     print currOrder.orderNum
        #     print currOrder.buyerName
        #     print currOrder.dueDate
        #     print currOrder.orderAmount
        #     for item in currOrder.items:
        #         print item.itemName
        #         print item.itemQuantity
        #         print item.itemDuration
        #         print item.itemAmount
        #     print currOrder.message
        #
        #     if currOrder.attachments:
        #         for attachment in currOrder.attachments:
        #             print attachment.attachmentTitle
    except:
        logger.exception(sys.exc_info())
