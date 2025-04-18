import requests
import csv
import os
import time
from datetime import datetime

filename = "ttg_historical_data.csv"

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

def save_data_to_csv(data, filename):
    file_exists = os.path.isfile(filename)
    with open(filename, mode="a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)

# Bucle infinito para guardar cada minuto
print("⏳ Iniciando recolección de datos cada minuto...")
while True:
    try:
        data = fetch_ttg_data()
        save_data_to_csv(data, filename)
        print(f"✅ Datos guardados: {data['timestamp']}")
        time.sleep(45)  # Esperar 60 segundos
    except Exception as e:
        print(f"⚠️ Error: {e}")
        time.sleep(10)  # Esperar menos si falla, para reintentar rápido
