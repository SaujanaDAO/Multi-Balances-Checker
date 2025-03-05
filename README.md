# Multi Balances Checker

### 1️⃣ Update & Install Dependencies
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

### 2️⃣ Install Scripts
```
git clone https://github.com/SaujanaDAO/Multi-Balances-Checker.git
cd Multi-Balances-Checker
```
### 3️⃣ Buat & Edit File Konfigurasi
```
nano config.py
```

### 4️⃣ Run Script
#### Native Balances Checker
```
python3 check_native_balance.py
```
#### Token Balances Checker
```
python3 check_token_balance.py
```

### 5️⃣ Catatan
- Hal-hal yang perlu dirubah-rubah sesuai chain dan kebutuhan ada di file config.py
- Scripts akan menghasilkan file .CSV yang dapat kamu download dan buka di excel
- Scripts ini 100% aman, karna tidak memerlukan Private Key atau Phrase
- Semoga Bermanfaat
- Jangan lupa diskusi dan join di CH dan Grup kami di TG : https://t.me/ZeroDropDAO dan https://t.me/ZeroDropLounge
