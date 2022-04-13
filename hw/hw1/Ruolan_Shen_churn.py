import csv
import json
import sys
import requests

#k_value = str(1)

k_value = str(sys.argv[1])
url_index ='https://dsci551hw1-b6c45-default-rtdb.firebaseio.com/WA_Fn-UseC_-Telco-Customer-Churn.json?orderBy="Churn"&equalTo="Yes"&limitToFirst='+k_value+'&print=pretty'
    
response = requests.get(url_index)
reloadJS = json.loads(response.text)

i = 0
# for index, x in list(reloadJS.items()):

# data =
if(k_value == '1'):
    print(reloadJS[1]['customerID'])
else:
    data = sorted(reloadJS.items(), key=lambda x: x[1]['customerID'])
    for index, x in list(data):
    
      
            
        print(x['customerID'])
            
            
