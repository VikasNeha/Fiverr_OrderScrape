import gui
import os
import sys
import config
import FiverrOrderScrape
from Utilities.myLogger import logger

# --- here goes your event handlers ---


def setDefaultOutputPaths(evt):
    fileName = "Output\\"
    outputPath = config.get_main_dir() + "\\" + fileName
    mywin['txtOutputPath'].value = outputPath


def browseOutputPath(evt):
    from gui import dialog

    outputPath = dialog.choose_directory(message="Choose the outoput directory",
                                         path=config.get_main_dir() + "/Output/")

    if outputPath is not None:
        mywin['txtOutputPath'].value = outputPath


def load(evt):
    setDefaultOutputPaths(evt)
    mywin['statusbar'].text = 'Fiverr Order Scraping Tool. Developed by Saquib Liaquat !!!'


def doOrderScrape(evt):
    if not mywin['txtFivUsername'].value or not mywin['txtFivPassword'].value:
        gui.alert("Please enter username and password")
        return
    if not os.path.isdir(mywin['txtOutputPath'].value):
        os.makedirs(mywin['txtOutputPath'].value)
    config.outputPath = mywin['txtOutputPath'].value
    config.outputAttachmentsPath = config.outputPath + "Attachments/"
    if not os.path.isdir(config.outputAttachmentsPath):
        os.makedirs(config.outputAttachmentsPath)
    config.FivUsername = mywin['txtFivUsername'].value
    config.FivPassword = mywin['txtFivPassword'].value

    try:
        gui.alert("Starting Order Scrape. \nPlease do not touch your keyboard or mouse.")
        mywin.minimized = True

        ret_value = FiverrOrderScrape.main()
        mywin.minimized = False

        if ret_value == 1:
            gui.alert("Order Scraping Done.")
        elif ret_value == 101:
            gui.alert("There were no orders to scrape.")
        elif ret_value == 102:
            gui.alert("There were no new orders to scrape.")
        else:
            gui.alert("There were some problems with scraping. Please report to developer.")


    except:
        logger.exception(sys.exc_info())
    finally:
        mywin.minimized = False


# --- gui2py designer generated code starts ---

#======== MAIN WINDOW ========#
gui.Window(name=u'Fiverr_OrderScrape',
           title=u'Fiverr Order Scraping Tool',
           maximize_box=False, resizable=False, height='400px', left='173',
           top='58', width='550px', bgcolor=u'#E0E0E0', fgcolor=u'#000000',
           image=config.get_main_dir()+'/Resources/tile.bmp', tiled=True, )

#======== HEADER LABELS ========#
gui.Label(id=281, name='label_211_281', height='17', left='50', top='40',
          width='254', transparent=True,
          font={'size': 9, 'family': 'sans serif', 'face': u'Arial'},
          parent=u'Fiverr_OrderScrape',
          text=u'Welcome to Fiverr Order Scrape Tool', )

gui.Label(id=1001, name='label_1001', height='17', left='50', top='80',
          width='131', parent=u'Fiverr_OrderScrape',
          text=u'Fiverr Username:', transparent=True, )

gui.TextBox(id=1003, name=u'txtFivUsername', height='23', left='160',
            sizer_align='center', top='80', width='150', bgcolor=u'#FFFFFF',
            editable=True, enabled=True, fgcolor=u'#000000',
            parent=u'Fiverr_OrderScrape', transparent=True)

gui.Label(id=1002, name='label_1002', height='17', left='50', top='120',
          width='131', parent=u'Fiverr_OrderScrape',
          text=u'Fiverr Password:', transparent=True, )

gui.TextBox(id=1004, name=u'txtFivPassword', height='23', left='160',
            sizer_align='center', top='120', width='150', bgcolor=u'#FFFFFF',
            editable=True, enabled=True, fgcolor=u'#000000',
            parent=u'Fiverr_OrderScrape', transparent=True, password=True)

#======== OUTPUT XLS SECTION ========#

#----- Output XLS Label -----#
gui.Label(id=348, name='label_302_348', height='17', left='50', top='180',
          width='131', parent=u'Fiverr_OrderScrape',
          text=u'Output txt files will be available at:', transparent=True, )
#----- Output Path textbox -----#
gui.TextBox(id=469, name=u'txtOutputPath', height='23', left='50',
            sizer_align='center', top='205', width='428', bgcolor=u'#FFFFFF',
            editable=False, enabled=False, fgcolor=u'#000000',
            parent=u'Fiverr_OrderScrape', transparent=True,)
#----- Open Output XLS Button -----#
gui.Button(label=u'Open Output Directory', name=u'btnOpenOutput', height='33',
           left='329', top='233', width='150', enabled=False,
           fgcolor=u'#000000', parent=u'Fiverr_OrderScrape', transparent=True, )

#----- Browse Button -----#
gui.Button(label=u'Browse...', name=u'btnBrowseOutputPath', left='60', top='233', height='33',
           fgcolor=u'#000000', parent=u'Fiverr_OrderScrape', transparent=True, )
#----- Select Default Input Button -----#
gui.Button(id=205, label=u'Select Default Output Path', name=u'btnOutputDefault',
           left='160', top='233', width='160', height='33', fgcolor=u'#000000',
           parent=u'Fiverr_OrderScrape', transparent=True, )

#======== DO ORDER SCRAPE BUTTON ========#
gui.Button(label=u'Do Order Scrape', name=u'btnDoOrderScrape', height='39',
           left='185', top='327', width='292', fgcolor=u'#000000',
           font={'size': 11, 'family': 'sans serif', 'face': u'Tahoma'},
           parent=u'Fiverr_OrderScrape', transparent=True, )

gui.StatusBar(name='statusbar', parent=u'Fiverr_OrderScrape', )

gui.Image(name='image_148', height='40', left='440', top='5', width='100',
          fgcolor=u'#000000',
          filename=config.get_main_dir()+'/Resources/python-powered.bmp',
          parent=u'Fiverr_OrderScrape', stretch=False, transparent=False, border='static')

# --- gui2py designer generated code ends ---

# get a reference to the Top Level Window:
mywin = gui.get("Fiverr_OrderScrape")

# assign your event handlers:
mywin.onload = load
mywin['btnOutputDefault'].onclick = setDefaultOutputPaths
mywin['btnBrowseOutputPath'].onclick = browseOutputPath
mywin['btnDoOrderScrape'].onclick = doOrderScrape
#mywin['btnOpenOutput'].onclick = openOutputXLS

if __name__ == "__main__":
    # myLogger.setupLogging()
    mywin.show()
    gui.main_loop()