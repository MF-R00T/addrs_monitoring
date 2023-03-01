import requests
import smtplib
import time

# Prompt the user for the cryptocurrency address and email
address = input("Enter the address to track: ")
email = input("Enter the email to send results to: ")

# Flag to keep track of whether to keep updating or not
keep_updating = True

# Function to get the current balance of the address for Ethereum
def get_eth_balance(address):
    etherscan_api_key = "your_etherscan_api_key_here"
    etherscan_endpoint = f"https://api.etherscan.io/api?module=account&action=balance&address={address}&apikey={etherscan_api_key}"
    response = requests.get(etherscan_endpoint)
    if response.status_code == 200:
        balance = int(response.json()["result"]) / 10**18  # convert wei to ether
        return balance
    else:
        return None

# Function to get the list of recent transactions for the address for Ethereum
def get_eth_transactions(address):
    etherscan_api_key = "your_etherscan_api_key_here"
    etherscan_endpoint = f"https://api.etherscan.io/api?module=account&action=txlist&address={address}&sort=desc&apikey={etherscan_api_key}"
    response = requests.get(etherscan_endpoint)
    if response.status_code == 200:
        transactions = response.json()["result"]
        return transactions
    else:
        return None

# Function to get the current balance of the address for Bitcoin
def get_btc_balance(address):
    blockchain_api_key = "your_blockchain_api_key_here"
    blockchain_endpoint = f"https://blockchain.info/rawaddr/{address}?api_code={blockchain_api_key}"
    response = requests.get(blockchain_endpoint)
    if response.status_code == 200:
        balance = response.json()["final_balance"] / 10**8  # convert satoshis to BTC
        return balance
    else:
        return None

# Function to get the list of recent transactions for the address for Bitcoin
def get_btc_transactions(address):
    blockchain_api_key = "your_blockchain_api_key_here"
    blockchain_endpoint = f"https://blockchain.info/rawaddr/{address}?api_code={blockchain_api_key}"
    response = requests.get(blockchain_endpoint)
    if response.status_code == 200:
        transactions = response.json()["txs"]
        return transactions
    else:
        return None

# Function to get the current balance of the address for TRON
def get_tron_balance(address):
    tronscan_endpoint = f"https://apilist.tronscan.org/api/account?address={address}"
    response = requests.get(tronscan_endpoint)
    if response.status_code == 200:
        balance = response.json()["balance"] / 10**6  # convert SUN to TRX
        return balance
    else:
        return None

# Function to get the list of recent transactions for the address for TRON
def get_tron_transactions(address):
    tronscan_endpoint = f"https://apilist.tronscan.org/api/transaction?limit=100&sort=-timestamp&start=0&address={address}"
    response = requests.get(tronscan_endpoint)
    if response.status_code == 200:
        transactions = response.json()["data"]
        return transactions
    else:
        return None

# Function to send an email with the results
def send_email(email, subject, body):
    gmail_address = "your_gmail_address_here"
    gmail_password = "your_gmail_password_here"
    recipient = email

def main():
    # Prompt user for crypto address and email address
    address = input("Enter your cryptocurrency address: ")
    email = input("Enter your email address: ")

    # Prompt user for end date for updates
    end_date_str = input("Enter the end date for updates (YYYY-MM-DD): ")
    end_date = datetime.datetime.strptime(end_date_str, "%Y-%m-%d")

    # Create a list of blockchain APIs to check
    blockchains = [
        ("Ethereum", "https://api.etherscan.io/api"),
        ("Bitcoin", "https://blockchain.info/rawaddr"),
        ("Tron", "https://apilist.tronscan.org/api/account")
    ]

    # Continuously check for updates until end date is reached or user cancels
    global keep_updating
    keep_updating = True
    while keep_updating and datetime.datetime.now() < end_date:
        for blockchain in blockchains:
            name, url = blockchain
            try:
                # Check for deposits and withdrawals using the API
                transactions = get_transactions(url, address)
                new_deposits, new_withdrawals = get_new_transactions(transactions, name)
                # If there are new deposits or withdrawals, send an email to the user
                if new_deposits or new_withdrawals:
                    send_email(email, name, new_deposits, new_withdrawals)
            except Exception as e:
                print(f"Failed to get transactions for {name}: {e}")
        time.sleep(60)
