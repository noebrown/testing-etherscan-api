import requests
import datetime
from tabulate import tabulate
from datetime import datetime


# Defining constants token address (used vitalik.eth as test)and api key
testAddress = "0xd8da6bf26964af9d7eed9e03e53415d37aa96045"
# apiKey = "INSERT YOUR API KEY AND UNCOMMENT"


# Fetch normal transactions
fetchNormTrans = f'https://api.etherscan.io/api?module=account&action=txlist&address={testAddress}&startblock=0&endblock=99999999&page=1&offset=10&sort=asc&apikey={apiKey}'
normalTransactions = requests.get(fetchNormTrans).json()


# Convert the epoch timestamp to a datetime object
def epoch_to_datetime(epoch_timestamp):
    # Convert the epoch timestamp to a datetime object
    datetime_obj = datetime.fromtimestamp(epoch_timestamp)
    # Format the datetime object into a readable string
    formatted_datetime = datetime_obj.strftime('%Y-%m-%d %H:%M:%S')
    
    return formatted_datetime


# Determine if credit or debit transaction
def credit_or_debit(fromAddress, toAddress):
    if (fromAddress == testAddress and toAddress != testAddress):
        transactionType = "credit"
    if (fromAddress != testAddress and toAddress == testAddress):
        transactionType = "debit"
    if (fromAddress == testAddress and toAddress == testAddress):
        transactionType = "void"
    
    return transactionType
    

# Convert wei value to eth value
def convert_to_eth(value):
    ethValue = float(value) / 1000000000000000000

    return ethValue


# Extract certain information from API
extractedInfo = []
for transaction in normalTransactions["result"]:
    transaction_info = {
        "hash": transaction["hash"],
        "timeStamp": epoch_to_datetime(int(transaction["timeStamp"])),
        "from": transaction["from"],
        "to": transaction["to"],
        "transactionType": credit_or_debit(transaction["from"], transaction["to"]),
        "value": convert_to_eth(transaction["value"]),
        "gasPrice": convert_to_eth(transaction["gasPrice"])
    }
    
    extractedInfo.append(transaction_info)


# Generate table of extracted data
header = extractedInfo[0].keys()
rows =  [x.values() for x in extractedInfo]
print(tabulate(rows, header))
