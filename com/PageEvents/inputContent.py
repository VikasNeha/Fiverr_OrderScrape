import config
import codecs
from Utilities.myLogger import logger
import sys
import os
import shutil


class orderItem:
    itemName = None
    itemQuantity = None
    itemDuration = None
    itemAmount = None


class orderAttachment:
    attachmentURL = None
    attachmentTitle = None
    attachmentPath = None


class Order:
    orderURL = None
    orderNum = None
    buyerName = None
    dueDate = None
    orderAmount = None
    items = None
    message = None
    attachments = None


def readScrapedOrders():
    fileName = "Resources\\scrapedOrders.txt"
    f = open(config.get_main_dir() + "\\" + fileName)
    for line in f.readlines():
        config.ScrapedOrders.append(line.rstrip('\n'))
    f.close()


def writeOutputFiles():
    for currOrder in config.Orders:
        try:
            fout = codecs.open(config.outputPath + currOrder.orderNum + ".txt", "wb", encoding="utf-8")
            print>>fout, "Order Number:", currOrder.orderNum, "\r"
            print>>fout, "Buyer Name:", currOrder.buyerName, "\r"
            # print>>fout, "Due Date:", currOrder.dueDate, "\r"
            # print>>fout, "Order Amount:", currOrder.orderAmount, "\r"
            # if currOrder.items is not None:
            #     print>>fout, " ", "\r"
            #     print>>fout, "------- ITEM INFORMATION", "\r"
            #     i = 1
            #     for item in currOrder.items:
            #         print>>fout, "Item#", i, "\r"
            #         print>>fout, "Item Name:", item.itemName, "\r"
            #         print>>fout, "Item Qty:", item.itemQuantity, "\r"
            #         print>>fout, "Due In:", item.itemDuration, "\r"
            #         print>>fout, "Amount:", item.itemAmount, "\r"
            #         i += 1
            if currOrder.message is not None:
                print>>fout, " ", "\r"
                print>>fout, "********** INSTRUCTION ***********", "\r"
                print>>fout, currOrder.message.replace("\n", "\r\n"), "\r"
            # if currOrder.attachments is not None:
            #     print>>fout, " ", "\r"
            #     print>>fout, "------- ATTACHMENTS", "\r"
            #     i = 1
            #     for attachment in currOrder.attachments:
            #         print>>fout, "#", i, "-", attachment.attachmentTitle, "-", attachment.attachmentPath.replace("/", "\\"), "\r"
            #         i += 1
            fout.close()
            config.ScrapedOrders.append(currOrder.orderNum)
        except:
            logger.exception(sys.exc_info())


def writeScrapedOrders():
    f = None
    try:
        fileName = "Resources\\scrapedOrders.txt"
        f = open(config.get_main_dir() + "\\" + fileName, "wb")
        for orderNum in config.ScrapedOrders:
            print>>f, orderNum
        f.close()
    except:
        logger.exception(sys.exc_info())
    finally:
        if f:
            f.close()


def make_directory_and_move():
    for currOrder in config.Orders:
        try:
            outputDirPath = config.outputPath + currOrder.orderNum
            if not os.path.isdir(outputDirPath):
                os.makedirs(outputDirPath)
            shutil.copy2(outputDirPath+".txt", outputDirPath)
            os.remove(outputDirPath+".txt")
            if currOrder.attachments is not None:
                for attachment in currOrder.attachments:
                    shutil.copy2(attachment.attachmentPath, outputDirPath)
                    os.remove(attachment.attachmentPath)
        except:
            logger.exception(sys.exc_info())