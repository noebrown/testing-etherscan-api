import requests
import datetime
import tabulate
from tabulate import tabulate
from datetime import datetime


# Defining constants token address (used vitalik.eth as test)and api key
testAddress = "0xd8da6bf26964af9d7eed9e03e53415d37aa96045"
# apiKey = "INSERT YOUR API KEY AND UNCOMMENT"


# Fetch internal transactions
fetchNormTrans = f'https://api.etherscan.io/api?module=account&action=txlistinternal&address={testAddress}&startblock=0&endblock=99999999&page=1&offset=10&sort=asc&apikey={apiKey}'
internalTransactions = requests.get(fetchNormTrans).json()


# Convert the epoch timestamp to a datetime object
def epoch_to_datetime(epoch_timestamp):
    datetimeObj = datetime.fromtimestamp(epoch_timestamp)
    formattedDatetime = datetimeObj.strftime('%Y-%m-%d %H:%M:%S')
    
    return formattedDatetime

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
    ethBalance = float(value) / 1000000000000000000

    return ethBalance

# Extract certain information from API
extractedInfo = []
for transaction in internalTransactions["result"]:
    transaction_info = {
        "hash": transaction["hash"],
        "timeStamp": epoch_to_datetime(int(transaction["timeStamp"])),
        "from": transaction["from"],
        "to": transaction["to"],
        "transactionType": credit_or_debit(transaction["from"], transaction["to"]),
        "value": convert_to_eth(transaction["value"])
        # still trying to determine how gas is used and what not
        # "gasPrice": convert_to_eth(transaction["gasPrice"])
    }
    
    extractedInfo.append(transaction_info)


# Generate table of extracted data
header = extractedInfo[0].keys()
rows =  [x.values() for x in extractedInfo]
print(tabulate(rows, header))
