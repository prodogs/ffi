import threading
import time
from urllib.request import HTTPBasicAuthHandler
import requests
from requests.exceptions import HTTPError
import os

from requests import Session
from requests.adapters import HTTPAdapter
from urllib3.util.ssl_ import create_urllib3_context
import requests
from requests.exceptions import HTTPError
from urllib3.exceptions import InsecureRequestWarning
from requests.auth import HTTPBasicAuth
import random
import pandas as pd

import os
import json
 
from PyQt5 import QtGui
from pdb import run
from PyQt5.QtWidgets import QApplication, QWidget, QTabWidget
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QTextEdit, QProgressBar,QLabel,QFileDialog,QComboBox, QListWidget
from PyQt5.QtWidgets import QAbstractItemView


source = "TRANSAMERICA PERSONALIZED PORTFOLIOS IRA"

CIPHERS = (
    'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:'
    'ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:'
    'DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384'
)

class DESAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        context = create_urllib3_context(ciphers=CIPHERS)
        kwargs['ssl_context'] = context
        return super(DESAdapter, self).init_poolmanager(*args, **kwargs)
class apiTestRunnerUI():

    statusLabel = QLabel("Status : ")
    errorsLabel = QLabel("Errors : ")
    scenario = QLabel("Scenario : ")
    responseFile = QTextEdit()
    test_file = QTextEdit()
    window = QWidget()
    progress_bar = QProgressBar()
    numberOfTests = QLabel("Number Of Tests : ")
    button2 = QPushButton("Run Tests")
    layout = QVBoxLayout()
    hlayout = QHBoxLayout()
    tab_widget = QTabWidget()
    tab1 = QWidget()
    tab2 = QWidget()
    runButton = QPushButton("Run Tests")
    stopButton = QPushButton("Stop Tests")
    openFileButton = QPushButton("OpenFile")
    apiTestFileNameLabel = QLabel("API Test File Name : ")
    baseUrlLabel = QLabel("Base URL : ")
    scenario = QLabel("Scenario : ")
    numberOfTests = QLabel("Number Of Tests : ")
    errorsLabel = QLabel("Errors : ")
    skippedLabel = QLabel("Skipped : ")
    statusLabel = QLabel("Status : ")
    filterLabel = QLabel("Filter : ")
    filterLayout = QHBoxLayout()
    scenarioLayout = QVBoxLayout()
    typeChoiceLayout = QVBoxLayout()
    combo_box = QComboBox()
    list_widget = QListWidget()

    
    def __init__(self):
        createQTUI()
    
    def initialize():
        setNumberOfTests(total_tests)
        setProgress(0)
        setErrors(0)
        setScenario("")
        setStatusMessage("Starting Run")
        setBaseURL(baseURL)
        setSkipped(0)

    def createQTUI():

        window.setWindowTitle('API REST Test Runner')

        runButton.setFixedSize(100, 50)
        runButton.clicked.connect(run_tests )

        stopButton.setFixedSize(100, 50)
        stopButton.clicked.connect(stopTests)
        
        openFileButton.setFixedSize(100, 50)
        openFileButton.clicked.connect(openTestFile)
        
        quitButton.setFixedSize(100, 50)
        quitButton.clicked.connect(quitApplication)

        hlayout.addWidget(runButton)
        hlayout.addWidget(stopButton)
        hlayout.addWidget(openFileButton)
        hlayout.addWidget(quitButton)

        layout.addLayout(hlayout)

        progress_bar.setRange(0, 100)
        progress_bar.setValue(50)
        progress_bar.setStyleSheet("""
        QProgressBar {
            border: 2px solid grey;
            border-radius: 5px;
            text-align: center;
        }

        QProgressBar::chunk { background-color: green;}""")
        
        layout.addWidget(progress_bar)

        apiTestFileNameLabel = QLabel("API Test File Name : ")
        layout.addWidget(apiTestFileNameLabel)

        baseUrlLabel = QLabel("Base URL : ")
        layout.addWidget(baseUrlLabel)

        scenario = QLabel("Scenario : ")
        layout.addWidget(scenario)
        
        numberOfTests = QLabel("Number Of Tests : ")
        layout.addWidget(numberOfTests)

        errorsLabel = QLabel("Errors : ")
        layout.addWidget(errorsLabel)

        skippedLabel = QLabel("Skipped : ")
        layout.addWidget(skippedLabel)

        statusLabel = QLabel("Status : ")
        statusLabel.setStyleSheet("background-color: yellow;color: black")

        layout.addWidget(statusLabel)
        layout.addWidget(filterLabel)
        layout.addLayout(filterLayout)
        
        title = QLabel("Select Scenario :")
        scenarioLayout.addWidget(title)
        combo_box.addItem("Scenario 1")
        combo_box.addItem("Scenario 2")
        combo_box.addItem("Scenario 3")
        scenarioLayout.addWidget(combo_box)
        filterLayout.addLayout(scenarioLayout)

        typeChoiceLayout = QVBoxLayout()
        title = QLabel("Select Types :")
        typeChoiceLayout.addWidget(title)
        list_widget = QListWidget()
        list_widget.setSelectionMode(QAbstractItemView.MultiSelection)
        typeChoiceLayout.addWidget(list_widget)
        filterLayout.addLayout(typeChoiceLayout)
        
        for i in range(10):
            list_widget.addItem(f"Item {i+1}")

        filterLayout.addWidget(list_widget)

        tab_widget = QTabWidget()
        tab_widget.setFixedSize(800, 600)

        current_directory = os.getcwd()
        print(current_directory)
        text = "Test File"
        global testFileText
        testFileText = QTextEdit()
        setTestJsonText(text)

        tab_widget.addTab(testFileText, "Test File")
        layout.addWidget(tab_widget)

        global responseFileText
        responseFileText = QTextEdit()
        setResponseFileText(text)

        tab_widget.addTab(responseFileText, "Results File")
        layout.addWidget(tab_widget)

        window.setLayout(layout)
        window.show()

    class CompareCheck:

class apiTestRunner():
    def send_get_request(baseURL,url):
        global requestURL

        start_time = time.time()

        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

        requestURL = baseURL + url

        try:
            response = requests.get(url, verify=False)

            # If the response was successful, no Exception will be raised
            response.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')  # Python 3.6
        except Exception as err:
            print(f'Other error occurred: {err}')  # Python 3.6
        else:
            print('Success!')

        return response.json()  # or response.text, o

    def send_api_request(url,body,source, acctID, account_no):
        global baseURL
        global requestURL

        s = Session()
        s.mount('https://', DESAdapter())

        random_number = str(random.randint(1000, 9999))
        requestID = "automated_tests" + random_number

        #print(url)
        username = "user" 
        password = "password!"
        auth = HTTPBasicAuth(username, password)
        start_time = time.time()

        requestURL = baseURL + url
        if (body == None):
            response = requests.get(requestURL, auth=auth)
        else:
            response = requests.post(requestURL, auth=auth, json=body)

        executionTime = time.time() - start_time

        return response

    def account_performance_test(json_data):
        account_no = json_data.get('account_no')
        acctID = json_data.get('acctID')    
        start = json_data.get('start')  
        end = json_data.get('end')

        url = '/advisor-partners-app-svc/restservices/participant/account-performance/{}/{}/{}/{}/{}'.format(source, acctID,account_no,start,end)

        response = send_api_request(url,None,source, acctID, account_no)

        return response

    def account_status_test(json_data):
        account_no = json_data.get('account_no')
        acct_id = json_data.get('acctID')  # Renamed the variable to 'acct_id'
        url = '/advisor-partners-app-svc/restservices/participant/account-status/{}/{}/{}'.format(source, acct_id, account_no)

        response = send_api_request(url, None, source, acct_id, account_no)

        return response

    def transaction_test(json_data):
        account_no = json_data.get('account_no')
        acctID = json_data.get('acctID')
        requestID = json_data.get('requestID')

        url = '/advisor-partners-app-svc/restservices/participant/transaction-status'
        body = json_data.get('body')

        response = send_api_request(url,body,source, acctID, account_no)

        return response

    def realignments_test(json_data):
        account_no = json_data.get('account_no')
        acctID = json_data.get('acctID')

        url = '/advisor-partners-app-svc/restservices/participant/realignments/{}/{}/{}'.format(source, acctID,account_no)
        body = json_data.get('body')

        response = send_api_request(url,body,source, acctID, account_no)

        return response

    def future_allocation_test(json_data):
        account_no = json_data.get('account_no')
        acctID = json_data.get('acctID')

        url = '/advisor-partners-app-svc/restservices/participant/future-allocation/{}/{}/{}'.format(source, acctID,account_no)
        body = json_data.get('body')

        response = send_api_request(url,body,source, acctID, account_no)

        return response

    def doc_list_test(json_data):
        body = json_data.get('body')
        acctID = json_data.get('acctID')
        account_no = json_data.get('account_no')
        start = json_data.get('start')
        end = json_data.get('end')

        url = '/advisor-partners-app-svc/restservices/customer/getDocDetails?customerId={}&startDate={}&endDate={}'.format(acctID,start,end)

        response = send_api_request(url,body,source, acctID, account_no)

        return response

    def doc_test(json_data):
        account_no = json_data.get('account_no')
        acctID = json_data.get('acctID')
        start = json_data.get('start')
        end = json_data.get('end')
        body = json_data.get('body')
        url = '/advisor-partners-app-svc/restservices/customer/downloadDoc'

        response = send_api_request(url,body,source, acctID, account_no)

        return response


    flag: bool
    status: str

    def checkResponse(testData, responseJson, responseStatus):
        #print(testData)
        compareCheck = CompareCheck()  # Instantiate the CompareCheck class using the = operator
        if int(testData.get("response_status")) == responseStatus:
            compareCheck.flag = True
            compareCheck.status = "Response status matches expected {}\n".format(testData.get("response_status"))
        else:
            compareCheck.flag = False
            compareCheck.status = "Response status does not match expected {}, got {}\n".format(testData.get("response_status"), responseStatus)  # Close the parentheses
        return compareCheck


class UIAPIRunOutput(APIRunOutput):
    def __init__(self):
        super().__init__()

    def showTestResults(self, message):
        global testResultsText
        super().showTestResults(message)
        testResultsText.config(text=message)

    def logThis(self, file, message):
        global logMessages
        global responseFileText
        super().logThis(file, message)
        responseFileText.insertPlainText(logMessages + "\n")
        responseFileText.moveCursor(QtGui.QTextCursor.End)

    def setScenarioText(scenarioText):
        global scenario
        scenario.setText(scenarioText)

    def setStatusMessage(status):
        global statusLabel
        statusLabel.setText(f"Status : {status}")

    def setErrors(errors):
        global errorsLabel
        errorsLabel.setText(f"Errors : {errors}")

    def setNumberOfTests(tests):
        global numberOfTests
        numberOfTests.setText(f"Number of Tests : {tests}")

    def setSkipped(skipped):
        global skippedLabel
        skippedLabel.setText(f"Skipped : {skipped}")


class APIRunOutput():
    def __init__(self):
        super().__init__()

    def setNumberOfTests(tests):
        None

    def setErrors(errors):
        None
    def setSkipped(skipped):
        None

    def setScenarioText(scenarioText):
        None

    def setProgress(progress):
        global progress_bar
        progress_bar.setValue(progress)

    def showTestResults(message):
        responseFileText.insertPlainText(message + "\n")
        responseFileText.moveCursor(QtGui.QTextCursor.End)
        
    def setStatusMessage(status):
        None

    def setProgress(progress):
        None

def logThis(file, message):
    global logMessages
    global runUI, responseFileText

    file.write(message)
    logMessages = logMessages + "LOG : "+message
    if runUI:
        responseFileText.insertPlainText(logMessages + "\n")
        responseFileText.moveCursor(QtGui.QTextCursor.End)

    else:
        print(message)
    
    responseFileText.insertPlainText(logMessages + "\n")
    responseFileText.moveCursor(QtGui.QTextCursor.End)

def showTestResults(message):
    global runUI
    if runUI:
        testResultsText.config(text=message)


def run_tests():

    global baseURL
    global runUI

    runUI = False
    responseFileName = "test_response_"+time.strftime("%Y%m%d-%H%M%S")+".txt"
    responseFile = open(responseFileName, 'w')


    if os.path.exists('./tests.json'):
        with open('./tests.json', 'r') as f:
            if os.stat('./tests.json').st_size != 0:
                try:
                    testLoad = json.load(f)
                except json.JSONDecodeError:
                    logThis(responseFile,"File is not valid JSON.")
            else:
                logThis(responseFile,"File is empty.")
    else:
        logThis(responseFile,"File does not exist.")
    

    data = testLoad.get("tests")
    baseURL = testLoad.get("baseURL")
    testName = testLoad.get("testName")\
    total_tests = len(data)

    initializeTest(testLoad)

    logThis(responseFile,"Running Tests for {}\n".format(testName))
    logThis(responseFile,"Run Time {}\n".format(time.strftime("%Y%m%d-%H%M%S")))
    logThis(responseFile,"-------------------------------------------------------------------\n\n")
    logThis(responseFile,"Running {} Tests\n".format(len(data)))
    logThis(responseFile,"Base URL =  {} \n".format(baseURL))
    logThis(responseFile,"-------------------------------------------------------------------\n\n")

    errors = 0
    compareString = ""
    tests_processed = 0
    tests_skipped = 0
    runUI = True

    for test in data:
        global requestURL
        runTest = test.get("run")

        if (runTest == "true"):
            tests_processed += 1
            logThis(responseFile,"-------------------------------------------------------------------\n\n")
            logThis(responseFile,"Running testing case #{} \n".format(tests_processed))
            logThis(responseFile,"Scenario : {}\n".format(test.get("scenario")))
            logThis(responseFile,"Test Type : {} \nTest Data : {}\n".format(test.get("type"),test))
        
            compareString = ""
            start_time = time.time()

            if test.get("type") == "account-status":
                response = account_status_test(test)
                #print(response)
                compareReturn = checkResponse(test,response.json, response.status_code)
                compareString = compareReturn.status
                if (compareReturn.flag== False): errors +=1

            if (test.get("type") == "account-performance"):
                response = account_performance_test(test)
                compareReturn = checkResponse(test,response.json, response.status_code)
                compareString = compareReturn.status
                if (compareReturn.flag== False): errors +=1

            if test.get("type") == "transaction-status":
                response = transaction_test(test)
                compareReturn = checkResponse(test, response.json, response.status_code)
                compareString = compareReturn.status
                if (compareReturn.flag== False): errors +=1

            if (test.get("type") == "future-allocation"):
                response = future_allocation_test(test)
                compareReturn = checkResponse(test,response.json, response.status_code)
                compareString = compareReturn.status
                if (compareReturn.flag== False): errors +=1

            if (test.get("type") == "realignments"):
                response = realignments_test(test)
                compareReturn = checkResponse(test,response.json, response.status_code)
                compareString = compareReturn.status
                if (compareReturn.flag== False): errors +=1

            if (test.get("type") == "doc-list"):
                response = doc_list_test(test)
                compareReturn = checkResponse(test,response.json, response.status_code)
                compareString = compareReturn.status
                if (compareReturn.flag== False): errors +=1

            if (test.get("type") == "doc"):
                response = doc_test(test)
                compareReturn = checkResponse(test,response.json, response.status_code)
                compareString = compareReturn.status

            end_time = time.time()
            executionTime = end_time - start_time

            if (runTest == "true"):
                variableTests = test.get("variableTests")
                if (variableTests is not None):
                    logThis(responseFile,"Variable Tests : \n")

                logThis(responseFile,"Request URL : {}\n".format(requestURL))
                logThis(responseFile,"Response Data : {}".format(response))
                if response is not None:
                    if (test.get("type") != "doc"):
                        logThis(responseFile,"Response Data : "+response.text+"\n")
                        #json.dump(response.text, responseFile)
                    else:
                        logThis(responseFile,"Status code return : {}\n".format(response.status_code))

                logThis(responseFile,compareString)
                logThis(responseFile,"Execution Time = {} : \n".format(executionTime))

                if (compareReturn.flag):
                    logThis(responseFile,"Test Result :  Passed\n")
                else:
                    logThis(responseFile,"Test Result : Failed\n")
        else :
            tests_skipped += 1
            logThis(responseFile,"\n\n")
            logThis(responseFile,"Test Case # {} Skipped\n".format(tests_processed))
            logThis(responseFile,"Skipped Scenario : {}\n".format(test.get("scenario")))    
        
        logThis(responseFile,"-------------------------------------------------------------------\n\n")

    testResults = "\n\n {} Tests with {} Errors, {:.2%} Failure Rate Skipped {} ".format(tests_processed, errors, errors/total_tests,tests_skipped)
    logThis(responseFile,testResults)
    logThis(responseFile,"-------------------------------------------------------------------\n\n")

    showTestResults(testResults)
    responseFile.close()

def on_button_click():
    thread = threading.Thread(target=run_tests)
    thread.start()

def on_show_tests_click():
    os.system("notepad.exe tests.json")

def setTestJsonText(text):
    global testFileText
    testFileText.setPlainText(text)

def setResponseFileText(text):
    global responseFileText

def stopTests():
    print("Stopping Tests")

def quitApplication():
    exit()

def setStatusMessage(status):
    global statusLabel
    statusLabel.setText(f"Status : {status}")

def setProgress(progress):
    global progress_bar
    progress_bar.setValue(progress)

def setScenario(scenarioText):
    global scenario
    scenario.setText(scenarioText)

def setErrors(errors):
    global errorsLabel
    errorsLabel.setText(f"Errors : {errors}")

def setNumberOfTests(tests):
    global numberOfTests
    numberOfTests.setText(f"Number of Tests : {tests}")

def setSkipped(skipped):
    global skippedLabel
    skippedLabel.setText(f"Skipped : {skipped}")

def setBaseURL(baseURL):
    global baseUrlLabel
    baseUrlLabel.setText(f"Base URL : {baseURL}")

def openTestFile():
    file_dialog = QFileDialog()
    file_name, _ = file_dialog.getOpenFileName()

    if file_name:
        print(f"Selected file: {file_name}")
    
    return file_name

class APITestRunnerApp():

    def run():
        app = QApplication([])
        createQTUI()
        run_tests()

        app.exec_()
        return

def main():
    testRunnerApp = new APITestRunnerApp()
    testRunnerApp.run()

if __name__ == '__main__':
    main()

