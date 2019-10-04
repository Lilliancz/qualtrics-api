import sys
import requests
import json
import pandas as pd
import csv
import time
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel
from PyQt5.QtCore import pyqtSlot
import os


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Lending Game Download CSV'
        self.left = 100
        self.top = 100
        self.width = 700
        self.height = 400
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.labelA = QLabel(self)
        self.labelA.setText('Click the button below to get lending game data')
        self.labelA.move(120, 100)
        self.labelA.adjustSize()
        self.labelB = QLabel(self)


        button = QPushButton('Click to get CSV', self)
        button.setToolTip('Get CSV here')
        button.move(250, 200)
        button.clicked.connect(self.on_click)
        self.show()
		
    @pyqtSlot()
    def on_click(self):

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
                     "J_Info", "DateTaken", "TriggerResponseID", "TriggerSurveyID"])

        # save to csv
        timestr = time.strftime("%Y%m%d-%H%M%S")
        final.to_csv('lendingGameData'+timestr+".csv")
        os.remove("temp.csv")
		
        self.labelA.setText('Done! Please check the directory for your CSV output!')
        self.labelA.move(100, 100)
        self.labelA.adjustSize()
        self.labelB.setText('Please close this window and the command prompt window.')
        self.labelB.move(50, 300)
        self.labelB.adjustSize()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

# used pyinstaller to get this to be added as a single exe file for
# non-python users to run code
