from web3 import Web3
from web3.exceptions import InvalidAddress, ContractLogicError

provider_url = "https://base.lava.build" # bizi otomatik olarak en düşük pingli yere yönlendiren lava nın rpc adresi ip analizine gerek yok kendi bilgisayarından çalıştırabilirsin
private_key = "" #Claim edilebilir cüzdanının private keyi
contract_address = "0x3E10685609C34eFf6DC2c0F85d2A3122294AC5ae"

# Web3 setup
web3 = Web3(Web3.HTTPProvider(provider_url))
account = web3.eth.account.from_key(private_key)
contract_address = web3.to_checksum_address(contract_address)

# Metamask ile claime butonuna bastığında çıkan hex datayı yapıştır buraya aşağu yukarı bu şekilde bir data çıkacak onu kopyala yapıştır
# temsili şu şekil olacak 0xe3f8c3920000000000000000000000000000000000000000000000000000000000000002
data =  ""

#Aşağıdaki linki aç son işlemlerden birinin transaction hashi ni kopyala ve aşağıya yapıştır gas ve gas price için referans olacak
#https://basescan.org/address/0x3e10685609c34eff6dc2c0f85d2a3122294ac5ae
txn_hash = ""

transaction = web3.eth.get_transaction(txn_hash)
transaction_receipt = web3.eth.get_transaction_receipt(txn_hash)
nonce = web3.eth.get_transaction_count(account.address)
def claim():
    try:
        tx = {  
            'from': account.address,
            'chainId': 8453,
            'to': contract_address,
            'nonce': nonce,
            'gas': transaction_receipt['gasUsed']*2, #işlemizin öne alınması için agresif gas ve gas price
            'gasPrice': int(transaction['gasPrice']*2),
            'data': data
        }
        signed_tx = web3.eth.account.sign_transaction(tx, private_key)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        return receipt.transactionHash.hex()
    except Exception as e:
        raise

if __name__ == "__main__":
    while 1:
        try:
            claim()
            break
        except Exception as e:
            with open("error.txt", "a") as file:
                file.write(str(e) + "\n")
      