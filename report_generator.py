import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader

# MySQL Connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Mansi@113",
    database="seo_metrics"
)
cursor = conn.cursor()

# Fetch data for the last month
query = """
SELECT url, performance, accessibility, best_practices, seo, timestamp 
FROM seo_data 
WHERE timestamp >= (
    SELECT MIN(timestamp) 
    FROM seo_data 
    WHERE DAYOFWEEK(timestamp) = 2  -- Monday (1 = Sunday, 2 = Monday)
    AND MONTH(timestamp) = MONTH(CURDATE())
    AND YEAR(timestamp) = YEAR(CURDATE())
    AND HOUR(timestamp) = 12
)
"""
df = pd.read_sql(query, conn)
conn.close()

# Convert timestamp to datetime
df["timestamp"] = pd.to_datetime(df["timestamp"])
df["date"] = df["timestamp"].dt.date
daily_avg = df.groupby("date").mean()

# Generate and save plots
figures = []

metrics = {
    "Performance Score": "performance",
    "Accessibility Score": "accessibility",
    "Best Practices Score": "best_practices",
    "SEO Score": "seo"
}


for title, col in metrics.items():
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(daily_avg.index, daily_avg[col], marker="o", linestyle="-")
    ax.set_title(f"Monthly {title} Trends")
    ax.set_xlabel("Date")
    ax.set_ylabel(title)
    ax.grid()
    plt.xticks(rotation=45)

    filename = f"{col}.png"
    plt.savefig(filename)
    figures.append(filename)
    plt.close()

# Generate Multi-Page PDF Report
pdf_filename = "monthly_seo_report.pdf"
c = canvas.Canvas(pdf_filename, pagesize=letter)

for idx, img_path in enumerate(figures):
    if idx > 0:
        c.showPage()  
    c.drawImage(ImageReader(img_path), 50, 300, width=500, height=300)  # image configuration
    c.drawString(250, 750, "Monthly SEO Report")  # Title on each page

c.save()
print(f"PDF Report Generated: {pdf_filename}")
