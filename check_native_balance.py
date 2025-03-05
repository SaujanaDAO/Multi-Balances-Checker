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

