import sys
import requests
import json
import pandas as pd
import csv
import time
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QCalendarWidget
from PyQt5.QtCore import pyqtSlot, QDate
import os


class App(QWidget):
    global currentYear, currentMonth, currentDay

    currentMonth = datetime.now().month
    currentYear = datetime.now().year
    currentDay = datetime.now().day

    def __init__(self):
        super().__init__()
        self.title = 'Lending Game Download CSV'
        self.left = 100
        self.top = 100
        self.width = 400
        self.height = 400
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.labelCalendar = QLabel(self)
        self.labelCalendar.setText('Starting on which date would you like to pull data?')
        self.labelCalendar.move(20, 20)
        self.labelCalendar.adjustSize()

        self.calendar = QCalendarWidget(self)
        self.calendar.move(20, 40)
        self.calendar.setGridVisible(True)
        self.calendar.setSelectedDate(QDate(currentYear, currentMonth, currentDay))
        self.calendar.clicked.connect(self.showDate)

        self.labelC = QLabel(self)
        date = self.calendar.selectedDate()
        self.labelC.setText(date.toString())
        self.labelC.resize(100,20)
        self.labelC.move(20, 240)

        self.labelA = QLabel(self)
        self.labelA.setText('Click the button below to get lending game data')
        self.labelA.move(20, 300)
        self.labelA.adjustSize()
        self.labelB = QLabel(self)
        self.labelB.move(20, 320)
        self.labelDate = QLabel(self)
        self.labelDate.move(20, 340)
        self.labelDate.resize(100, 20)

        self.pushButton = QPushButton('Click to get CSV', self)
        self.pushButton.setToolTip('Get CSV here')
        self.pushButton.move(20, 340)
        self.pushButton.clicked.connect(self.on_click)
        self.show()

    def showDate(self, date):
        self.labelC.setText(date.toString())

    @pyqtSlot()
    def on_click(self):

        self.labelA.setText('Done! Please check the directory for your CSV output!')
        self.labelA.adjustSize()
        self.labelB.setText('Please close this window and the command prompt window.')
        self.labelB.adjustSize()
        self.pushButton.hide()
        date = self.calendar.selectedDate().toString("yyyyMMdd")
        date = int(date)
        #self.labelDate.setText(date)


        # must specify
        apiToken = ""
        mailingListID = ""
        fileFormat = "csv"
        dataCenter = 'umich'

        baseUrl = "https://{0}.qualtrics.com/API/v3/mailinglists/{1}/contacts/".format(dataCenter, mailingListID)
        headers = {
            "content-type": "application/json",
            "x-api-token": apiToken,
        }

        requestDownloadUrl = baseUrl
        requestDownload = requests.request("GET", requestDownloadUrl, headers=headers, stream=True)

        data = json.loads(requestDownload.content)['result']['elements']

        # there is no header row in the csv, so the header names are just taken from the keys in the first row of the data
        with open('temp.csv', 'w', encoding='utf8', newline='') as output_file:
            mylist = csv.DictWriter(output_file,
                                    fieldnames=data[0].keys(),
                                    )
            mylist.writeheader()
            mylist.writerows(data)

        # reads csv, but all values are loaded as string.
        df = pd.read_csv('temp.csv')

        # convert embedded data to dict using apply(eval)
        # to check type, use .apply(type)
        ed = df.embeddedData.apply(eval)
        df2 = ed.apply(pd.Series)

        # concatenate old with new
        final = pd.concat([df, df2], axis=1)

        # drop junk
        final = final.drop(
            columns=["id", "firstName", "embeddedData", "lastName", "email", "language", "unsubscribed", "responseHistory",
                     "emailHistory", "A_Info", "B_Info", "C_Info", "D_Info", "E_Info", "F_Info", "G_Info", "H_Info",
                     "I_Info",
                     "J_Info", "TriggerResponseID", "TriggerSurveyID"])

        # save to csv
        timestr = time.strftime("%Y%m%d-%H%M%S")
        final['DateTaken'] = final['DateTaken'].astype(int)
        final = final[final.DateTaken >= date]
        final.to_csv('lendingGameData'+timestr+".csv")
        os.remove("temp.csv")
		
		
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

# used pyinstaller to get this to be added as a single exe file for
# non-python users to run code
