import csv
import json
import requests
import sys

k_value = str(sys.argv[1])

# k_value = sys.argv[1]


url_index ='https://dsci551hw1-b6c45-default-rtdb.firebaseio.com/WA_Fn-UseC_-Telco-Customer-Churn.json?orderBy="tenure"&startAt='+k_value+'&print=pretty'

    
    
response = requests.get(url_index)
reloadJS = json.loads(response.text)
ans=[]
i = 0
# len(reloadJS)
# print(type(reloadJS.items()['tenure'])

#
for index, x in list(sorted(reloadJS.items())):
    
#         if(x['tenure'] >= '10' ):
#     print(x['tenure'])
#             ans.append(x['customerID'])
    i = i+1
    
print(i)
