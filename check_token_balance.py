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

