import requests
import mysql.connector
import json
from datetime import datetime

# Configuration
API_KEY = "AIzaSyCSpe59Y_UY0QBtF1CIfEModCgkCkasB4A"  # API Key for Google PageSpeed
#target URL
URLS = [
    "https://www.google.com",
    "https://news.google.com",
    "https://www.bing.com",
    "https://search.yahoo.com",
    "https://www.duckduckgo.com",
    "https://www.ecosia.org",
    "https://www.qwant.com",
    "https://www.startpage.com",
    "https://yandex.com",
    "https://www.baidu.com"
]

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Mansi@113",
    "database": "seo_metrics"
}

# Fetch SEO Data from Google PageSpeed
def get_seo_data(url):
    api_url = f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={url}&key={API_KEY}"
    response = requests.get(api_url)
    data = response.json()
    
    # Extract Key Metrics Safely
    lighthouse_result = data.get("lighthouseResult", {}).get("categories", {})

    metrics = {
        "url": url,
        "performance": lighthouse_result.get("performance", {}).get("score", 0) * 100,
        "accessibility": lighthouse_result.get("accessibility", {}).get("score", 0) * 100,
        "best_practices": lighthouse_result.get("best-practices", {}).get("score", 0) * 100,
        "seo": lighthouse_result.get("seo", {}).get("score", 0) * 100,
        "timestamp": datetime.now()
    }
    return metrics

# Store Data in MySQL
def store_data_in_mysql(metrics):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    # Create Table if not Exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS seo_data (
            id INT AUTO_INCREMENT PRIMARY KEY,
            url VARCHAR(255),
            performance FLOAT,
            accessibility FLOAT,
            best_practices FLOAT,
            seo FLOAT,
            timestamp DATETIME
        )
    """)
    
    # Insert Data
    cursor.execute("""
        INSERT INTO seo_data (url, performance, accessibility, best_practices, seo, timestamp)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (metrics["url"], metrics["performance"], metrics["accessibility"], 
          metrics["best_practices"], metrics["seo"], metrics["timestamp"]))

    conn.commit()
    cursor.close()
    conn.close()

# Main Execution: Process Multiple URLs
if __name__ == "__main__":
    for url in URLS:
        print(f"Fetching SEO data for: {url}")
        seo_metrics = get_seo_data(url)
        store_data_in_mysql(seo_metrics)
        print(f"SEO Metrics stored for: {url}\n")

    print("All URLs processed successfully!")
