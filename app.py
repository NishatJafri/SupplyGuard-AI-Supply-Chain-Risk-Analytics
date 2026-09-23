import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import warnings
warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="SupplyGuard AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# GLOBAL STYLE
# ─────────────────────────────────────────────
st.markdown("""
<style>
html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background-color: #ffffff;
    color: #1a1a1a;
    font-family: 'Segoe UI', sans-serif;
}
[data-testid="stSidebar"] {
    background-color: #f5f5f5;
    border-right: 1px solid #e0e0e0;
}
h1 { font-size: 1.8rem; font-weight: 700; color: #111; border-bottom: 2px solid #2563eb; padding-bottom: 6px; }
h2 { font-size: 1.35rem; font-weight: 600; color: #1e3a5f; margin-top: 1.6rem; }
h3 { font-size: 1.1rem; font-weight: 600; color: #333; margin-top: 1rem; }
.kpi-card {
    background: #f0f4ff;
    border: 1px solid #c7d7f9;
    border-radius: 8px;
    padding: 18px 14px 12px 14px;
    text-align: center;
}
.kpi-label { font-size: 0.78rem; color: #555; text-transform: uppercase; letter-spacing: .05em; }
.kpi-value { font-size: 1.65rem; font-weight: 700; color: #1e3a5f; line-height: 1.2; margin-top: 4px; }
.kpi-sub   { font-size: 0.75rem; color: #888; margin-top: 3px; }
.section-divider { border: none; border-top: 1px solid #e0e0e0; margin: 22px 0; }
.insight-box {
    background: #f0f7ff;
    border-left: 4px solid #2563eb;
    padding: 12px 16px;
    margin-bottom: 10px;
    border-radius: 0 6px 6px 0;
    font-size: 0.9rem;
    line-height: 1.55;
}
.dataframe thead tr th { background-color: #1e3a5f !important; color: #fff !important; }
[data-testid="stSidebar"] .stRadio label { font-size: 0.88rem; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# DATA LOADER
# ─────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("supply_chain_cleaned.csv", low_memory=False)
    df["order_date"]    = pd.to_datetime(df["order_date"],    errors="coerce")
    df["shipping_date"] = pd.to_datetime(df["shipping_date"], errors="coerce")
    return df

df = load_data()

# ─────────────────────────────────────────────
# COLOUR PALETTE
# ─────────────────────────────────────────────
C = {
    "blue":    "#2563eb",
    "indigo":  "#4f46e5",
    "teal":    "#0d9488",
    "green":   "#16a34a",
    "amber":   "#d97706",
    "orange":  "#ea580c",
    "red":     "#dc2626",
    "rose":    "#e11d48",
    "purple":  "#7c3aed",
    "sky":     "#0284c7",
    "lime":    "#65a30d",
    "pink":    "#db2777",
}
PALETTE   = [C["blue"], C["teal"], C["amber"], C["purple"], C["green"], C["rose"], C["sky"], C["orange"], C["indigo"], C["lime"]]
PIE_PAL   = [C["blue"], C["teal"], C["amber"], C["purple"], C["green"], C["rose"]]
NEG_COLOR = "#ef4444"

# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
def fmt_num(n, decimals=0):
    if abs(n) >= 1_000_000:
        return f"${n/1_000_000:.2f}M"
    if abs(n) >= 1_000:
        return f"${n/1_000:.1f}K"
    return f"${n:,.{decimals}f}"

def kpi(label, value, sub="", accent="#2563eb"):
    return f"""
    <div class="kpi-card" style="border-color:{accent}33;background:{accent}0d">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value" style="color:{accent}">{value}</div>
        <div class="kpi-sub">{sub}</div>
    </div>"""

def section_line():
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

def styled_fig(h=3.8):
    fig, ax = plt.subplots(figsize=(7, h))
    fig.patch.set_facecolor("#ffffff")
    ax.set_facecolor("#fafafa")
    ax.tick_params(labelsize=8)
    ax.spines[["top","right"]].set_visible(False)
    return fig, ax

def color_barh(ax, labels, values, colors=None, xlabel=""):
    if colors is None:
        colors = PALETTE[:len(values)]
    bars = ax.barh(labels, values, color=colors, edgecolor="white", linewidth=0.6)
    ax.set_xlabel(xlabel, fontsize=9)
    ax.spines[["top","right"]].set_visible(False)
    ax.tick_params(labelsize=8)
    for bar in bars:
        w = bar.get_width()
        ax.text(w * 1.01 if w >= 0 else w * 0.99,
                bar.get_y() + bar.get_height()/2,
                f"{w:,.1f}", va="center", ha="left" if w >= 0 else "right", fontsize=7.5)
    return ax

def color_bar(ax, labels, values, colors=None, ylabel="", title=""):
    if colors is None:
        colors = PALETTE[:len(values)]
    ax.bar(labels, values, color=colors, edgecolor="white", linewidth=0.6)
    ax.set_ylabel(ylabel, fontsize=9)
    ax.set_title(title, fontsize=10, fontweight="bold", pad=8)
    ax.spines[["top","right"]].set_visible(False)
    ax.tick_params(labelsize=8)
    return ax

# ─────────────────────────────────────────────
# SIDEBAR NAVIGATION
# ─────────────────────────────────────────────
st.sidebar.markdown("## 🛡️ SupplyGuard AI")
st.sidebar.markdown("---")
section = st.sidebar.radio(
    "Navigate",
    [
        "🏠 Overview & Data",
        "🚛 Delivery & Shipping",
        "💹 Sales & Profit",
        "🗂️ Product Analysis",
        "🔍 Risk & Anomaly",
        "🧠 AI Insights",
    ],
    label_visibility="collapsed",
)
st.sidebar.markdown("---")
st.sidebar.markdown("**Dataset**")
st.sidebar.caption(f"Rows: **{len(df):,}** · Columns: **{df.shape[1]}**")
st.sidebar.caption(f"Orders: **{df['order_id'].nunique():,}**")
st.sidebar.caption(f"Years: **{sorted(df['order_year'].unique())}**")

# ═══════════════════════════════════════════════════════════════
# HOME — OVERVIEW, CLEANED DATA, EXPLORATION
# ═══════════════════════════════════════════════════════════════
if section == "🏠 Overview & Data":

    st.markdown("# 🛡️ Supply Chain Analytics & Risk Intelligence Dashboard")
    st.caption("SupplyGuard AI — End-to-end view of orders, sales, deliveries, and risk across global markets.")
    section_line()

    # ── KPIs ────────────────────────────────────────────────────
    total_orders    = df["order_id"].nunique()
    total_sales     = df["sales"].sum()
    total_profit    = df["order_profit"].sum()
    avg_margin      = df["profit_margin_pct"].mean()
    late_pct        = df["is_delayed"].mean() * 100
    fraud_count     = df["is_fraud_flagged"].sum()
    loss_orders     = df["is_loss_order"].sum()
    revenue_at_risk = df["revenue_at_risk"].sum()

    cols = st.columns(4)
    cols[0].markdown(kpi("Total Orders",      f"{total_orders:,}",    "unique order IDs",  C["blue"]),   unsafe_allow_html=True)
    cols[1].markdown(kpi("Total Revenue",     fmt_num(total_sales),   "gross sales",       C["teal"]),   unsafe_allow_html=True)
    cols[2].markdown(kpi("Total Profit",      fmt_num(total_profit),  "net profit",        C["green"]),  unsafe_allow_html=True)
    cols[3].markdown(kpi("Avg Profit Margin", f"{avg_margin:.1f}%",   "per order item",    C["indigo"]), unsafe_allow_html=True)

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    cols2 = st.columns(4)
    cols2[0].markdown(kpi("Late Delivery Rate",   f"{late_pct:.1f}%",      "of all shipments",  C["amber"]),  unsafe_allow_html=True)
    cols2[1].markdown(kpi("Fraud-Flagged Orders", f"{fraud_count:,}",       "suspected fraud",   C["rose"]),   unsafe_allow_html=True)
    cols2[2].markdown(kpi("Loss-Making Orders",   f"{loss_orders:,}",       "negative profit",   C["orange"]), unsafe_allow_html=True)
    cols2[3].markdown(kpi("Revenue at Risk",      fmt_num(revenue_at_risk), "from late / loss",  C["red"]),    unsafe_allow_html=True)

    section_line()

    # ── Overview Charts ──────────────────────────────────────────
    c1, c2 = st.columns(2)
    with c1:
        yr = df.groupby("order_year")["sales"].sum().sort_index()
        fig, ax = styled_fig()
        bars = ax.bar(yr.index.astype(str), yr.values,
                      color=[C["blue"], C["teal"], C["indigo"], C["sky"]], edgecolor="white")
        ax.set_title("Annual Revenue", fontsize=10, fontweight="bold")
        ax.set_ylabel("Revenue ($)", fontsize=9)
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x/1e6:.1f}M"))
        for bar in bars:
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() * 1.01,
                    f"${bar.get_height()/1e6:.1f}M", ha="center", fontsize=8, fontweight="bold")
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

    with c2:
        ds = df["delivery_status"].value_counts()
        fig, ax = styled_fig()
        wedges, texts, autotexts = ax.pie(
            ds.values, labels=ds.index, autopct="%1.1f%%",
            colors=PIE_PAL[:len(ds)], startangle=90,
            textprops={"fontsize": 8}, pctdistance=0.82,
            wedgeprops={"edgecolor": "white", "linewidth": 1.5})
        ax.set_title("Delivery Status Split", fontsize=10, fontweight="bold")
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

    # Market orders + Profit by year side by side
    c3, c4 = st.columns(2)
    with c3:
        mkt = df["market"].value_counts()
        fig, ax = styled_fig()
        color_bar(ax, mkt.index, mkt.values, PALETTE[:len(mkt)],
                  ylabel="Order Count", title="Orders by Market")
        ax.tick_params(axis="x", rotation=12)
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

    with c4:
        yr_p = df.groupby("order_year")["order_profit"].sum().sort_index()
        fig, ax = styled_fig()
        bar_colors = [C["green"] if v >= 0 else NEG_COLOR for v in yr_p.values]
        ax.bar(yr_p.index.astype(str), yr_p.values, color=bar_colors, edgecolor="white")
        ax.set_title("Annual Profit", fontsize=10, fontweight="bold")
        ax.set_ylabel("Profit ($)", fontsize=9)
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x/1e6:.1f}M"))
        ax.spines[["top","right"]].set_visible(False)
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

    section_line()

    # ── Cleaned Dataset ──────────────────────────────────────────
    st.markdown("## 🗃️ Cleaned Dataset")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Rows",           f"{df.shape[0]:,}")
    m2.metric("Columns",        f"{df.shape[1]}")
    m3.metric("Missing Values", f"{df.isnull().sum().sum():,}")
    m4.metric("Duplicate Rows", f"{df.duplicated().sum():,}")

    st.markdown("#### Column Data Types")
    dtype_df = pd.DataFrame({
        "Column":        df.dtypes.index,
        "Type":          df.dtypes.astype(str).values,
        "Non-Null Count": df.notnull().sum().values,
        "Null Count":    df.isnull().sum().values,
        "Unique Values": [df[c].nunique() for c in df.columns],
    })
    st.dataframe(dtype_df, use_container_width=True, height=260)

    st.markdown("#### Sample Records (first 10 rows)")
    st.dataframe(df.head(10), use_container_width=True)

    section_line()

    # ── Data Exploration ─────────────────────────────────────────
    st.markdown("## 🔬 Data Exploration")
    tab1, tab2, tab3 = st.tabs(["📊 Descriptive Stats", "📈 Distributions", "🔍 Patterns"])

    with tab1:
        num_cols = ["sales","order_profit","order_item_discount_rate",
                    "order_item_quantity","profit_margin_pct","days_shipping_real",
                    "shipping_delay_days","product_price"]
        st.dataframe(df[num_cols].describe().T.round(2), use_container_width=True)

    with tab2:
        col_sel = st.selectbox("Choose a numeric column", num_cols)
        data = df[col_sel].dropna()
        fig, ax = styled_fig()
        n, bins, patches = ax.hist(data, bins=40, edgecolor="white", linewidth=0.4)
        # gradient colouring by bin height
        norm = plt.Normalize(n.min(), n.max())
        cmap = plt.cm.Blues
        for p, val in zip(patches, n):
            p.set_facecolor(cmap(norm(val)))
        ax.set_title(f"Distribution of {col_sel}", fontsize=10, fontweight="bold")
        ax.set_xlabel(col_sel, fontsize=9)
        ax.set_ylabel("Count", fontsize=9)
        ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

    with tab3:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("##### Orders by Customer Segment")
            seg = df["customer_segment"].value_counts()
            fig, ax = styled_fig()
            color_bar(ax, seg.index, seg.values, [C["blue"], C["teal"], C["indigo"]],
                      ylabel="Order Count", title="Customer Segment")
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)

        with c2:
            st.markdown("##### Orders by Market")
            mkt2 = df["market"].value_counts()
            fig, ax = styled_fig()
            color_bar(ax, mkt2.index, mkt2.values, PALETTE[:len(mkt2)],
                      ylabel="Order Count", title="Market")
            ax.tick_params(axis="x", labelsize=8, rotation=12)
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)

        st.markdown("##### Orders by Shipping Mode")
        sm = df["shipping_mode"].value_counts()
        fig, ax = styled_fig(3.0)
        color_bar(ax, sm.index, sm.values, [C["sky"], C["blue"], C["indigo"], C["purple"]],
                  ylabel="Count", title="Shipping Mode")
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

        st.markdown("##### Order Status Breakdown")
        os_counts = df["order_status"].value_counts().reset_index()
        os_counts.columns = ["Status", "Count"]
        os_counts["% Share"] = (os_counts["Count"] / os_counts["Count"].sum() * 100).round(2)
        st.dataframe(os_counts, use_container_width=True)

        st.markdown("##### Payment Type Breakdown")
        pay = df["payment_type"].value_counts()
        fig, ax = styled_fig(3.5)
        ax.pie(pay.values, labels=pay.index, autopct="%1.1f%%",
               colors=PIE_PAL[:len(pay)], startangle=90,
               textprops={"fontsize": 8},
               wedgeprops={"edgecolor": "white", "linewidth": 1.5})
        ax.set_title("Payment Types", fontsize=10, fontweight="bold")
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

# ═══════════════════════════════════════════════════════════════
# DELIVERY & SHIPPING
# ═══════════════════════════════════════════════════════════════
elif section == "🚛 Delivery & Shipping":
    st.markdown("# 🚛 Delivery & Shipping Analysis")
    section_line()

    on_time_pct   = (df["delivery_status"] == "Shipping on time").mean() * 100
    late_pct      = (df["is_delayed"] == 1).mean() * 100
    avg_delay     = df.loc[df["is_delayed"] == 1, "shipping_delay_days"].mean()
    cancelled_pct = (df["delivery_status"] == "Shipping canceled").mean() * 100

    kc = st.columns(4)
    kc[0].markdown(kpi("On-Time Rate",        f"{on_time_pct:.1f}%",  "", C["green"]),  unsafe_allow_html=True)
    kc[1].markdown(kpi("Late Delivery Rate",  f"{late_pct:.1f}%",     "", C["red"]),    unsafe_allow_html=True)
    kc[2].markdown(kpi("Avg Delay (days)",    f"{avg_delay:.1f}",     "when late", C["amber"]), unsafe_allow_html=True)
    kc[3].markdown(kpi("Cancelled Shipments", f"{cancelled_pct:.1f}%","", C["orange"]), unsafe_allow_html=True)

    section_line()
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Delay Overview", "🚢 Shipping Mode", "🌍 Market & Region", "📅 Trends"])

    with tab1:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### Delivery Status Distribution")
            ds = df["delivery_status"].value_counts()
            fig, ax = styled_fig()
            color_barh(ax, ds.index, ds.values, PIE_PAL[:len(ds)], xlabel="Count")
            ax.set_title("Delivery Status", fontsize=10, fontweight="bold")
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)

        with c2:
            st.markdown("#### Late Delivery by Customer Segment")
            seg_late = df.groupby("customer_segment")["is_delayed"].mean().mul(100).sort_values()
            fig, ax = styled_fig()
            color_barh(ax, seg_late.index, seg_late.values,
                       [C["amber"], C["orange"], C["red"]], xlabel="Late Delivery %")
            ax.set_title("Late % by Segment", fontsize=10, fontweight="bold")
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)

        st.markdown("#### Late Delivery Risk Flag Analysis")
        risk_tab = df.groupby("late_delivery_risk").agg(
            Orders=("order_id","count"),
            Avg_Delay=("shipping_delay_days","mean"),
            Avg_Profit=("order_profit","mean"),
        ).round(2).reset_index()
        risk_tab["late_delivery_risk"] = risk_tab["late_delivery_risk"].map({0:"Low Risk", 1:"High Risk"})
        st.dataframe(risk_tab, use_container_width=True)

    with tab2:
        st.markdown("#### Late Delivery Rate by Shipping Mode")
        sm_late = df.groupby("shipping_mode")["is_delayed"].mean().mul(100).sort_values()
        fig, ax = styled_fig(3.0)
        color_barh(ax, sm_late.index, sm_late.values,
                   [C["green"], C["amber"], C["orange"], C["red"]][:len(sm_late)],
                   xlabel="Late Delivery %")
        ax.set_title("Late % by Shipping Mode", fontsize=10, fontweight="bold")
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

        st.markdown("#### Average Fulfillment Days by Shipping Mode")
        sm_days = df.groupby("shipping_mode")[["days_shipping_real","days_shipping_scheduled"]].mean().round(2)
        st.dataframe(sm_days, use_container_width=True)

        st.markdown("#### Shipping Mode Volume & Revenue")
        sm_rev = df.groupby("shipping_mode").agg(
            Orders=("order_id","count"),
            Revenue=("sales","sum"),
            Profit=("order_profit","sum"),
        ).round(0)
        sm_rev["Avg_Revenue_per_Order"] = (sm_rev["Revenue"] / sm_rev["Orders"]).round(2)
        st.dataframe(sm_rev, use_container_width=True)

    with tab3:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### Late Delivery Rate by Market")
            mkt_late = df.groupby("market")["is_delayed"].mean().mul(100).sort_values()
            fig, ax = styled_fig()
            color_barh(ax, mkt_late.index, mkt_late.values, PALETTE[:len(mkt_late)], xlabel="Late Delivery %")
            ax.set_title("Late % by Market", fontsize=10, fontweight="bold")
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)

        with c2:
            st.markdown("#### Orders by Market")
            mkt_ord = df["market"].value_counts()
            fig, ax = styled_fig()
            color_barh(ax, mkt_ord.index, mkt_ord.values, PALETTE[:len(mkt_ord)], xlabel="Order Count")
            ax.set_title("Order Volume by Market", fontsize=10, fontweight="bold")
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)

        st.markdown("#### Top 10 Regions by Late Deliveries")
        reg_late = df.groupby("order_region")["is_delayed"].mean().mul(100).sort_values(ascending=False).head(10)
        fig, ax = styled_fig(4.2)
        color_barh(ax, reg_late.index[::-1], reg_late.values[::-1],
                   PALETTE[:len(reg_late)], xlabel="Late Delivery %")
        ax.set_title("Top 10 Regions — Late %", fontsize=10, fontweight="bold")
        ax.tick_params(labelsize=7.5)
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

    with tab4:
        st.markdown("#### Monthly Late Delivery Trend")
        month_late = df.groupby("year_month")["is_delayed"].mean().mul(100).reset_index()
        month_late.columns = ["year_month", "late_pct"]
        month_late = month_late.sort_values("year_month")
        fig, ax = styled_fig(3.5)
        ax.fill_between(range(len(month_late)), month_late["late_pct"], alpha=0.15, color=C["red"])
        ax.plot(range(len(month_late)), month_late["late_pct"],
                color=C["red"], linewidth=2, marker="o", markersize=3.5)
        tick_step = max(1, len(month_late) // 8)
        ax.set_xticks(range(0, len(month_late), tick_step))
        ax.set_xticklabels(month_late["year_month"].iloc[::tick_step], rotation=45, fontsize=7.5)
        ax.set_ylabel("Late %", fontsize=9)
        ax.set_title("Monthly Late Delivery %", fontsize=10, fontweight="bold")
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:.0f}%"))
        ax.spines[["top","right"]].set_visible(False)
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

        st.markdown("#### Yearly Delivery Performance")
        yr_del = df.groupby(["order_year","delivery_status"]).size().unstack(fill_value=0)
        st.dataframe(yr_del, use_container_width=True)

# ═══════════════════════════════════════════════════════════════
# SALES & PROFIT
# ═══════════════════════════════════════════════════════════════
elif section == "💹 Sales & Profit":
    st.markdown("# 💹 Sales & Profit Analysis")
    section_line()

    total_sales  = df["sales"].sum()
    total_profit = df["order_profit"].sum()
    avg_margin   = df["profit_margin_pct"].mean()
    avg_discount = df["order_item_discount_rate"].mean() * 100

    kc = st.columns(4)
    kc[0].markdown(kpi("Total Revenue",    fmt_num(total_sales),  "", C["blue"]),   unsafe_allow_html=True)
    kc[1].markdown(kpi("Total Profit",     fmt_num(total_profit), "", C["green"]),  unsafe_allow_html=True)
    kc[2].markdown(kpi("Avg Profit Margin",f"{avg_margin:.1f}%",  "", C["teal"]),   unsafe_allow_html=True)
    kc[3].markdown(kpi("Avg Discount Rate",f"{avg_discount:.1f}%","", C["amber"]),  unsafe_allow_html=True)

    section_line()
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Yearly Trends", "👥 Segments", "🌍 Markets", "💸 Discounts"])

    with tab1:
        c1, c2 = st.columns(2)
        with c1:
            yr_rev = df.groupby("order_year")["sales"].sum()
            fig, ax = styled_fig()
            color_bar(ax, yr_rev.index.astype(str), yr_rev.values,
                      [C["blue"], C["teal"], C["indigo"], C["sky"]],
                      ylabel="Revenue ($)", title="Annual Revenue")
            ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x/1e6:.1f}M"))
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)

        with c2:
            yr_prof = df.groupby("order_year")["order_profit"].sum()
            fig, ax = styled_fig()
            bar_colors = [C["green"] if v >= 0 else NEG_COLOR for v in yr_prof.values]
            color_bar(ax, yr_prof.index.astype(str), yr_prof.values, bar_colors,
                      ylabel="Profit ($)", title="Annual Profit")
            ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x/1e6:.1f}M"))
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)

        st.markdown("#### Monthly Revenue & Profit Trend")
        mn = df.groupby("year_month").agg(
            Revenue=("sales","sum"), Profit=("order_profit","sum")
        ).reset_index().sort_values("year_month")
        fig, ax = styled_fig(3.8)
        ax.fill_between(range(len(mn)), mn["Revenue"], alpha=0.1, color=C["blue"])
        ax.plot(range(len(mn)), mn["Revenue"], label="Revenue", color=C["blue"], linewidth=2)
        ax.plot(range(len(mn)), mn["Profit"],  label="Profit",  color=C["green"], linewidth=2, linestyle="--")
        tick_step = max(1, len(mn) // 8)
        ax.set_xticks(range(0, len(mn), tick_step))
        ax.set_xticklabels(mn["year_month"].iloc[::tick_step], rotation=45, fontsize=7.5)
        ax.set_ylabel("Amount ($)", fontsize=9)
        ax.legend(fontsize=8)
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x/1e6:.1f}M"))
        ax.spines[["top","right"]].set_visible(False)
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

        st.markdown("#### Yearly Summary Table")
        yr_tab = df.groupby("order_year").agg(
            Orders=("order_id","count"),
            Revenue=("sales","sum"),
            Profit=("order_profit","sum"),
            Avg_Margin=("profit_margin_pct","mean"),
            Avg_Discount=("order_item_discount_rate","mean"),
        ).round(2)
        yr_tab["Profit_Margin_%"] = (yr_tab["Profit"] / yr_tab["Revenue"] * 100).round(2)
        st.dataframe(yr_tab, use_container_width=True)

    with tab2:
        c1, c2 = st.columns(2)
        with c1:
            seg_sales = df.groupby("customer_segment")[["sales","order_profit"]].sum().sort_values("sales", ascending=True)
            fig, ax = styled_fig()
            x = range(len(seg_sales))
            w = 0.35
            ax.bar([i - w/2 for i in x], seg_sales["sales"],        width=w, label="Revenue",
                   color=C["blue"], edgecolor="white")
            ax.bar([i + w/2 for i in x], seg_sales["order_profit"], width=w, label="Profit",
                   color=C["green"], edgecolor="white")
            ax.set_xticks(list(x))
            ax.set_xticklabels(seg_sales.index, fontsize=8)
            ax.legend(fontsize=8)
            ax.set_title("Revenue & Profit by Segment", fontsize=10, fontweight="bold")
            ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x/1e6:.1f}M"))
            ax.spines[["top","right"]].set_visible(False)
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)

        with c2:
            seg_margin = df.groupby("customer_segment")["profit_margin_pct"].mean().sort_values()
            fig, ax = styled_fig()
            color_barh(ax, seg_margin.index, seg_margin.values,
                       [C["teal"], C["blue"], C["indigo"]], xlabel="Avg Profit Margin %")
            ax.set_title("Margin by Segment", fontsize=10, fontweight="bold")
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)

        st.markdown("#### Segment Deep Dive")
        seg_detail = df.groupby("customer_segment").agg(
            Orders=("order_id","count"),
            Revenue=("sales","sum"),
            Profit=("order_profit","sum"),
            Avg_Margin=("profit_margin_pct","mean"),
            Late_Rate=("is_delayed","mean"),
            Loss_Orders=("is_loss_order","sum"),
        ).round(2)
        seg_detail["Late_Rate_%"] = (seg_detail["Late_Rate"] * 100).round(1)
        seg_detail = seg_detail.drop(columns=["Late_Rate"])
        st.dataframe(seg_detail, use_container_width=True)

    with tab3:
        c1, c2 = st.columns(2)
        with c1:
            mkt_rev = df.groupby("market")["sales"].sum().sort_values()
            fig, ax = styled_fig()
            color_barh(ax, mkt_rev.index, mkt_rev.values, PALETTE[:len(mkt_rev)], xlabel="Revenue ($)")
            ax.set_title("Revenue by Market", fontsize=10, fontweight="bold")
            ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x/1e6:.1f}M"))
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)

        with c2:
            mkt_prof = df.groupby("market")["order_profit"].sum().sort_values()
            fig, ax = styled_fig()
            pcolors = [C["green"] if v >= 0 else NEG_COLOR for v in mkt_prof.values]
            color_barh(ax, mkt_prof.index, mkt_prof.values, pcolors, xlabel="Profit ($)")
            ax.set_title("Profit by Market", fontsize=10, fontweight="bold")
            ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x/1e6:.1f}M"))
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)

        st.markdown("#### Top 10 Regions by Revenue")
        reg_rev = df.groupby("order_region")["sales"].sum().sort_values(ascending=False).head(10)
        st.dataframe(reg_rev.reset_index().rename(columns={"sales":"Revenue ($)"}), use_container_width=True)

    with tab4:
        st.markdown("#### Discount Rate Distribution")
        data_d = df["order_item_discount_rate"].dropna()
        fig, ax = styled_fig()
        n, bins, patches = ax.hist(data_d, bins=30, edgecolor="white", linewidth=0.4)
        norm = plt.Normalize(n.min(), n.max())
        cmap = plt.cm.YlOrRd
        for p, val in zip(patches, n):
            p.set_facecolor(cmap(norm(val)))
        ax.set_xlabel("Discount Rate", fontsize=9)
        ax.set_ylabel("Count", fontsize=9)
        ax.set_title("Discount Rate Distribution", fontsize=10, fontweight="bold")
        ax.spines[["top","right"]].set_visible(False)
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

        st.markdown("#### Profit Margin vs Discount Rate")
        sample = df[["order_item_discount_rate","profit_margin_pct"]].dropna().sample(min(3000, len(df)), random_state=42)
        fig, ax = styled_fig()
        scatter = ax.scatter(sample["order_item_discount_rate"], sample["profit_margin_pct"],
                             alpha=0.25, s=8, c=sample["profit_margin_pct"],
                             cmap="RdYlGn", vmin=-100, vmax=100)
        plt.colorbar(scatter, ax=ax, label="Profit Margin %", shrink=0.8)
        ax.set_xlabel("Discount Rate", fontsize=9)
        ax.set_ylabel("Profit Margin %", fontsize=9)
        ax.set_title("Discount vs Profit Margin (sample 3k)", fontsize=10, fontweight="bold")
        ax.spines[["top","right"]].set_visible(False)
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

        disc_tab = df.groupby("customer_segment").agg(
            Avg_Discount=("order_item_discount_rate","mean"),
            Total_Discount_Given=("order_item_discount","sum"),
            Avg_Profit_Margin=("profit_margin_pct","mean"),
        ).round(3)
        disc_tab["Avg_Discount_%"] = (disc_tab["Avg_Discount"] * 100).round(2)
        st.dataframe(disc_tab, use_container_width=True)

# ═══════════════════════════════════════════════════════════════
# PRODUCT ANALYSIS
# ═══════════════════════════════════════════════════════════════
elif section == "🗂️ Product Analysis":
    st.markdown("# 🗂️ Product Analysis")
    section_line()

    total_products   = df["product_id"].nunique()
    total_categories = df["category_name"].nunique()
    total_depts      = df["department_name"].nunique()
    top_product      = df.groupby("product_name")["sales"].sum().idxmax()

    kc = st.columns(4)
    kc[0].markdown(kpi("Unique Products", f"{total_products:,}",  "", C["blue"]),   unsafe_allow_html=True)
    kc[1].markdown(kpi("Categories",      f"{total_categories:,}","", C["teal"]),   unsafe_allow_html=True)
    kc[2].markdown(kpi("Departments",     f"{total_depts:,}",     "", C["indigo"]), unsafe_allow_html=True)
    kc[3].markdown(kpi("Top Revenue Product",
                        top_product[:22]+"…" if len(top_product) > 22 else top_product,
                        "by revenue", C["amber"]), unsafe_allow_html=True)

    section_line()
    tab1, tab2, tab3 = st.tabs(["🏆 Top Products", "🏢 Departments & Categories", "📉 Low Performers"])

    with tab1:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### Top 10 Products by Revenue")
            top_rev = df.groupby("product_name")["sales"].sum().sort_values(ascending=False).head(10)
            fig, ax = styled_fig(4.5)
            color_barh(ax, top_rev.index[::-1], top_rev.values[::-1], PALETTE[:10], xlabel="Revenue ($)")
            ax.set_title("Top 10 by Revenue", fontsize=10, fontweight="bold")
            ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x/1e3:.0f}K"))
            ax.tick_params(labelsize=7.5)
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)

        with c2:
            st.markdown("#### Top 10 Products by Profit")
            top_prof = df.groupby("product_name")["order_profit"].sum().sort_values(ascending=False).head(10)
            fig, ax = styled_fig(4.5)
            color_barh(ax, top_prof.index[::-1], top_prof.values[::-1], PALETTE[:10], xlabel="Profit ($)")
            ax.set_title("Top 10 by Profit", fontsize=10, fontweight="bold")
            ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x/1e3:.0f}K"))
            ax.tick_params(labelsize=7.5)
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)

        st.markdown("#### Top 15 Products — Full Table")
        prod_table = df.groupby("product_name").agg(
            Orders=("order_id","count"),
            Revenue=("sales","sum"),
            Profit=("order_profit","sum"),
            Avg_Margin=("profit_margin_pct","mean"),
            Avg_Price=("product_price","mean"),
        ).round(2).sort_values("Revenue", ascending=False).head(15)
        st.dataframe(prod_table, use_container_width=True)

    with tab2:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### Revenue by Department")
            dept_rev = df.groupby("department_name")["sales"].sum().sort_values()
            fig, ax = styled_fig(4.5)
            color_barh(ax, dept_rev.index, dept_rev.values, PALETTE[:len(dept_rev)], xlabel="Revenue ($)")
            ax.set_title("Revenue by Department", fontsize=10, fontweight="bold")
            ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x/1e6:.1f}M"))
            ax.tick_params(labelsize=7.5)
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)

        with c2:
            st.markdown("#### Profit by Department")
            dept_prof = df.groupby("department_name")["order_profit"].sum().sort_values()
            fig, ax = styled_fig(4.5)
            dp_colors = [C["green"] if v >= 0 else NEG_COLOR for v in dept_prof.values]
            color_barh(ax, dept_prof.index, dept_prof.values, dp_colors, xlabel="Profit ($)")
            ax.set_title("Profit by Department", fontsize=10, fontweight="bold")
            ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x/1e6:.1f}M"))
            ax.tick_params(labelsize=7.5)
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)

        st.markdown("#### Category Performance")
        cat_tab = df.groupby("category_name").agg(
            Orders=("order_id","count"),
            Revenue=("sales","sum"),
            Profit=("order_profit","sum"),
            Avg_Margin=("profit_margin_pct","mean"),
            Loss_Orders=("is_loss_order","sum"),
        ).round(2).sort_values("Revenue", ascending=False)
        cat_tab["Loss_Rate_%"] = (cat_tab["Loss_Orders"] / cat_tab["Orders"] * 100).round(1)
        st.dataframe(cat_tab, use_container_width=True)

    with tab3:
        st.markdown("#### Bottom 10 Products by Profit (Loss Leaders)")
        bot_prof = df.groupby("product_name")["order_profit"].sum().sort_values().head(10)
        fig, ax = styled_fig(4.0)
        color_barh(ax, bot_prof.index[::-1], bot_prof.values[::-1],
                   [NEG_COLOR]*10, xlabel="Total Profit ($)")
        ax.set_title("Bottom 10 Products by Profit", fontsize=10, fontweight="bold")
        ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
        ax.tick_params(labelsize=7.5)
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

        st.markdown("#### Products with Highest Loss-Order Rate")
        loss_rate_df = df.groupby("product_name").agg(
            Total_Orders=("order_id","count"),
            Loss_Orders=("is_loss_order","sum"),
            Avg_Profit=("order_profit","mean"),
        )
        loss_rate_df["Loss_Rate_%"] = (loss_rate_df["Loss_Orders"] / loss_rate_df["Total_Orders"] * 100).round(1)
        st.dataframe(
            loss_rate_df[loss_rate_df["Total_Orders"] >= 50].sort_values("Loss_Rate_%", ascending=False).head(15),
            use_container_width=True,
        )

# ═══════════════════════════════════════════════════════════════
# RISK & ANOMALY
# ═══════════════════════════════════════════════════════════════
elif section == "🔍 Risk & Anomaly":
    st.markdown("# 🔍 Risk & Anomaly Analysis")
    section_line()

    fraud_orders  = df["is_fraud_flagged"].sum()
    fraud_revenue = df.loc[df["is_fraud_flagged"] == 1, "sales"].sum()
    loss_orders   = df["is_loss_order"].sum()
    rev_at_risk   = df["revenue_at_risk"].sum()
    loss_revenue  = df.loc[df["is_loss_order"] == 1, "sales"].sum()

    kc = st.columns(3)
    kc[0].markdown(kpi("Fraud-Flagged Orders",  f"{fraud_orders:,}",    f"Revenue: {fmt_num(fraud_revenue)}", C["rose"]),   unsafe_allow_html=True)
    kc[1].markdown(kpi("Loss-Making Orders",    f"{loss_orders:,}",     f"Revenue: {fmt_num(loss_revenue)}", C["orange"]),  unsafe_allow_html=True)
    kc[2].markdown(kpi("Total Revenue at Risk", fmt_num(rev_at_risk),   "late + loss",                       C["red"]),     unsafe_allow_html=True)

    section_line()
    tab1, tab2, tab3 = st.tabs(["🚨 Fraud Analysis", "📉 Loss Orders", "💰 Revenue at Risk"])

    with tab1:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### Fraud Rate by Payment Type")
            pay_fraud = df.groupby("payment_type")["is_fraud_flagged"].mean().mul(100).sort_values(ascending=True)
            fig, ax = styled_fig()
            color_barh(ax, pay_fraud.index, pay_fraud.values,
                       [C["amber"], C["orange"], C["red"], C["rose"]][:len(pay_fraud)],
                       xlabel="Fraud Rate %")
            ax.set_title("Fraud Rate by Payment Type", fontsize=10, fontweight="bold")
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)

        with c2:
            st.markdown("#### Fraud Rate by Market")
            mkt_fraud = df.groupby("market")["is_fraud_flagged"].mean().mul(100).sort_values(ascending=True)
            fig, ax = styled_fig()
            color_barh(ax, mkt_fraud.index, mkt_fraud.values, PALETTE[:len(mkt_fraud)], xlabel="Fraud Rate %")
            ax.set_title("Fraud Rate by Market", fontsize=10, fontweight="bold")
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)

        st.markdown("#### Suspected Fraud Orders — Status Breakdown")
        fraud_status = df.groupby("order_status")["is_fraud_flagged"].sum().sort_values(ascending=False).reset_index()
        fraud_status.columns = ["Order Status", "Fraud Flagged Count"]
        st.dataframe(fraud_status, use_container_width=True)

        st.markdown("#### Fraud Risk Score Distribution")
        fig, ax = styled_fig(3.0)
        scores = df["fraud_risk_score"].dropna()
        n, bins, patches = ax.hist(scores, bins=int(scores.max() - scores.min() + 1),
                                   edgecolor="white", rwidth=0.8)
        score_colors = [C["green"], C["amber"], C["orange"], C["red"], C["rose"]]
        for p, col in zip(patches, score_colors[:len(patches)]):
            p.set_facecolor(col)
        ax.set_xlabel("Fraud Risk Score", fontsize=9)
        ax.set_ylabel("Count", fontsize=9)
        ax.set_title("Fraud Risk Score Distribution", fontsize=10, fontweight="bold")
        ax.spines[["top","right"]].set_visible(False)
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

        st.markdown("#### High Fraud Risk Orders (Score ≥ 2)")
        high_fraud = df[df["fraud_risk_score"] >= 2][
            ["order_id","order_status","payment_type","sales","order_profit",
             "market","fraud_risk_score","is_fraud_flagged"]
        ].sort_values("fraud_risk_score", ascending=False).head(20)
        st.dataframe(high_fraud, use_container_width=True)

    with tab2:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### Loss Order Rate by Department")
            dept_loss = df.groupby("department_name")["is_loss_order"].mean().mul(100).sort_values(ascending=True)
            fig, ax = styled_fig(4.2)
            color_barh(ax, dept_loss.index, dept_loss.values, PALETTE[:len(dept_loss)], xlabel="Loss Order Rate %")
            ax.set_title("Loss Rate by Department", fontsize=10, fontweight="bold")
            ax.tick_params(labelsize=7.5)
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)

        with c2:
            st.markdown("#### Loss Order Rate by Shipping Mode")
            sm_loss = df.groupby("shipping_mode")["is_loss_order"].mean().mul(100).sort_values(ascending=True)
            fig, ax = styled_fig(3.0)
            color_barh(ax, sm_loss.index, sm_loss.values,
                       [C["green"], C["amber"], C["orange"], C["red"]][:len(sm_loss)],
                       xlabel="Loss Order Rate %")
            ax.set_title("Loss Rate by Shipping Mode", fontsize=10, fontweight="bold")
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)

        st.markdown("#### Monthly Loss Order Trend")
        mn_loss = df.groupby("year_month")["is_loss_order"].mean().mul(100).reset_index().sort_values("year_month")
        fig, ax = styled_fig(3.5)
        ax.fill_between(range(len(mn_loss)), mn_loss["is_loss_order"], alpha=0.15, color=C["orange"])
        ax.plot(range(len(mn_loss)), mn_loss["is_loss_order"],
                color=C["orange"], linewidth=2, marker="o", markersize=3.5)
        tick_step = max(1, len(mn_loss) // 8)
        ax.set_xticks(range(0, len(mn_loss), tick_step))
        ax.set_xticklabels(mn_loss["year_month"].iloc[::tick_step], rotation=45, fontsize=7.5)
        ax.set_ylabel("Loss Order Rate %", fontsize=9)
        ax.set_title("Monthly Loss Order %", fontsize=10, fontweight="bold")
        ax.spines[["top","right"]].set_visible(False)
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

    with tab3:
        st.markdown("#### Revenue at Risk by Market")
        rar_mkt = df.groupby("market")["revenue_at_risk"].sum().sort_values(ascending=True)
        fig, ax = styled_fig()
        color_barh(ax, rar_mkt.index, rar_mkt.values, PALETTE[:len(rar_mkt)], xlabel="Revenue at Risk ($)")
        ax.set_title("Revenue at Risk by Market", fontsize=10, fontweight="bold")
        ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x/1e6:.1f}M"))
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

        st.markdown("#### Revenue at Risk by Shipping Mode")
        rar_sm = df.groupby("shipping_mode")["revenue_at_risk"].sum().sort_values(ascending=True)
        fig, ax = styled_fig(3.0)
        color_barh(ax, rar_sm.index, rar_sm.values,
                   [C["teal"], C["amber"], C["orange"], C["red"]][:len(rar_sm)],
                   xlabel="Revenue at Risk ($)")
        ax.set_title("Revenue at Risk by Shipping Mode", fontsize=10, fontweight="bold")
        ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x/1e6:.1f}M"))
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

        st.markdown("#### Discount-Driven Losses")
        disc_loss = df[df["is_loss_order"] == 1].groupby("order_item_discount_rate").agg(
            Loss_Orders=("order_id","count"),
            Total_Loss=("order_profit","sum"),
        ).round(2).reset_index().sort_values("Total_Loss")
        st.dataframe(disc_loss.tail(15), use_container_width=True)

        transfer_fraud_pct = df[df["is_transfer_payment"] == 1]["is_fraud_flagged"].mean() * 100
        st.markdown(
            f'<div class="insight-box">💡 Orders with discount rate above 10% show significantly higher loss incidence. '
            f'Total revenue at risk: <strong>{fmt_num(df["revenue_at_risk"].sum())}</strong> across all markets. '
            f'Transfer payment is linked to <strong>{transfer_fraud_pct:.1f}%</strong> of fraud-flagged orders.</div>',
            unsafe_allow_html=True,
        )

# ═══════════════════════════════════════════════════════════════
# AI INSIGHTS
# ═══════════════════════════════════════════════════════════════
elif section == "🧠 AI Insights":
    st.markdown("# 🧠 AI Insights")
    st.caption("What is the data telling us? — Key findings distilled from the full analytics pipeline.")
    section_line()

    total_orders     = df["order_id"].nunique()
    total_sales      = df["sales"].sum()
    total_profit     = df["order_profit"].sum()
    avg_margin       = df["profit_margin_pct"].mean()
    late_pct         = df["is_delayed"].mean() * 100
    fraud_count      = df["is_fraud_flagged"].sum()
    loss_orders      = df["is_loss_order"].sum()
    loss_rate        = df["is_loss_order"].mean() * 100
    rev_at_risk      = df["revenue_at_risk"].sum()
    top_market       = df.groupby("market")["sales"].sum().idxmax()
    worst_del_market = df.groupby("market")["is_delayed"].mean().idxmax()
    best_dept        = df.groupby("department_name")["order_profit"].sum().idxmax()
    worst_dept       = df.groupby("department_name")["order_profit"].sum().idxmin()
    top_seg          = df.groupby("customer_segment")["sales"].sum().idxmax()
    most_late_mode   = df.groupby("shipping_mode")["is_delayed"].mean().idxmax()
    disc_corr        = df[["order_item_discount_rate","profit_margin_pct"]].corr().iloc[0, 1]
    fraud_pay        = df.groupby("payment_type")["is_fraud_flagged"].mean().idxmax()

    insight_colors = [C["blue"], C["red"], C["orange"], C["amber"], C["rose"], C["teal"], C["indigo"], C["green"]]
    insights = [
        ("🌐 Scale & Reach",
         f"The supply chain dataset covers <strong>{total_orders:,} unique orders</strong> across <strong>5 global markets</strong> "
         f"spanning 4 years (2015–2018). Total gross revenue is <strong>{fmt_num(total_sales)}</strong> with net profit of "
         f"<strong>{fmt_num(total_profit)}</strong> — an average profit margin of <strong>{avg_margin:.1f}%</strong> per order item."),

        ("🚨 Delivery Crisis — The Biggest Operational Risk",
         f"<strong>{late_pct:.1f}% of all shipments are delivered late</strong>. This is not a minor issue — it affects more than "
         f"half of all orders. The <strong>{worst_del_market}</strong> market has the highest late delivery rate, and "
         f"<strong>{most_late_mode}</strong> shipping is the most delay-prone mode. Late deliveries are the primary driver "
         f"of customer dissatisfaction and revenue at risk."),

        ("💸 Revenue at Risk Is Substantial",
         f"A total of <strong>{fmt_num(rev_at_risk)}</strong> in revenue is at risk due to late deliveries and loss-making orders. "
         f"<strong>{loss_orders:,} orders ({loss_rate:.1f}%)</strong> are loss-making — meaning the business is selling at a "
         f"loss on roughly 1 in 5 transactions. Immediate intervention on loss products and discount policies is needed."),

        ("🏷️ Discounts Are Hurting Profitability",
         f"There is a <strong>negative correlation ({disc_corr:.2f})</strong> between discount rate and profit margin. "
         f"Orders with high discount rates (>10%) are significantly more likely to be loss-making. "
         f"The discount strategy needs to be re-evaluated — especially in segments where margins are already thin."),

        ("🕵️ Fraud Is a Real and Quantifiable Threat",
         f"<strong>{fraud_count:,} orders are flagged as potentially fraudulent</strong>, representing "
         f"{fmt_num(df.loc[df['is_fraud_flagged']==1,'sales'].sum())} in revenue exposure. "
         f"The <strong>{fraud_pay}</strong> payment method has the highest fraud association. "
         f"Orders marked as SUSPECTED_FRAUD in the order status confirm this pattern. "
         f"A fraud detection and prevention system should be prioritized."),

        ("🏆 Top Market & Best Performer",
         f"<strong>{top_market}</strong> is the highest revenue-generating market. "
         f"The <strong>{top_seg}</strong> customer segment drives the most sales volume. "
         f"The <strong>{best_dept}</strong> department generates the most profit, "
         f"while <strong>{worst_dept}</strong> consistently produces losses — suggesting a portfolio review is needed."),

        ("📅 Growth Trend & Seasonality",
         f"Revenue grew from 2015 to 2018 with visible quarterly seasonality. Q4 typically shows higher order volumes. "
         f"Year-over-year profit improvement was inconsistent due to rising loss orders and discounting. "
         f"Aligning discount campaigns with high-margin periods would significantly improve profitability."),

        ("🔧 Recommended Actions",
         "<ol style='margin:0;padding-left:18px;line-height:1.8'>"
         "<li>Audit and tighten the discount policy — especially for &gt;10% discount rates.</li>"
         "<li>Investigate and reduce late deliveries in Pacific Asia and with Standard Class shipping.</li>"
         "<li>Implement automated fraud screening for Transfer payment orders with high fraud risk scores.</li>"
         "<li>Review loss-making products in the Book Shop and Discs Shop departments.</li>"
         "<li>Invest in predictive delivery analytics to flag high-risk shipments before they go late.</li>"
         "<li>Segment-level profitability dashboards should be reviewed monthly by regional managers.</li>"
         "</ol>"),
    ]

    for (title, body), accent in zip(insights, insight_colors):
        st.markdown(f"### {title}")
        st.markdown(
            f'<div class="insight-box" style="border-left-color:{accent};background:{accent}0d;font-size:0.92rem">'
            f'{body}</div>',
            unsafe_allow_html=True,
        )
        st.markdown("")

    section_line()

    # ── Summary Scorecard ────────────────────────────────────────
    st.markdown("#### 📊 Summary Scorecard")
    score_data = {
        "Metric": [
            "Total Revenue", "Total Profit", "Avg Profit Margin",
            "Late Delivery Rate", "Loss Order Rate",
            "Fraud-Flagged Orders", "Revenue at Risk",
        ],
        "Value": [
            fmt_num(total_sales), fmt_num(total_profit), f"{avg_margin:.1f}%",
            f"{late_pct:.1f}%",   f"{loss_rate:.1f}%",
            f"{fraud_count:,}",   fmt_num(rev_at_risk),
        ],
        "Status": [
            "✅ Strong", "✅ Positive", "⚠️ Moderate",
            "🔴 Critical", "🔴 High",
            "⚠️ Monitor", "🔴 High",
        ],
    }
    st.dataframe(pd.DataFrame(score_data), use_container_width=True, hide_index=True)

    # ── Scorecard visual bar ─────────────────────────────────────
    st.markdown("#### 📈 Key Metric Comparison (Rates %)")
    rate_metrics = {
        "Late Delivery %": late_pct,
        "Loss Order %":    loss_rate,
        "Fraud Rate %":    fraud_count / len(df) * 100,
        "On-Time %":       (df["delivery_status"] == "Shipping on time").mean() * 100,
        "Profit Margin %": avg_margin,
    }
    fig, ax = styled_fig(3.0)
    bar_colors_sc = [C["red"], C["orange"], C["rose"], C["green"], C["blue"]]
    bars = ax.bar(list(rate_metrics.keys()), list(rate_metrics.values()),
                  color=bar_colors_sc, edgecolor="white")
    ax.set_ylabel("%", fontsize=9)
    ax.set_title("Business Health Metrics (%)", fontsize=10, fontweight="bold")
    ax.spines[["top","right"]].set_visible(False)
    ax.tick_params(axis="x", labelsize=8, rotation=10)
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                f"{bar.get_height():.1f}%", ha="center", fontsize=8, fontweight="bold")
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    section_line()
    st.markdown(
        "<p style='font-size:0.8rem;color:#888;text-align:center'>"
        "Analysis based on supply_chain_cleaned.csv · 180,519 records · 62 features · 2015–2018 · SupplyGuard AI"
        "</p>",
        unsafe_allow_html=True,
    )
