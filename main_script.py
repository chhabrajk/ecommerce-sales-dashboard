# ============================================================
# E-Commerce Sales Analytics Dashboard
# Author: Jagdish Chhabra | github.com/jagdish-chhabra
# Stack: Python, Pandas, Plotly, Dash
# Dataset: Simulated E-Commerce Orders (Olist-style structure)
# ============================================================

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash import Dash, dcc, html, Input, Output
import os
import warnings
warnings.filterwarnings("ignore")

os.makedirs("screenshots", exist_ok=True)
os.makedirs("output", exist_ok=True)

# ── 1. GENERATE REALISTIC SAMPLE DATA ───────────────────────
np.random.seed(42)
n = 2000

categories   = ["Electronics", "Clothing", "Home & Kitchen", "Sports", "Books", "Beauty"]
regions      = ["North", "South", "East", "West", "Central"]
statuses     = ["Delivered", "Shipped", "Cancelled", "Returned"]
status_probs = [0.75, 0.12, 0.08, 0.05]

dates = pd.date_range("2023-01-01", "2024-12-31", periods=n)

df = pd.DataFrame({
    "order_id"      : range(1, n + 1),
    "order_date"    : dates,
    "category"      : np.random.choice(categories, n),
    "region"        : np.random.choice(regions, n),
    "quantity"      : np.random.randint(1, 6, n),
    "unit_price"    : np.round(np.random.uniform(10, 500, n), 2),
    "discount_pct"  : np.random.choice([0, 5, 10, 15, 20], n, p=[0.4, 0.2, 0.2, 0.1, 0.1]),
    "status"        : np.random.choice(statuses, n, p=status_probs),
    "customer_id"   : np.random.randint(1, 400, n),
})

df["revenue"]      = df["quantity"] * df["unit_price"] * (1 - df["discount_pct"] / 100)
df["month"]        = df["order_date"].dt.to_period("M").astype(str)
df["month_dt"]     = pd.to_datetime(df["month"])
df["year"]         = df["order_date"].dt.year

# ── 2. KPI CALCULATIONS ─────────────────────────────────────
def calc_kpis(data):
    delivered = data[data["status"] == "Delivered"]
    return {
        "total_revenue"   : delivered["revenue"].sum(),
        "total_orders"    : len(data),
        "avg_order_value" : delivered["revenue"].mean(),
        "cancellation_rt" : len(data[data["status"] == "Cancelled"]) / len(data) * 100,
        "unique_customers": data["customer_id"].nunique(),
    }

# ── 3. DASH APP ──────────────────────────────────────────────
app = Dash(__name__)

app.layout = html.Div([

    # ── Header
    html.Div([
        html.H1("📦 E-Commerce Sales Dashboard", style={"color": "#fff", "margin": 0}),
        html.P("Interactive analytics powered by Python + Plotly Dash",
               style={"color": "#ccc", "margin": 0}),
    ], style={"background": "#1a1a2e", "padding": "20px 30px"}),

    # ── Filters
    html.Div([
        html.Div([
            html.Label("Year", style={"fontWeight": "bold"}),
            dcc.Dropdown(
                id="year-filter",
                options=[{"label": str(y), "value": y} for y in sorted(df["year"].unique())],
                value=None, placeholder="All Years", clearable=True
            ),
        ], style={"width": "200px"}),
        html.Div([
            html.Label("Category", style={"fontWeight": "bold"}),
            dcc.Dropdown(
                id="cat-filter",
                options=[{"label": c, "value": c} for c in categories],
                value=None, placeholder="All Categories", clearable=True
            ),
        ], style={"width": "220px"}),
        html.Div([
            html.Label("Region", style={"fontWeight": "bold"}),
            dcc.Dropdown(
                id="reg-filter",
                options=[{"label": r, "value": r} for r in regions],
                value=None, placeholder="All Regions", clearable=True
            ),
        ], style={"width": "200px"}),
    ], style={"display": "flex", "gap": "20px", "padding": "20px 30px",
              "background": "#f8f9fa", "alignItems": "flex-end"}),

    # ── KPI Cards
    html.Div(id="kpi-cards", style={"display": "flex", "gap": "15px",
                                     "padding": "20px 30px", "flexWrap": "wrap"}),

    # ── Charts row 1
    html.Div([
        dcc.Graph(id="revenue-trend", style={"flex": "2"}),
        dcc.Graph(id="category-pie",  style={"flex": "1"}),
    ], style={"display": "flex", "gap": "15px", "padding": "0 30px"}),

    # ── Charts row 2
    html.Div([
        dcc.Graph(id="region-bar"),
        dcc.Graph(id="status-bar"),
    ], style={"display": "flex", "gap": "15px", "padding": "15px 30px"}),

], style={"fontFamily": "Segoe UI, sans-serif", "background": "#f0f2f5", "minHeight": "100vh"})


# ── 4. CALLBACKS ─────────────────────────────────────────────
def filter_df(year, cat, reg):
    d = df.copy()
    if year: d = d[d["year"] == year]
    if cat:  d = d[d["category"] == cat]
    if reg:  d = d[d["region"] == reg]
    return d


def kpi_card(title, value, color):
    return html.Div([
        html.P(title, style={"margin": 0, "color": "#666", "fontSize": "13px"}),
        html.H3(value, style={"margin": "5px 0 0", "color": color}),
    ], style={"background": "#fff", "padding": "15px 20px", "borderRadius": "10px",
              "boxShadow": "0 2px 8px rgba(0,0,0,0.08)", "minWidth": "160px",
              "borderTop": f"4px solid {color}"})


@app.callback(
    Output("kpi-cards",      "children"),
    Output("revenue-trend",  "figure"),
    Output("category-pie",   "figure"),
    Output("region-bar",     "figure"),
    Output("status-bar",     "figure"),
    Input("year-filter", "value"),
    Input("cat-filter",  "value"),
    Input("reg-filter",  "value"),
)
def update_dashboard(year, cat, reg):
    d = filter_df(year, cat, reg)
    k = calc_kpis(d)

    # KPI cards
    cards = [
        kpi_card("Total Revenue",      f"${k['total_revenue']:,.0f}",    "#4361ee"),
        kpi_card("Total Orders",        f"{k['total_orders']:,}",          "#3f8600"),
        kpi_card("Avg Order Value",     f"${k['avg_order_value']:,.2f}",  "#7209b7"),
        kpi_card("Cancellation Rate",   f"{k['cancellation_rt']:.1f}%",   "#d62828"),
        kpi_card("Unique Customers",    f"{k['unique_customers']:,}",      "#f4a261"),
    ]

    # Revenue trend
    trend = (d[d["status"] == "Delivered"]
             .groupby("month_dt")["revenue"].sum()
             .reset_index()
             .sort_values("month_dt"))
    fig_trend = px.area(trend, x="month_dt", y="revenue",
                        title="📈 Monthly Revenue Trend",
                        labels={"month_dt": "Month", "revenue": "Revenue ($)"},
                        color_discrete_sequence=["#4361ee"])
    fig_trend.update_layout(plot_bgcolor="#fff", paper_bgcolor="#fff")

    # Category breakdown
    cat_rev = (d[d["status"] == "Delivered"]
               .groupby("category")["revenue"].sum().reset_index())
    fig_pie = px.pie(cat_rev, names="category", values="revenue",
                     title="🍕 Revenue by Category",
                     color_discrete_sequence=px.colors.qualitative.Set3)
    fig_pie.update_layout(paper_bgcolor="#fff")

    # Region performance
    reg_rev = (d[d["status"] == "Delivered"]
               .groupby("region")["revenue"].sum()
               .sort_values(ascending=True).reset_index())
    fig_reg = px.bar(reg_rev, x="revenue", y="region", orientation="h",
                     title="🗺️ Revenue by Region",
                     labels={"revenue": "Revenue ($)", "region": "Region"},
                     color="revenue", color_continuous_scale="Blues")
    fig_reg.update_layout(plot_bgcolor="#fff", paper_bgcolor="#fff", showlegend=False)

    # Order status distribution
    status_cnt = d.groupby("status").size().reset_index(name="count")
    colors = {"Delivered": "#3f8600", "Shipped": "#4361ee",
              "Cancelled": "#d62828", "Returned": "#f4a261"}
    fig_status = px.bar(status_cnt, x="status", y="count",
                        title="📋 Order Status Breakdown",
                        color="status",
                        color_discrete_map=colors,
                        labels={"count": "Orders", "status": "Status"})
    fig_status.update_layout(plot_bgcolor="#fff", paper_bgcolor="#fff", showlegend=False)

    return cards, fig_trend, fig_pie, fig_reg, fig_status


# ── 6. EXPORT STATIC SNAPSHOT FOR GITHUB PAGES ──────────────
def export_static():
    d = df.copy()
    k = calc_kpis(d)

    trend = (d[d["status"] == "Delivered"]
             .groupby("month_dt")["revenue"].sum()
             .reset_index().sort_values("month_dt"))
    cat_rev = (d[d["status"] == "Delivered"]
               .groupby("category")["revenue"].sum().reset_index())
    reg_rev = (d[d["status"] == "Delivered"]
               .groupby("region")["revenue"].sum()
               .sort_values(ascending=True).reset_index())
    status_cnt = d.groupby("status").size().reset_index(name="count")
    colors_map = {"Delivered": "#3f8600", "Shipped": "#4361ee",
                  "Cancelled": "#d62828", "Returned": "#f4a261"}

    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=("Monthly Revenue Trend", "Revenue by Category",
                        "Revenue by Region", "Order Status Breakdown"),
        specs=[[{"type": "xy"}, {"type": "domain"}],
               [{"type": "xy"}, {"type": "xy"}]]
    )
    fig.add_trace(go.Scatter(x=trend["month_dt"], y=trend["revenue"],
                              fill="tozeroy", line=dict(color="#4361ee", width=2),
                              name="Revenue"), row=1, col=1)
    fig.add_trace(go.Pie(labels=cat_rev["category"], values=cat_rev["revenue"],
                          name="Category"), row=1, col=2)
    fig.add_trace(go.Bar(x=reg_rev["revenue"], y=reg_rev["region"],
                          orientation="h", marker_color="#4361ee",
                          name="Region"), row=2, col=1)
    fig.add_trace(go.Bar(x=status_cnt["status"], y=status_cnt["count"],
                          marker_color=[colors_map[s] for s in status_cnt["status"]],
                          name="Status"), row=2, col=2)
    fig.update_layout(
        title="E-Commerce Sales Dashboard — JK Chhabra Analytics Portfolio",
        height=700, template="plotly_white", showlegend=False
    )
    fig.write_html("screenshots/dashboard_snapshot.html")
    fig.write_html("output/dashboard_snapshot.html")
    print("💾 Static snapshot saved: screenshots/dashboard_snapshot.html")

export_static()

# ── 7. ENTRY POINT ───────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True)

