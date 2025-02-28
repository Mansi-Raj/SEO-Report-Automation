import pandas as pd
import matplotlib.pyplot as plt
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
import os
import shutil
from datetime import datetime
from sqlalchemy import create_engine, exc
import urllib.parse

# Create report directory structure
current_date = datetime.now()
month_year = current_date.strftime("%B-%Y")  # Format: "Month-Year"
report_dir = os.path.join(os.getcwd(), "report", month_year)  # Ensures it runs from any directory
os.makedirs(report_dir, exist_ok=True)

# Database connection using SQLAlchemy
try:
    password = urllib.parse.quote("Mansi@113")  # Encodes special characters
    engine = create_engine(f"mysql+mysqlconnector://root:{password}@localhost/seo_metrics")
    with engine.connect() as conn:
        query = """
        SELECT url, performance, accessibility, best_practices, seo, timestamp 
        FROM seo_data 
        WHERE timestamp >= DATE_SUB(CURDATE(), INTERVAL 1 MONTH) 
        AND DAYOFWEEK(timestamp) = 2  -- Only Mondays
        AND HOUR(timestamp) = 12
        """
        df = pd.read_sql(query, conn)
except exc.SQLAlchemyError as e:
    print(f" Database connection failed: {e}")
    exit()

# Check if DataFrame is empty
if df.empty:
    print("No SEO data available for the selected period. Report not generated.")
    exit()

# Convert timestamp to datetime
df["timestamp"] = pd.to_datetime(df["timestamp"])
df["date"] = df["timestamp"].dt.date

#  Aggregate daily averages
daily_avg = df.groupby("date").agg({
    "performance": "mean",
    "accessibility": "mean",
    "best_practices": "mean",
    "seo": "mean"
})

# Generate and save plots
figures = []
temp_figures_dir = os.path.join(report_dir, "temp")
os.makedirs(temp_figures_dir, exist_ok=True)

metrics = {
    "Performance Score": "performance",
    "Accessibility Score": "accessibility",
    "Best Practices Score": "best_practices",
    "SEO Score": "seo"
}

for title, col in metrics.items():
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(daily_avg.index, daily_avg[col], marker="o", linestyle="-", color="b")
    ax.set_title(f"Monthly {title} Trends", fontsize=14)
    ax.set_xlabel("Date", fontsize=12)
    ax.set_ylabel(title, fontsize=12)
    ax.grid(True)
    plt.xticks(rotation=45)

    filename = os.path.join(temp_figures_dir, f"{col}.png")
    plt.savefig(filename, bbox_inches="tight")
    figures.append(filename)
    plt.close()

# Generate Multi-Page PDF Report
pdf_filename = os.path.join(report_dir, f"report-{month_year}.pdf")
c = canvas.Canvas(pdf_filename, pagesize=letter)

for idx, img_path in enumerate(figures):
    if idx > 0:
        c.showPage()  
    c.drawImage(ImageReader(img_path), 50, 300, width=500, height=300)
    c.drawString(250, 750, f"Monthly SEO Report - {month_year}")

c.save()

#  Clean up temporary image files
shutil.rmtree(temp_figures_dir)

print(f"PDF Report Generated: {pdf_filename}")
