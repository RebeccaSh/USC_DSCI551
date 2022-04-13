import csv
import json
import requests


         

csvFilePath = r'WA_Fn-UseC_-Telco-Customer-Churn.csv'
# jsonFilePath = 'WA_Fn-UseC_-Telco-Customer-Churn.json'
baseURL = 'https://dsci551hw1-b6c45-default-rtdb.firebaseio.com/WA_Fn-UseC_-Telco-Customer-Churn'
# make_json(csvFilePath, jsonFilePath)
data = {}
i = 1
    # Open a csv reader called DictReader
with open(csvFilePath, encoding='utf-8') as csvf:
    csvReader = csv.DictReader(csvf)
#
    for rows in csvReader:
        rows['tenure']  = int(rows['tenure'])
        if(rows['SeniorCitizen']=='1'):
#                 print(rows['customerID'])
            key = i
            data[key] = rows
            i = i+1
#             print(key)
putResponse = requests.put(baseURL + '.json', json.dumps(data, indent=4))

# try:
#     putResponse = requests.put(baseURL + '.json', json.dumps(data, indent=4))
#     if putResponse.status_code == 200:
#         print("Upload {} Successfully".format('data'))
#     else:
#         print("Upload data failed, Reason: {}".format(putResponse.text))
# except:
#     print("Upload {} failed".format('data'))

        



