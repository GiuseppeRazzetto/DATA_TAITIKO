import os
import json
import gspread
from google.oauth2 import service_account

# Cargar el JSON desde la variable de entorno
creds_json = os.environ.get("GOOGLE_CREDS_JSON")
creds_dict = json.loads(creds_json)

# Crear las credenciales a partir del diccionario
creds = service_account.Credentials.from_service_account_info(
    creds_dict,
    scopes=["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
)

client = gspread.authorize(creds)
sheet = client.open("PRECIO_TTG").sheet1

headers = [
    "timestamp", "price_usd", "price_native",
    "volume_h24", "volume_h6", "volume_h1", "volume_m5",
    "buys_h24", "sells_h24", "buys_h6", "sells_h6",
    "price_change_h1", "price_change_h6", "price_change_h24",
    "liquidity_usd", "liquidity_base", "liquidity_quote",
    "fdv", "market_cap"
]

def fetch_ttg_data():
    url = "https://api.dexscreener.com/latest/dex/pairs/solana/DrgGbUa6SMEDeY2YbwgfoKKNx5rLRG5kNkNgunxzp4G3"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()["pair"]
    
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "price_usd": float(data["priceUsd"]),
        "price_native": float(data["priceNative"]),
        "volume_h24": float(data["volume"]["h24"]),
        "volume_h6": float(data["volume"]["h6"]),
        "volume_h1": float(data["volume"]["h1"]),
        "volume_m5": float(data["volume"]["m5"]),
        "buys_h24": data["txns"]["h24"]["buys"],
        "sells_h24": data["txns"]["h24"]["sells"],
        "buys_h6": data["txns"]["h6"]["buys"],
        "sells_h6": data["txns"]["h6"]["sells"],
        "price_change_h1": float(data["priceChange"]["h1"]),
        "price_change_h6": float(data["priceChange"]["h6"]),
        "price_change_h24": float(data["priceChange"]["h24"]),
        "liquidity_usd": float(data["liquidity"]["usd"]),
        "liquidity_base": float(data["liquidity"]["base"]),
        "liquidity_quote": float(data["liquidity"]["quote"]),
        "fdv": float(data["fdv"]),
        "market_cap": float(data["marketCap"]),
    }

# Bucle 24/7 con intervalo de 30 segundos
print("⏳ Iniciando monitoreo continuo...")
while True:
    try:
        data = fetch_ttg_data()
        row = [data[h] for h in headers]
        sheet.append_row(row)
        print(f"✅ Guardado: {data['timestamp']}")
        time.sleep(30)
    except Exception as e:
        print(f"⚠️ Error: {e}")
        time.sleep(10)

