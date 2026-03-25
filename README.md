# 📦 E-Commerce Sales Dashboard

> **Repo name:** `ecommerce-sales-dashboard`
> **Description:** Interactive Python dashboard analyzing e-commerce sales by category, region & time — built with Plotly Dash.

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=flat-square&logo=plotly&logoColor=white)
![Dash](https://img.shields.io/badge/Dash-00ADD8?style=flat-square)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat-square&logo=pandas&logoColor=white)

> 🚀 **[Live Demo →](https://chhabrajk.github.io/ecommerce-sales-dashboard/)**

---

## 🎯 Business Problem

E-commerce managers need real-time visibility into sales performance across categories,
regions, and time periods — but raw order data sitting in spreadsheets makes it
impossible to spot trends quickly.

**This dashboard solves that.** Drop in your order data and get an interactive,
filterable analytics suite in seconds.

---

## 📊 What It Does

- Tracks **Total Revenue, Orders, AOV, Cancellation Rate, Unique Customers**
- Interactive **filters** by Year, Category, and Region
- **Monthly revenue trend** with area chart
- **Category breakdown** via pie chart
- **Regional performance** via horizontal bar chart
- **Order status distribution** (Delivered / Shipped / Cancelled / Returned)

---

## 🖼️ Dashboard Preview

> 📸 **Add screenshots here after running locally.**
> Drag & drop images into this README on GitHub, or place them in a `/screenshots` folder.

| KPI Cards | Revenue Trend | Category Breakdown |
|-----------|--------------|-------------------|
| ![KPI](screenshots/kpi_cards.png) | ![Trend](screenshots/revenue_trend.png) | ![Pie](screenshots/category_pie.png) |

> 🌐 **[Open Live Dashboard →](https://chhabrajk.github.io/ecommerce-sales-dashboard/)**

---

## 🚀 Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/chhabrajk/ecommerce-sales-dashboard.git
cd ecommerce-sales-dashboard

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the dashboard
python main_script.py

# 4. Open in browser
# → http://127.0.0.1:8050

# 5. To generate a static HTML demo for GitHub Pages:
#    In ecommerce_dashboard.py, add at the end:
#    app.layout  (save as demo.html using plotly's write_html)
#    Then upload demo.html to this repo root
```

---

## 📁 Repo Structure

```
ecommerce-sales-dashboard/
├── main_script.py
├── requirements.txt
├── index.html           ← GitHub Pages demo
├── screenshots/
│   └── dashboard_snapshot.html
├── output/
│   └── dashboard_snapshot.html
└── README.md
```

---

## 🧰 Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.9+ | Core language |
| Pandas | Data manipulation |
| Plotly | Charts & visualizations |
| Dash | Web dashboard framework |
| NumPy | Data simulation & math |

---

## 📦 Requirements

```txt
dash==2.17.0
plotly==5.22.0
pandas==2.2.2
numpy==1.26.4
```

---

## 💡 Key Insights This Dashboard Reveals

- Which product categories drive the most revenue
- Which regions are underperforming vs target
- Seasonal revenue patterns month-over-month
- Cancellation rate trends that signal fulfilment issues

---

## 👤 Author

**JK Chhabra** — Senior Data Analytics Consultant
- 🌐 [GitHub](https://github.com/chhabrajk)
- 💼 [Upwork](#)
- 📧 jsinfo618@gmail.com

---

*Part of the [Analytics Portfolio](https://github.com/chhabrajk) — 6 end-to-end data projects covering BI, ML, forecasting, ETL, finance, and marketing analytics.*