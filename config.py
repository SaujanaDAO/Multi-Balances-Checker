RPC_URL = "https://optimism.publicnode.com"  # Bisa diganti sesuai chain yang digunakan

TOKEN_ADDRESS = "0x4200000000000000000000000000000000000042"  # Ganti dengan SC token yang ingin dicek
TOKEN_DECIMALS = 18  # Sesuaikan dengan desimal token (biasanya 18)

# Nama chain yang sedang digunakan (harus sesuai dengan CoinGecko) sedangkan Mapping di bawah hanya yang sempat kami input
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

# Tambahkan hingga 1000 wallet juga boleh
WALLET_ADDRESSES = [
"wallet1", 
"wallet2", 
"dst", 
] 

