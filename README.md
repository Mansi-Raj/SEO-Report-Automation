# Automated SEO Report Generator

## 📌 Overview

The **Automated SEO Report Generator** is a Python-based tool that fetches SEO performance metrics from a MySQL database, generates visual trend analysis, and compiles them into a **multi-page PDF report**. The reports are automatically generated on **Mondays at 12 PM** and include key metrics like **Performance Score, Accessibility Score, Best Practices Score, and SEO Score**.

---

## 🚀 Features

- **Automated Data Retrieval**: Fetches SEO data from a MySQL database.
- **Dynamic Report Generation**: Generates reports for the **last month**.
- **Data Visualization**: Uses **Matplotlib** to create clear, insightful trend graphs.
- **Multi-Page PDF Export**: Generates and saves reports in a structured PDF format.
- **Automated Cleanup**: Deletes temporary files after report generation.
- **Error Handling**: Gracefully handles database connection failures and missing data.

---

## 🛠️ Technologies Used

- **Python** (Primary Language)
- **Pandas** (Data Handling & Processing)
- **Matplotlib** (Data Visualization)
- **SQLAlchemy** (Database Connection)
- **MySQL** (Database Storage)
- **ReportLab** (PDF Generation)
- **OS & shutil** (File Management)

---

## 🌐 APIs Used

**Google PageSpeed Insights API**: Fetches website performance, accessibility, best practices, and SEO scores.

**API Documentation**: Google PageSpeed Insights

---

## 📂 Project Structure

```
📁 Automated-SEO-Report-Generator
│── 📁 report/               # Stores generated reports
│── 📁 report/month-year/    # Stores reports for a specific month
│── 📄 seo_report.py         # Main script for generating reports
│── 📄 README.md             # Project documentation
```

---

## 🔧 Installation & Setup

### **1️⃣ Clone the Repository**

```bash
git clone https://github.com/yourusername/seo-report-generator.git
cd seo-report-generator
```

### **2️⃣ Install Dependencies**

Make sure you have **Python 3.x** installed, then run:

```bash
pip install pandas matplotlib reportlab sqlalchemy mysql-connector-python
```

### **3️⃣ Configure MySQL Database**

Ensure you have a MySQL server running and update the database credentials in `seo_report.py`:

```python
engine = create_engine("mysql+mysqlconnector://root:yourpassword@localhost/seo_metrics")
```

### **4️⃣ Run the Script**

To generate the SEO report manually, run:

```bash
python seo_report.py
```

---

## 📊 Example Report

A sample of the generated PDF report includes:
✅ **Performance Trends**  
✅ **SEO Score Evolution**  
✅ **Best Practices Insights**  
✅ **Accessibility Score Tracking**

---

### 🔹 Happy Coding! 🚀
