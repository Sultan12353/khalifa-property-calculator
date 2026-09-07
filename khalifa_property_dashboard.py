import streamlit as st
import plotly.graph_objects as go


st.set_page_config(
    page_title="Khalifa Property Calculator",
    page_icon="🏠",
    layout="wide",
)
st.markdown(
    """
    <style>
    div[data-testid="stSliderThumbValue"] {
        font-size: 13px !important;
        font-weight: 600 !important;
        padding: 3px 6px !important;
        min-width: 45px !important;
        transition: all 0.15s ease-in-out !important;
    }

    div[data-testid="stSlider"]:has([role="slider"]:active)
    div[data-testid="stSliderThumbValue"] {
        font-size: 27px !important;
        font-weight: 900 !important;
        color: white !important;
        background-color: #176B87 !important;
        padding: 10px 14px !important;
        border-radius: 10px !important;
        min-width: 110px !important;
        transform: translateY(-8px) !important;
        box-shadow: 0 5px 14px rgba(0,0,0,0.30) !important;
    }

    div[data-baseweb="slider"] [role="slider"] {
        transition: all 0.15s ease-in-out !important;
    }

    div[data-baseweb="slider"] [role="slider"]:active {
        width: 25px !important;
        height: 25px !important;
        background-color: #18A999 !important;
        border: 3px solid white !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.30) !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

def money(value: float) -> str:
    return f"£{value:,.0f}"


def calculate_sdlt(price: float, additional_property: bool = True) -> float:
    """England residential SDLT bands, with optional 5% additional-property surcharge."""
    bands = [
        (125_000, 0.00),
        (250_000, 0.02),
        (925_000, 0.05),
        (1_500_000, 0.10),
        (float("inf"), 0.12),
    ]
    surcharge = 0.05 if additional_property else 0.0
    tax = 0.0
    lower = 0.0

    for upper, rate in bands:
        taxable_slice = max(0.0, min(price, upper) - lower)
        tax += taxable_slice * (rate + surcharge)
        if price <= upper:
            break
        lower = upper

    return tax


st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #f5f8ff 0%, #eefaf8 55%, #fff7e7 100%);
    }
    .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }
    .hero {
        padding: 1.7rem 2rem;
        border-radius: 24px;
        color: white;
        background: linear-gradient(120deg, #102a43, #176b87 58%, #18a999);
        box-shadow: 0 14px 35px rgba(16, 42, 67, 0.20);
        margin-bottom: 1.4rem;
    }
    .hero h1 { margin: 0; font-size: 2.15rem; }
    .hero p { margin: .45rem 0 0; opacity: .88; font-size: 1.02rem; }
    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.92);
        border: 1px solid rgba(23, 107, 135, 0.14);
        border-radius: 18px;
        padding: 1rem 1.1rem;
        box-shadow: 0 8px 20px rgba(16, 42, 67, 0.08);
    }
    div[data-testid="stMetricLabel"] { color: #486581; }
    div[data-testid="stMetricValue"] { color: #102a43; }
    div[data-testid="stNumberInput"] input {
        border-radius: 12px;
    }
    .decision {
        padding: 1rem 1.2rem;
        border-radius: 16px;
        font-weight: 700;
        font-size: 1.05rem;
        margin-top: .6rem;
    }
    .go { background: #d9fbe8; color: #087443; border-left: 7px solid #18a999; }
    .review { background: #fff1c7; color: #8a5700; border-left: 7px solid #f4b942; }
    .stop { background: #ffe1e1; color: #9c2424; border-left: 7px solid #e45757; }
    .small-note { color: #627d98; font-size: .86rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
        <h1>🏠 Khalifa Property Calculator</h1>
        <p>One clear view of costs, post-tax profit and investor return.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.header("Deal assumptions")
    target_roi = st.slider("Target post-tax ROI", 5.0, 30.0, 15.0, 0.5)
    tax_rate = st.slider("Estimated project tax rate", 0.0, 30.0, 19.0, 1.0)
    additional_property = st.toggle("Additional-property SDLT", value=True)
    contingency_rate = st.slider("Renovation contingency", 0.0, 25.0, 12.0, 1.0)
    st.caption("Tax treatment depends on ownership and activity. Confirm it with a UK accountant.")

st.subheader("Adjust the property figures")

left, middle, right = st.columns(3)

with left:
    purchase_price = st.slider(
        "Purchase price",
        min_value=0,
        max_value=2000000,
        value=0,
        step=5000,
        format="£%d"
    )

    renovation = st.slider(
        "Renovation budget",
        min_value=0,
        max_value=500000,
        value=0,
        step=5000,
        format="£%d"
    )

with middle:
    buying_costs = st.slider(
        "Buying costs",
        min_value=0,
        max_value=50000,
        value=7000,
        step=500,
        format="£%d"
    )

    finance_costs = st.slider(
        "Holding costs",
        min_value=0,
        max_value=50000,
        value=3000,
        step=500,
        format="£%d"
    )

with right:
    selling_costs = st.slider(
        "Selling costs",
        min_value=0,
        max_value=50000,
        value=7000,
        step=500,
        format="£%d"
    )

    selling_price = st.slider(
        "Expected selling price",
        min_value=0,
        max_value=3000000,
        value=0,
        step=5000,
        format="£%d"
    )
sdlt = calculate_sdlt(purchase_price, additional_property)
contingency = renovation * contingency_rate / 100
total_cost = purchase_price + sdlt + renovation + contingency + buying_costs + finance_costs + selling_costs
pre_tax_profit = selling_price - total_cost
estimated_tax = max(pre_tax_profit, 0) * tax_rate / 100
post_tax_profit = pre_tax_profit - estimated_tax
roi = (post_tax_profit / total_cost * 100) if total_cost else 0.0
margin = (post_tax_profit / selling_price * 100) if selling_price else 0.0

st.divider()
st.subheader("Investment result")
m1, m2, m3, m4 = st.columns(4)
m1.metric("Total project cost", money(total_cost))
m2.metric("Post-tax profit", money(post_tax_profit))
m3.metric("Post-tax ROI", f"{roi:.1f}%", f"Target {target_roi:.1f}%")
m4.metric("Profit margin", f"{margin:.1f}%")

if roi >= target_roi:
    decision_class = "go"
    decision_text = "✅ Meets target — proceed to full survey and legal due diligence."
elif roi >= 10:
    decision_class = "review"
    decision_text = "⚠️ Review — negotiate the price or reduce costs before proceeding."
else:
    decision_class = "stop"
    decision_text = "⛔ Below threshold — the current figures do not justify the risk."

st.markdown(
    f'<div class="decision {decision_class}">{decision_text}</div>',
    unsafe_allow_html=True,
)

chart_col, detail_col = st.columns([1.35, 1])

with chart_col:
    st.subheader("Where the money goes")
    labels = ["Purchase", "SDLT", "Renovation", "Contingency", "Buying", "Finance/holding", "Selling"]
    values = [purchase_price, sdlt, renovation, contingency, buying_costs, finance_costs, selling_costs]
    colours = ["#176B87", "#F4B942", "#18A999", "#8BD3C7", "#6C8CD5", "#A678DE", "#E88873"]
    fig = go.Figure(go.Pie(labels=labels, values=values, hole=0.58, marker_colors=colours))
    fig.update_layout(
        height=370,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        legend=dict(orientation="h", y=-0.12),
        annotations=[dict(text=money(total_cost), x=0.5, y=0.5, font_size=18, showarrow=False)],
    )
    st.plotly_chart(fig, use_container_width=True)

with detail_col:
    st.subheader("Deal breakdown")
    st.write(f"**Stamp Duty Land Tax:** {money(sdlt)}")
    st.write(f"**Renovation contingency:** {money(contingency)}")
    st.write(f"**Pre-tax profit:** {money(pre_tax_profit)}")
    st.write(f"**Estimated project tax:** {money(estimated_tax)}")
    st.write(f"**Break-even selling price:** {money(total_cost)}")
    target_sale = (
        total_cost * (1 + (target_roi / 100) / (1 - tax_rate / 100))
        if tax_rate < 100
        else 0
    )
    st.write(f"**Selling price needed for target:** {money(target_sale)}")
    st.markdown(
        '<p class="small-note">Figures are estimates for screening a deal, not legal, tax or valuation advice.</p>',
        unsafe_allow_html=True,
    )
