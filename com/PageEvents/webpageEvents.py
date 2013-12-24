from selenium import webdriver
from selenium.webdriver.support import ui
from selenium.common.exceptions import *
import config
from Utilities.constants import IDMODE
import logging
# from socket import error as socket_error
# import time
# import sys
# import subprocess
# import shlex
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

module_logger = logging.getLogger('main.webpageEvents')


# noinspection PyBroadException
class WebpageEvents(object):

    def __init__(self):
        ffProfile = FirefoxProfile()
        ffProfile.set_preference('permissions.default.image', 2)
        ffProfile.set_preference('browser.download.manager.showWhenStarting', False)
        ffProfile.set_preference('browser.download.folderList', 2)
        ffProfile.set_preference('browser.download.dir', config.outputAttachmentsPath.replace("/", "\\"))
        ffProfile.set_preference('browser.download.manager.closeWhenDone', True)

        mimeTypes = 'text/csv,application/csv,text/plain,text/comma-separated-values,text/html'
        mimeTypes += ',application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        mimeTypes += ',application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        mimeTypes += ',application/zip,application/msword,application/pdf,binary/octet-stream'
        ffProfile.set_preference('browser.helperApps.neverAsk.saveToDisk', mimeTypes)
        self.driver = webdriver.Firefox(ffProfile)


    def destroy(self):
        self.driver.quit()

    def navigate(self, url):
        self.driver.get(url)

    def findElement(self, idMode, idValue):
        try:
            webElement = None
            self.waitUntilElementIsPresent(idMode, idValue)
            if idMode == IDMODE.ID:
                webElement = self.driver.find_element_by_id(idValue)
            elif idMode == IDMODE.CLASS:
                webElement = self.driver.find_element_by_class_name(idValue)
            elif idMode == IDMODE.PARTIAL_LINK_TEXT:
                webElement = self.driver.find_element_by_partial_link_text(idValue)
            elif idMode == IDMODE.LINK_TEXT:
                webElement = self.driver.find_element_by_link_text(idValue)
            return webElement
        except (NoSuchElementException, ElementNotVisibleException, TimeoutException):
            raise

    def waitUntilElementIsPresent(self, idMode, idValue):
        try:
            wait = ui.WebDriverWait(self.driver, config.webElementTimeOut)
            if idMode == IDMODE.ID:
                wait.until(lambda driver: self.driver.find_element_by_id(idValue))
            elif idMode == IDMODE.CLASS:
                wait.until(lambda driver: self.driver.find_element_by_class_name(idValue))
            elif idMode == IDMODE.PARTIAL_LINK_TEXT:
                wait.until(lambda driver: self.driver.find_element_by_partial_link_text(idValue))
            elif idMode == IDMODE.LINK_TEXT:
                wait.until(lambda driver: self.driver.find_element_by_link_text(idValue))
        except:
            raise

    def getElementText(self, idMode, idValue):
        try:
            return self.findElement(idMode, idValue).text
        except:
            raise

    def clickPartialLink(self, idValue):
        try:
            self.findElement(IDMODE.PARTIAL_LINK_TEXT, idValue).click()
        except:
            raise

    def takeScreenshot(self, fileName):
        try:
            self.driver.get_screenshot_as_file(fileName)
        except:
            return

    def enterText(self, idMode, idValue, text):
        textbox = self.findElement(idMode, idValue)
        textbox.clear()
        textbox.send_keys(text)

    def clickButton(self, buttonText):
        allButtons = self.driver.find_elements_by_tag_name('button')
        buttonFound = False
        for currButton in allButtons:
            if currButton.text == buttonText:
                currButton.click()
                buttonFound = True
                break
        if not buttonFound:
            raise Exception('Problem in finding and clicking button: ' + buttonText)

    def assertLinkPresent(self, linkText):
        try:
            self.waitUntilElementIsPresent(IDMODE.PARTIAL_LINK_TEXT, linkText)
        except:
            raise


# def start_selenium_server():
#     fileName = "Utilities/selenium-server-standalone-2.38.0.jar"
#     pathName = config.get_main_dir() + "/" + fileName
#     print pathName
#     # null = open(config.get_main_dir() + "/Resources/null")
#     proc = subprocess.Popen(shlex.split('java -jar {p}'.format(p=pathName)))
#     return proc