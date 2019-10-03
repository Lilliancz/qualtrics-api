import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot



class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Lending Game Download CSV'
        self.left = 10
        self.top = 10
        self.width = 320
        self.height = 200
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        button = QPushButton('Click to get CSV', self)
        button.setToolTip('This is an example button')
        button.move(100, 70)
        button.clicked.connect(self.on_button_clicked)

        self.show()

    def on_button_clicked():
        alert = QMessageBox()
        alert.setText('Button pressed!')
        alert.exec_()

        import requests
        import json
        import pandas as pd
        import csv

        # this version accepts manual input from the user
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
        with open('contacts.csv', 'w', encoding='utf8', newline='') as output_file:
            mylist = csv.DictWriter(output_file,
                                    fieldnames=data[0].keys(),
                                    )
            mylist.writeheader()
            mylist.writerows(data)

        # reads csv, but all values are loaded as string.
        df = pd.read_csv('contacts.csv')

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
        final.to_csv('rest.csv')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
