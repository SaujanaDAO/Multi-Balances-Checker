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
nano check_token_balance.py
```

