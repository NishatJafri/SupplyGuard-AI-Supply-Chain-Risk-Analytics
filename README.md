# SupplyGuard-AI-Supply-Chain-Risk-Analytics
SupplyGuard AI is an interactive supply chain risk analytics application built with Python, Pandas, and Streamlit. It analyzes supply chain data to identify delivery delays, product performance patterns, regional risks, and operational insights, with AI-assisted analysis to support data-driven decision-making.
# 🛡️ SupplyGuard AI
## Supply Chain Analytics & Risk Intelligence Dashboard

> An interactive, end-to-end supply chain analytics web application built with **Streamlit** and **Python**.  
> Transforms 180,519 raw order records into actionable intelligence across sales, delivery, product, risk, and fraud domains.

---

## 📌 Project Overview

**SupplyGuard AI** is a data analytics dashboard developed as part of the IBM SkillsBuild Data Analytics with AI Internship programme. The project follows a complete data analytics pipeline — from raw data cleaning through exploration, domain analysis, risk detection, and AI-driven insights — all presented in a clean, readable, single-page Streamlit application.

| Attribute         | Detail                                               |
|-------------------|------------------------------------------------------|
| **Project Name**  | SupplyGuard AI                                       |
| **Full Title**    | Supply Chain Analytics & Risk Intelligence Dashboard |
| **Domain**        | Supply Chain / Business Analytics                    |
| **Dataset**       | DataCo Supply Chain Dataset                          |
| **Records**       | 180,519 order-level rows · 62 features               |
| **Time Period**   | 2015 – 2018                                          |
| **Markets**       | Europe, USCA, LATAM, Pacific Asia, Africa            |
| **Tech Stack**    | Python · Streamlit · Pandas · NumPy · Matplotlib     |

---

## 📊 Dataset Summary

| Metric                | Value            |
|-----------------------|-----------------|
| Total Records         | 180,519          |
| Features              | 62               |
| Unique Orders         | 65,752           |
| Unique Products       | 118              |
| Product Categories    | 50               |
| Countries Covered     | 164              |
| Departments           | 11               |
| Years Covered         | 2015, 2016, 2017, 2018 |

**Key Columns Used:**  
`order_id`, `order_date`, `sales`, `order_profit`, `profit_margin_pct`, `delivery_status`, `is_delayed`, `shipping_delay_days`, `shipping_mode`, `market`, `order_region`, `customer_segment`, `department_name`, `category_name`, `product_name`, `is_fraud_flagged`, `fraud_risk_score`, `is_loss_order`, `revenue_at_risk`, `payment_type`, `order_status`, `is_transfer_payment`

---

## 🗂️ Application Structure

The app is divided into **6 sidebar sections**, each covering a stage of the analytics pipeline:

```
🛡️ SupplyGuard AI
│
├── 🏠 Overview & Data
│   ├── KPI Dashboard (8 key metrics)
│   ├── Annual Revenue & Profit Charts
│   ├── 🗃️ Cleaned Dataset (dtypes, nulls, sample)
│   └── 🔬 Data Exploration (stats, distributions, patterns)
│
├── 🚛 Delivery & Shipping
│   ├── KPIs: On-Time, Late Rate, Avg Delay, Cancellations
│   ├── Delay Overview (by segment, status)
│   ├── Shipping Mode Analysis
│   ├── Market & Region Analysis
│   └── Monthly Trend Charts
│
├── 💹 Sales & Profit
│   ├── KPIs: Revenue, Profit, Margin, Discount
│   ├── Yearly Trends (revenue + profit)
│   ├── Customer Segment Analysis
│   ├── Market & Region Analysis
│   └── Discount Impact Analysis
│
├── 🗂️ Product Analysis
│   ├── KPIs: Products, Categories, Departments
│   ├── Top 10 Products by Revenue & Profit
│   ├── Department & Category Performance
│   └── Loss Leaders & High-Risk Products
│
├── 🔍 Risk & Anomaly
│   ├── KPIs: Fraud Orders, Loss Orders, Revenue at Risk
│   ├── Fraud Analysis (by payment, market, score)
│   ├── Loss Order Trends
│   └── Revenue at Risk by Market & Shipping Mode
│
└── 🧠 AI Insights
    ├── 8 Data-Driven Insight Cards
    ├── Summary Scorecard Table
    └── Business Health Metrics Bar Chart
```

---

## 🔑 Key Findings

| Finding                         | Value / Detail                                      |
|---------------------------------|-----------------------------------------------------|
| Total Revenue                   | $36.78M                                             |
| Total Profit                    | $3.97M                                              |
| Average Profit Margin           | 10.83%                                              |
| **Late Delivery Rate**          | **57.28%** — critical operational issue             |
| On-Time Delivery Rate           | 17.84%                                              |
| Average Delay (when late)       | 1.62 days                                           |
| Cancelled Shipments             | 4.30%                                               |
| **Loss-Making Orders**          | **33,784 (18.71%)** — 1 in 5 orders at a loss       |
| **Fraud-Flagged Orders**        | **4,062** orders                                    |
| Revenue at Risk                 | $3.88M                                              |
| Top Revenue Market              | Europe                                              |
| Highest Delay Market            | Europe                                              |
| Most Delay-Prone Shipping Mode  | First Class                                         |
| Best Performing Department      | Fan Shop                                            |
| Worst Performing Department     | Book Shop                                           |
| Top Customer Segment            | Consumer                                            |
| Highest Fraud Payment Type      | TRANSFER                                            |
| Top Revenue Product             | Field & Stream Sportsman 16 Gun Fire Safe           |
| Discount–Margin Correlation     | −0.023 (negative relationship)                      |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9 or higher
- `pip` package manager

### Installation

```bash
# 1. Clone or download the project
git clone https://github.com/your-username/supplyguard-ai.git
cd supplyguard-ai

# 2. (Optional) Create a virtual environment
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS / Linux

# 3. Install dependencies
pip install -r requirements.txt
```

### Running the App

```bash
streamlit run app.py
```

The app will open automatically at `http://localhost:8501`

### Project Files

```
supplyguard-ai/
├── app.py                        # Main Streamlit application
├── supply_chain_cleaned.csv      # Cleaned dataset (required)
├── DataCoSupplyChainDataset.csv  # Original raw dataset
├── requirements.txt              # Python dependencies
├── README.md                     # This file
└── project_report.docx           # Full project report
```

---

## 📦 Dependencies

| Package       | Version   | Purpose                          |
|---------------|-----------|----------------------------------|
| `streamlit`   | ≥ 1.32.0  | Web application framework        |
| `pandas`      | ≥ 2.0.0   | Data loading, wrangling, aggregation |
| `numpy`       | ≥ 1.26.0  | Numerical computations           |
| `matplotlib`  | ≥ 3.8.0   | All charts and visualisations    |

---

## 🎨 UI Design

- **Theme:** Clean white background with blue accent (`#2563eb`)
- **KPI Cards:** Colour-coded by metric type (blue, teal, green, amber, red, rose)
- **Charts:** Full colour palette — each category gets a distinct colour
- **Insight Boxes:** Left-border accent cards, unique colour per insight topic
- **Layout:** Wide layout, sidebar navigation, tabbed sub-sections
- **Typography:** Segoe UI system font, consistent heading hierarchy

---

## 🧠 Analytics Pipeline

```
Raw Data (DataCoSupplyChainDataset.csv)
        ↓
Data Cleaning & Feature Engineering
        ↓
supply_chain_cleaned.csv  ←── App reads this file
        ↓
┌─────────────────────────────────────────────────┐
│  1. Overview KPIs  →  Business snapshot          │
│  2. Cleaned Data   →  Data quality validation    │
│  3. Exploration    →  Stats, distributions       │
│  4. Delivery       →  Delay & shipping analysis  │
│  5. Sales & Profit →  Revenue, margin, discount  │
│  6. Products       →  Top/low performers         │
│  7. Risk & Fraud   →  Anomaly detection          │
│  8. AI Insights    →  Narrative findings         │
└─────────────────────────────────────────────────┘
```

---

## 📁 Dataset Features Engineered

The cleaned CSV includes several engineered features beyond the original raw data:

| Feature               | Description                                              |
|-----------------------|----------------------------------------------------------|
| `is_delayed`          | Binary flag: 1 if actual shipping > scheduled days       |
| `shipping_delay_days` | Difference between actual and scheduled shipping days    |
| `fulfillment_days`    | Total days from order to ship                            |
| `is_loss_order`       | Binary flag: 1 if `order_profit` < 0                     |
| `is_fraud_flagged`    | Binary flag: 1 if order shows fraud signals              |
| `fraud_risk_score`    | Composite score 0–4 based on multiple fraud indicators   |
| `revenue_at_risk`     | Revenue exposed to loss from late/cancelled orders       |
| `profit_margin_pct`   | `(order_profit / sales) × 100`                           |
| `discount_impact`     | Discount rate × sales value                              |
| `is_transfer_payment` | Binary flag for TRANSFER payment type                    |
| `order_year/month/quarter` | Temporal decomposition of order_date               |
| `year_month`          | `YYYY-MM` string for trend charts                        |

---

## 👩‍💻 Author
**Nishat Jafri**
**IBM SkillsBuild Data Analytics with AI Internship**  
Project: SupplyGuard AI — Supply Chain Analytics & Risk Intelligence Dashboard  

---

## 📄 License

This project is for academic and educational purposes under the IBM SkillsBuild Internship Programme.  
Dataset: DataCo Smart Supply Chain for Big Data Analysis (publicly available for research use).

