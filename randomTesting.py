import requests
import datetime
from tabulate import tabulate
from datetime import datetime


# Defining constants token address (used vitalik.eth as test)and api key
# token_address = input('What is your token address?\n') 
testAddress = "0xd8da6bf26964af9d7eed9e03e53415d37aa96045"
# apiKey = "INSERT YOUR API KEY AND UNCOMMENT"


# print a readable version of response
# print(responseEthPrice) 


# Fetch normal transactions
fetchNormTrans = f'https://api.etherscan.io/api?module=account&action=txlist&address={test_address}&startblock=0&endblock=99999999&page=1&offset=10&sort=asc&apikey={api_key}'
normalTransactions = requests.get(fetchNormTrans).json()
print(normalTransactions) 

#information i want 

first_block_number = normalTransactions["result"][0]["blockNumber"]
epoch_timestamp = normalTransactions["result"][0]["blockNumber"]
print(first_block_number)
#print(normalTransactions['result'][1].blockNumber)


def epoch_to_datetime(epoch_timestamp):
    # Convert the epoch timestamp to a datetime object
    datetime_obj = datetime.fromtimestamp(epoch_timestamp)
    # Format the datetime object into a readable string
    formatted_datetime = datetime_obj.strftime('%Y-%m-%d %H:%M:%S')
    
    return formatted_datetime

# Example usage:
epoch_time = 1714243523
#print(convert_epoch_to_datetime(epoch_time))

def credit_or_debit(from_address, to_address):
    if (from_address == test_address and to_address != test_address):
        transactionType = "credit"
    if (from_address != test_address and to_address == test_address):
        transactionType = "debit"
    if (from_address == test_address and to_address == test_address):
        transactionType = "void"
    
    return transactionType
    

def convert_to_eth(value):
    weiBalance = float(value) / 1000000000000000000
    ethBalance = "%.7f" % weiBalance

    return weiBalance


extracted_info = []
# Loop over each transaction in the result list
for transaction in normalTransactions["result"]:
    # Extract the relevant information and store it in a dictionary
    transaction_info = {
        "transactionIndex": transaction["transactionIndex"],
        "hash": transaction["hash"],
        "timeStamp": epoch_to_datetime(int(transaction["timeStamp"])),
        "from": transaction["from"],
        "to": transaction["to"],
        "transactionType": credit_or_debit(transaction["from"], transaction["to"]),
        "value": convert_to_eth(transaction["value"]),
        "gasPrice": convert_to_eth(transaction["gasPrice"])
    }
    
    # Append the dictionary to the extracted_info list
    extracted_info.append(transaction_info)

# Print the resulting list of dictionaries
for info in extracted_info:
    print(info)

# print gas price from an index
# print(extracted_info[0]["gasPrice"])
