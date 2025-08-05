from web3 import Web3
from web3.exceptions import InvalidAddress, ContractLogicError
from contract_abi import ABI

provider_url = "https://base.lava.build" # bizi otomatik olarak en düşük pingli yere yönlendiren lava nın rpc adresi ip analizine gerek yok kendi bilgisayarından çalıştırabilirsin
private_key = "" # hacklenen cüzdanının private keyi
clean_wallet_address = "" #çekmek istediğin temiz cüzdanın adresi

allocation = 0 #kaç miktar claim ettiysen küsüratsız olarak yaz mesela 78.5 ise 78 yaz  

# Web3 setup
web3 = Web3(Web3.HTTPProvider(provider_url))
account = web3.eth.account.from_key(private_key)
token_contract_address = "0xE0Cd4cAcDdcBF4f36e845407CE53E87717b6601d"
token_contract = web3.eth.contract(address=web3.to_checksum_address(token_contract_address), abi=ABI)

# Aşağıdaki linke tıkla son işlemlerden birinin transaction hashini kopyala gas ve gas price için referans
# https://basescan.org/advanced-filter?tkn=0xE0Cd4cAcDdcBF4f36e845407CE53E87717b6601d&txntype=2&mtd=0xa9059cbb%7eTransfer
txn_hash = ""

transaction = web3.eth.get_transaction(txn_hash)
transaction_receipt = web3.eth.get_transaction_receipt(txn_hash)
amount = web3.to_wei(allocation, 'ether')
nonce = web3.eth.get_transaction_count(account.address)
nonce += 1
def sendmoz():
    try:
        tx = token_contract.functions.transfer(
        web3.to_checksum_address(clean_wallet_address),
        amount
    ).build_transaction({
        'chainId': 8453,  # Arbitrum One chain ID
        'gas': int(transaction_receipt['gasUsed']*1.6),     # agresif normalin 2 katı kadar fee 
        'gasPrice': transaction['gasPrice']*2,
        'nonce': nonce,
    })
        signed_tx = web3.eth.account.sign_transaction(tx, private_key)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        return receipt.transactionHash.hex()
    except Exception as e:
        raise

if __name__ == "__main__":
    while 1:
        try:
            sendmoz()
            break
        except Exception as e:
            with open("error.txt", "a") as file:
                file.write(str(e) + "\n")
      

      
