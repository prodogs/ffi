import threading
import time
from urllib.request import HTTPBasicAuthHandler
import requests
from requests.exceptions import HTTPError

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
import tkinter as tk

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

def  account_status_test(json_data):

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

class CompareCheck:
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

def logThis(file, message):
    global logMessages
    global runUI
    file.write(message)
    logMessages = logMessages+ "LOG : "+message
    if runUI:
        text.insert(tk.END, logMessages + "\n")
        text.see(tk.END)  # Scroll the Text widget to show the latest entry
    else:
        print(message)

def update_log():
    while True:
        time.sleep(1)  # Wait for 1 second
       # message = "Updating at " + time.ctime()
        root.after(0, text.insert, tk.END, logMessages + "\n")

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
    showTestResults("")
  

    # Check if the file exists
    if os.path.exists('./tests.json'):
        # Open the file
        with open('./tests.json', 'r') as f:
            # Check if the file is not empty
            if os.stat('./tests.json').st_size != 0:
                # Load the JSON data from the file
                try:
                    testLoad = json.load(f)
                    # Now data contains the data from the JSON file
                    # print(data)
                except json.JSONDecodeError:
                    logThis(responseFile,"File is not valid JSON.")
            else:
                logThis(responseFile,"File is empty.")
    else:
        logThis(responseFile,"File does not exist.")

    data = testLoad.get("tests")
    baseURL = testLoad.get("baseURL")
    testName = testLoad.get("testName")

    total_tests = len(data)

 
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

global logMessages
global runUI
logMessages = ""
runUI = False

if runUI:
    root = tk.Tk()
    root.geometry("800x600")  # Width x Height
    root.title("API Test Runner")
    button = tk.Button(root, text="Run Tests!", command=on_button_click)
    button.pack()
    showTests = tk.Button(root, text="Show Tests!", command=on_show_tests_click)
    showTests.pack()

    testResultsText = tk.Label(root, text="Test Results")
    testResultsText.pack()
    text = tk.Text(root, font=("Arial", 8),width=800,height=500) 
    text.pack()
    text.insert(tk.END, "Welcome to the API Test Runner\n")

    root.mainloop()
else:
    run_tests()