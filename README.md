# multi_balances_checker

### 1 Update & Install Dependencies
```
sudo apt update && sudo apt upgrade -y
```
```
sudo apt install python3 python3-pip -y
```
```
pip install web3 requests
```
```
pip install --upgrade requests urllib3 chardet
```

### 2️⃣ Update & Install Dependencies
```
mkdir multi_balances_checker
cd multi_balances_checker
```
### 3️⃣ Buat & Edit File Konfigurasi
```
nano config.py
```
```
RPC_URL = "https://optimism.publicnode.com"  # Bisa diganti sesuai chain yang digunakan

TOKEN_ADDRESS = "0x4200000000000000000000000000000000000042"  # Ganti dengan SC token yang ingin dicek
TOKEN_DECIMALS = 18  # Sesuaikan dengan desimal token (biasanya 18)

# Nama chain yang sedang digunakan (harus sesuai dengan CoinGecko)
CHAIN_NAME = "optimism"

# Mapping chain ke CoinGecko ID
CHAIN_TO_CG_ID = {
    "ethereum": "ethereum",
    "bsc": "binancecoin",
    "polygon": "matic-network",
    "optimism": "ethereum", 
    "taiko": "ethereum",
    "arbitrum": "ethereum",
    "avalanche": "avalanche-2",
    "fantom": "fantom",
    "base": "ethereum"
}


WALLET_ADDRESSES = [
"wallet1", 
"wallet2", 
"dst", 
] 
    # Tambahkan hingga 1000 wallet juga boleh
```

```
nano check_native_balance.py
```

```
import json
import requests
import time
import csv
from web3 import Web3
from config import RPC_URL, WALLET_ADDRESSES, CHAIN_NAME, CHAIN_TO_CG_ID

CSV_FILENAME = "balances_native.csv"  # Nama file CSV untuk saldo native
CSV_DELIMITER = ";"  # Pakai ";" biar Excel tidak bingung
CSV_ENCODING = "utf-8-sig"

# Pastikan chain tersedia di CoinGecko
if CHAIN_NAME not in CHAIN_TO_CG_ID:
    raise ValueError(f"Chain {CHAIN_NAME} tidak terdaftar di CoinGecko. Periksa config.py!")

# Setup Web3
web3 = Web3(Web3.HTTPProvider(RPC_URL))

NATIVE_TOKENS = {
    "ethereum": "ETH",
    "bsc": "BNB",
    "polygon": "MATIC",
    "optimism": "ETH",
    "arbitrum": "ETH",
    "avalanche": "AVAX",
    "taiko": "ETH",
    "base": "ETH",
}

# Pastikan nama chain sudah diambil dari config
native_token = NATIVE_TOKENS.get(CHAIN_NAME.lower(), "UNKNOWN")

def get_native_price():
    """Mengambil harga native token dari CoinGecko"""
    try:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={CHAIN_TO_CG_ID[CHAIN_NAME]}&vs_currencies=usd"
        response = requests.get(url)
        data = response.json()
        return data[CHAIN_TO_CG_ID[CHAIN_NAME]]["usd"]
    except Exception as e:
        print(f"Error mendapatkan harga: {e}")
        return 0.0

native_price = get_native_price()

def check_balances():
    """Mengecek saldo native token untuk setiap wallet dan menyimpannya dalam CSV."""
    results = []
    try:
        for wallet in WALLET_ADDRESSES:
            try:
                checksum_wallet = Web3.to_checksum_address(wallet)
                balance_wei = web3.eth.get_balance(checksum_wallet)
                balance = web3.from_wei(balance_wei, "ether")
                balance_usd = float(balance) * native_price

                print(f"Wallet: {checksum_wallet} | Balance: {balance:.6f} {native_token} | ${balance_usd:.2f} USD")
                results.append([checksum_wallet, f"{balance:.6f}", native_token, f"${balance_usd:.2f}"])
                
                time.sleep(1)  # Hindari rate limit
            except Exception as e:
                print(f"Error checking wallet {wallet}: {e}")
    except KeyboardInterrupt:
        print("\nScript dihentikan oleh pengguna. Keluar...")
    
    # Simpan ke file CSV
    with open(CSV_FILENAME, "w", newline="", encoding=CSV_ENCODING) as file:
        writer = csv.writer(file, delimiter=CSV_DELIMITER)
        writer.writerow(["Wallet Address", "Balance", "Token", "USD Value"])
        writer.writerows(results)
    
    print(f"Saldo native telah disimpan di {CSV_FILENAME}")

if __name__ == "__main__":
    check_balances()


```

```
nano check_token_balance.py
```
```
from web3 import Web3
import csv
import time
import requests
from config import RPC_URL, TOKEN_ADDRESS, TOKEN_DECIMALS, WALLET_ADDRESSES

CSV_FILENAME = "balances_token.csv"  # Nama file CSV untuk saldo token
CSV_DELIMITER = ";"  # Gunakan ";" agar lebih kompatibel dengan Excel di berbagai lokal
CSV_ENCODING = "utf-8-sig"

# Inisialisasi koneksi ke node blockchain
web3 = Web3(Web3.HTTPProvider(RPC_URL))

# ABI ERC-20 untuk fungsi balanceOf
TOKEN_ABI = [
    {   
        "constant": True,
        "inputs": [{"name": "_owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    }
]

# Inisialisasi kontrak token
contract = web3.eth.contract(address=Web3.to_checksum_address(TOKEN_ADDRESS), abi=TOKEN_ABI)

def check_balances():
    """
    Mengecek saldo token dari setiap wallet dalam daftar WALLET_ADDRESSES.
    """
    results = []
    try:
        for wallet in WALLET_ADDRESSES:
            try:
                checksum_wallet = Web3.to_checksum_address(wallet)
                balance = contract.functions.balanceOf(checksum_wallet).call() / (10 ** TOKEN_DECIMALS)
                print(f"✅ Wallet: {wallet} | Balance: {balance}")
                results.append([wallet, balance])
            except Exception as e:
                print(f"⚠️ Error checking {wallet}: {str(e)}")
                results.append([wallet, "Error"])
            time.sleep(0.5)  # Beri jeda untuk menghindari rate limit

    except KeyboardInterrupt:
        print("\n❌ Program dihentikan oleh pengguna (CTRL + C). Menyimpan hasil sementara...")
    finally:
        save_to_csv(results)

def save_to_csv(data):
    """
    Menyimpan hasil saldo token ke dalam file CSV.
    """
    try:
        with open(CSV_FILENAME, mode="w", newline="", encoding=CSV_ENCODING) as file:
            writer = csv.writer(file, delimiter=CSV_DELIMITER)
            writer.writerow(["Wallet Address", "Balance"])  # Header
            writer.writerows(data)
        print(f"\n✅ Data saldo berhasil disimpan ke {CSV_FILENAME}")
    except Exception as e:
        print(f"\n❌ Gagal menyimpan CSV: {str(e)}")

if __name__ == "__main__":
    print("🔍 Mengecek saldo token...")
    check_balances()


```
