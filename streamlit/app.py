"""
European Banking Customer Churn Analytics
Full Interactive Dashboard — Mahi Ahalawat © 2026
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from utils import get_theme, get_theme_names

# ══════════════════════════════════════════════════════════
# PAGE CONFIG
# ══════════════════════════════════════════════════════════
st.set_page_config(
    page_title="EU Banking Churn Analytics",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════
# CSS
# ══════════════════════════════════════════════════════════
def load_css():
    css_path = Path(__file__).parent / "assets" / "style.css"
    if css_path.exists():
        try:
            css_text = css_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            css_text = css_path.read_text(encoding="cp1252", errors="replace")
        st.markdown(f"<style>{css_text}</style>", unsafe_allow_html=True)

load_css()

# ══════════════════════════════════════════════════════════
# DATA
# ══════════════════════════════════════════════════════════
@st.cache_data
def load_data() -> pd.DataFrame:
    path = Path(__file__).parent.parent / "data" / "cleaned_bank_churn.csv"
    df = pd.read_csv(path)

    df["Age_Group"] = pd.cut(
        df["Age"],
        bins=[17, 30, 45, 60, float("inf")],
        labels=["18-30", "31-45", "46-60", "60+"]
    )
    df["Balance_Group"] = pd.cut(
        df["Balance"],
        bins=[-1, 0, 50_000, 150_000, float("inf")],
        labels=["Zero", "Low (<50k)", "High (50-150k)", "Premium (>150k)"]
    )
    df["Credit_Group"] = pd.cut(
        df["CreditScore"],
        bins=[0, 579, 669, 739, 850],
        labels=["Poor 579", "Fair 580-669", "Good 670-739", "Excellent 740+"]
    )
    df["Tenure_Group"] = pd.cut(
        df["Tenure"],
        bins=[-1, 2, 5, float("inf")],
        labels=["New (0-2 yrs)", "Mid (3-5 yrs)", "Long (6+ yrs)"]
    )
    df["Status"]       = df["Exited"].map({0: "Retained", 1: "Churned"})
    df["Active_Label"] = df["IsActiveMember"].map({1: "Active", 0: "Inactive"})
    df["CrCard_Label"] = df["HasCrCard"].map({1: "Has Card", 0: "No Card"})
    return df

df = load_data()

# ══════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════
with st.sidebar:

    st.markdown("""
    <div style="
        background: linear-gradient(135deg,#0C3A6B 0%,#1565C0 100%);
        margin: -1rem -1rem 1.2rem -1rem;
        padding: 22px 20px 18px 20px;
        border-bottom: 1px solid #1E3A5F;
    ">
        <div style="font-size:22px; font-weight:800; color:#F1F5F9; letter-spacing:-0.5px;">
            🏦 ChurnScope
        </div>
        <div style="font-size:11px; color:#93C5FD; margin-top:2px; letter-spacing:0.05em;">
            EUROPEAN BANKING ANALYTICS
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Theme — selectbox, no typing allowed by default
    st.markdown('<span class="filter-label">Dashboard Theme</span>', unsafe_allow_html=True)
    theme_name = st.selectbox(
        "theme_select",
        get_theme_names(),
        index=1,
        label_visibility="collapsed",
        key="theme_select",
    )
    theme        = get_theme(theme_name)
    PRIMARY      = theme["primary"]
    SECONDARY    = theme["secondary"]
    ACCENT       = theme["accent"]
    CHURN_COLOR  = theme["churn_color"]
    RETAIN_COLOR = theme["retain_color"]
    CHART_SEQ    = theme["chart_seq"]

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("**🔍 Segment Filters**")
    st.caption("Choose one option per filter.")

    all_countries = sorted(df["Geography"].unique())
    all_genders   = sorted(df["Gender"].unique())
    all_age       = list(df["Age_Group"].cat.categories)
    all_balance   = list(df["Balance_Group"].cat.categories)
    all_credit    = list(df["Credit_Group"].cat.categories)
    all_tenure    = list(df["Tenure_Group"].cat.categories)

    # All selectboxes — no free-text input, only pick from list
    sel_country = st.selectbox(
        "🌍 Geography",
        ["All countries"] + all_countries,
        index=0,
        key="f_country",
    )
    sel_gender = st.selectbox(
        "👤 Gender",
        ["All genders"] + all_genders,
        index=0,
        key="f_gender",
    )
    sel_age = st.selectbox(
        "🎂 Age Group",
        ["All age groups"] + all_age,
        index=0,
        key="f_age_group",
    )
    sel_balance = st.selectbox(
        "💰 Balance Segment",
        ["All segments"] + all_balance,
        index=0,
        key="f_balance_group",
    )
    sel_credit = st.selectbox(
        "📊 Credit Band",
        ["All bands"] + all_credit,
        index=0,
        key="f_credit_group",
    )
    sel_tenure = st.selectbox(
        "📅 Tenure Group",
        ["All tenures"] + all_tenure,
        index=0,
        key="f_tenure_group",
    )

    st.markdown("---")

    if st.button("🔄 Reset All Filters", use_container_width=True):
        for k in ["f_country","f_gender","f_age_group","f_balance_group","f_credit_group","f_tenure_group"]:
            if k in st.session_state:
                del st.session_state[k]
        st.rerun()

    # Resolve selections
    countries  = all_countries if sel_country == "All countries"  else [sel_country]
    genders    = all_genders   if sel_gender  == "All genders"    else [sel_gender]
    age_groups = all_age       if sel_age     == "All age groups" else [sel_age]
    bal_groups = all_balance   if sel_balance == "All segments"   else [sel_balance]
    cr_groups  = all_credit    if sel_credit  == "All bands"      else [sel_credit]
    ten_groups = all_tenure    if sel_tenure  == "All tenures"    else [sel_tenure]

    fdf = df[
        df["Geography"].isin(countries)   &
        df["Gender"].isin(genders)         &
        df["Age_Group"].isin(age_groups)   &
        df["Balance_Group"].isin(bal_groups) &
        df["Credit_Group"].isin(cr_groups) &
        df["Tenure_Group"].isin(ten_groups)
    ]

    n_active = sum([
        sel_country != "All countries",
        sel_gender  != "All genders",
        sel_age     != "All age groups",
        sel_balance != "All segments",
        sel_credit  != "All bands",
        sel_tenure  != "All tenures",
    ])

    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
    cm1, cm2 = st.columns(2)
    cm1.metric("Customers",  f"{len(fdf):,}")
    cm2.metric("Filters On", n_active)
    st.info(f"🎯 {n_active} filter(s) active") if n_active else st.success("Showing all customers")

# ══════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════
DARK_BG   = "#1A2130"
GRID_CLR  = "#1E2D40"
FONT_CLR  = "#CBD5E1"
TICK_CLR  = "#64748B"

DARK_AXES = dict(
    xaxis=dict(gridcolor=GRID_CLR, zerolinecolor=GRID_CLR, tickfont_color=TICK_CLR),
    yaxis=dict(gridcolor=GRID_CLR, zerolinecolor=GRID_CLR, tickfont_color=TICK_CLR),
)

def churn_by(col: str, data: pd.DataFrame) -> pd.DataFrame:
    g = data.groupby(col, observed=True)["Exited"].agg(["sum","count"]).reset_index()
    g.columns = [col, "Churned", "Total"]
    g["Retained"]       = g["Total"] - g["Churned"]
    g["Churn Rate (%)"] = (g["Churned"] / g["Total"] * 100).round(1)
    return g

def base_layout(fig, h=310, margin=None, extra=None):
    """Apply dark theme layout to any figure."""
    m = margin or dict(l=10, r=10, t=10, b=10)
    layout = dict(
        height=h, margin=m,
        plot_bgcolor=DARK_BG, paper_bgcolor=DARK_BG,
        font_family="Inter", font_color=FONT_CLR,
        **DARK_AXES,
    )
    if extra:
        layout.update(extra)
    fig.update_layout(**layout)
    return fig

def bar_chart(df_in, x, y="Churn Rate (%)", h=310, color_seq=None,
              orient="v", xlab=None, ylab=None):
    """
    Categorical bar chart using color_discrete_sequence (not continuous scale)
    so bars always render as solid filled rectangles regardless of row count.
    """
    if color_seq is None:
        color_seq = ["#2E7D32", "#F9A825", "#C62828", "#1565C0",
                     "#6D28D9", "#0E7490", "#92400E"]
    if orient == "h":
        fig = px.bar(
            df_in, x=y, y=x, orientation="h", text=y,
            color=x,
            color_discrete_sequence=color_seq,
            labels={x: xlab or x, y: ylab or y},
        )
    else:
        fig = px.bar(
            df_in, x=x, y=y, text=y,
            color=x,
            color_discrete_sequence=color_seq,
            labels={x: xlab or x, y: ylab or y},
        )
    fig.update_traces(
        texttemplate="%{text:.1f}%",
        textposition="outside",
        marker_line_width=0,
        showlegend=False,
    )
    base_layout(fig, h=h)
    # Give horizontal bars extra right margin for labels
    if orient == "h":
        max_val = df_in[y].max() if len(df_in) else 40
        fig.update_layout(
            margin=dict(l=10, r=60, t=10, b=10),
            xaxis=dict(
                range=[0, max_val * 1.3],
                gridcolor=GRID_CLR, zerolinecolor=GRID_CLR, tickfont_color=TICK_CLR,
            ),
        )
    return fig

def sec(title: str, sub: str = ""):
    st.markdown(
        f'<p class="sec-head" style="color:#CBD5E1">{title}</p>'
        + (f'<p class="sec-sub" style="color:#475569">{sub}</p>' if sub else ""),
        unsafe_allow_html=True,
    )

# ══════════════════════════════════════════════════════════
# HEADER
# ══════════════════════════════════════════════════════════
st.markdown(f"""
<div style="
    background: linear-gradient(135deg, {PRIMARY} 0%, {SECONDARY} 100%);
    border-radius: 18px; padding: 28px 36px; margin-bottom: 20px;
    display:flex; align-items:center; gap:20px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.15);
">
    <div style="font-size:48px; line-height:1;">🏦</div>
    <div>
        <div style="font-size:24px; font-weight:800; color:#fff; letter-spacing:-0.5px; line-height:1.2;">
            European Banking Customer Churn Analytics
        </div>
        <div style="font-size:13px; color:rgba(255,255,255,0.72); margin-top:5px; letter-spacing:0.04em;">
            Customer Segmentation &nbsp;·&nbsp; Churn Risk Intelligence &nbsp;·&nbsp; Financial Analytics
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

if len(fdf) == 0:
    st.error("No customers match the current filters. Please widen your selection.")
    st.stop()

# ══════════════════════════════════════════════════════════
# KPI ROW
# ══════════════════════════════════════════════════════════
total      = len(fdf)
churned    = int(fdf["Exited"].sum())
retained   = total - churned
churn_rate = churned / total * 100
avg_bal    = fdf["Balance"].mean()
active_pct = fdf["IsActiveMember"].mean() * 100

k1,k2,k3,k4,k5,k6 = st.columns(6)
k1.metric("👥 Total Customers", f"{total:,}")
k2.metric("❌ Churned",          f"{churned:,}")
k3.metric("✅ Retained",         f"{retained:,}")
k4.metric("📉 Churn Rate",       f"{churn_rate:.1f}%")
k5.metric("💰 Avg Balance",      f"${avg_bal:,.0f}")
k6.metric("⚡ Active Members",   f"{active_pct:.1f}%")

st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# TABS
# ══════════════════════════════════════════════════════════
tab_ov, tab_geo, tab_demo, tab_fin, tab_seg, tab_ins = st.tabs([
    "📊  Overview", "🌍  Geography", "👥  Demographics",
    "💰  Financial", "🗂️  Segments",  "💡  Insights",
])

# ─────────────────────────────────────────────────────────
#  TAB 1 — OVERVIEW
# ─────────────────────────────────────────────────────────
with tab_ov:
    c1, c2 = st.columns(2)

    with c1:
        sec("Churn vs Retained", "Overall customer status split")
        pie_df = fdf["Status"].value_counts().reset_index()
        pie_df.columns = ["Status","Count"]
        fig_pie = px.pie(
            pie_df, names="Status", values="Count", hole=0.58,
            color="Status",
            color_discrete_map={"Retained": RETAIN_COLOR, "Churned": CHURN_COLOR},
        )
        fig_pie.update_traces(
            textposition="inside", textinfo="percent+label",
            pull=[0, 0.06], marker_line_width=2, marker_line_color=DARK_BG,
        )
        base_layout(fig_pie, h=320, extra=dict(
            showlegend=True, legend_title="Status",
            annotations=[dict(
                text=f"<b>{churn_rate:.1f}%</b><br>Churn",
                x=0.5, y=0.5, font_size=18, showarrow=False, font_color=FONT_CLR,
            )]
        ))
        st.plotly_chart(fig_pie, use_container_width=True)

    with c2:
        sec("Churn by Number of Products", "Customers with 3-4 products show extreme attrition")
        prod = churn_by("NumOfProducts", fdf)
        st.plotly_chart(bar_chart(prod, "NumOfProducts", h=320), use_container_width=True)

    st.divider()
    c3, c4 = st.columns(2)

    with c3:
        sec("Active vs Inactive Members", "Inactivity is a leading churn predictor")
        act = churn_by("Active_Label", fdf)
        fig_act = px.bar(
            act, x="Active_Label", y="Churn Rate (%)",
            color="Active_Label", text="Churn Rate (%)",
            color_discrete_map={"Active": RETAIN_COLOR, "Inactive": CHURN_COLOR},
        )
        fig_act.update_traces(texttemplate="%{text:.1f}%", textposition="outside",
                               showlegend=False, marker_line_width=0)
        base_layout(fig_act, h=280, extra=dict(xaxis_title="Member Status"))
        st.plotly_chart(fig_act, use_container_width=True)

    with c4:
        sec("Credit Card Ownership vs Churn", "Card ownership has minimal protective effect")
        cc = churn_by("CrCard_Label", fdf)
        fig_cc = px.bar(
            cc, x="CrCard_Label", y="Churn Rate (%)",
            color="CrCard_Label", text="Churn Rate (%)",
            color_discrete_map={"Has Card": SECONDARY, "No Card": "#475569"},
        )
        fig_cc.update_traces(texttemplate="%{text:.1f}%", textposition="outside",
                              showlegend=False, marker_line_width=0)
        base_layout(fig_cc, h=280, extra=dict(xaxis_title="Credit Card Status"))
        st.plotly_chart(fig_cc, use_container_width=True)

# ─────────────────────────────────────────────────────────
#  TAB 2 — GEOGRAPHY
# ─────────────────────────────────────────────────────────
with tab_geo:
    geo = churn_by("Geography", fdf)

    c1, c2 = st.columns(2)

    with c1:
        sec("Churn Rate by Country", "Geographic risk exposure")
        # Sort ascending so highest churn appears at top in horizontal bar
        geo_sorted = geo.sort_values("Churn Rate (%)", ascending=True).reset_index(drop=True)

        # Assign traffic-light colours ranked by churn rate
        _palette   = ["#2E7D32", "#F57F17", "#C62828"]
        _n         = len(geo_sorted)
        _clr_map   = {
            row["Geography"]: _palette[min(i, len(_palette) - 1)]
            for i, row in enumerate(geo_sorted.to_dict("records"))
        }

        fig_geo = px.bar(
            geo_sorted,
            x="Churn Rate (%)", y="Geography",
            orientation="h",
            text="Churn Rate (%)",
            color="Geography",
            color_discrete_map=_clr_map,
        )
        fig_geo.update_traces(
            texttemplate="%{text:.1f}%",
            textposition="outside",
            marker_line_width=0,
            showlegend=False,
        )
        _max = geo_sorted["Churn Rate (%)"].max() if len(geo_sorted) else 40
        base_layout(fig_geo, h=300, margin=dict(l=10, r=60, t=10, b=10), extra=dict(
            xaxis=dict(
                range=[0, _max * 1.3],
                gridcolor=GRID_CLR, zerolinecolor=GRID_CLR, tickfont_color=TICK_CLR,
            ),
            yaxis=dict(
                gridcolor=GRID_CLR, zerolinecolor=GRID_CLR,
                tickfont_color=FONT_CLR, tickfont_size=13,
            ),
        ))
        st.plotly_chart(fig_geo, use_container_width=True)

    with c2:
        sec("Customer Volume by Country", "Churned vs retained stack")
        fig_stack = px.bar(
            geo, x="Geography", y=["Churned","Retained"], barmode="stack",
            color_discrete_map={"Churned": CHURN_COLOR, "Retained": RETAIN_COLOR},
            text_auto=True,
        )
        base_layout(fig_stack, h=300, extra=dict(
            legend_title="Status", yaxis_title="Customers",
        ))
        st.plotly_chart(fig_stack, use_container_width=True)

    st.divider()
    c3, c4 = st.columns(2)

    with c3:
        sec("Country x Age Group Churn Heatmap")
        heat_ga = (
            fdf.groupby(["Geography","Age_Group"], observed=True)["Exited"]
            .mean().mul(100).round(1).unstack()
        )
        fig_h = px.imshow(
            heat_ga,
            color_continuous_scale=["#2E7D32","#FFFDE7","#C62828"],
            text_auto=True, aspect="auto",
            labels={"color":"Churn %","x":"Age Group","y":"Country"},
        )
        base_layout(fig_h, h=280)
        st.plotly_chart(fig_h, use_container_width=True)

    with c4:
        sec("Country x Gender Churn Heatmap")
        heat_gg = (
            fdf.groupby(["Geography","Gender"], observed=True)["Exited"]
            .mean().mul(100).round(1).unstack()
        )
        fig_hg = px.imshow(
            heat_gg,
            color_continuous_scale=["#2E7D32","#FFFDE7","#C62828"],
            text_auto=True, aspect="auto",
            labels={"color":"Churn %","x":"Gender","y":"Country"},
        )
        base_layout(fig_hg, h=280)
        st.plotly_chart(fig_hg, use_container_width=True)

    sec("Churn Rate by Country & Tenure")
    geo_ten = (
        fdf.groupby(["Geography","Tenure_Group"], observed=True)["Exited"]
        .mean().mul(100).round(1).reset_index()
    )
    geo_ten.columns = ["Geography","Tenure Group","Churn Rate (%)"]
    fig_gt = px.bar(
        geo_ten, x="Tenure Group", y="Churn Rate (%)",
        color="Geography", barmode="group", text="Churn Rate (%)",
        color_discrete_sequence=CHART_SEQ,
    )
    fig_gt.update_traces(texttemplate="%{text:.1f}%", textposition="outside",
                         marker_line_width=0)
    base_layout(fig_gt, h=320, extra=dict(legend_title="Country"))
    st.plotly_chart(fig_gt, use_container_width=True)

# ─────────────────────────────────────────────────────────
#  TAB 3 — DEMOGRAPHICS
# ─────────────────────────────────────────────────────────
with tab_demo:
    c1, c2 = st.columns(2)

    with c1:
        sec("Churn Rate by Age Group", "46-60 cohort shows highest attrition risk")
        age = churn_by("Age_Group", fdf)
        st.plotly_chart(bar_chart(age, "Age_Group", h=300, xlab="Age Group"),
                        use_container_width=True)

    with c2:
        sec("Churn Rate by Gender", "Women churn at a higher rate than men")
        gen = churn_by("Gender", fdf)
        fig_gen = px.bar(
            gen, x="Gender", y="Churn Rate (%)",
            color="Gender", text="Churn Rate (%)",
            color_discrete_map={"Male":"#1E88E5","Female":"#E91E63"},
        )
        fig_gen.update_traces(texttemplate="%{text:.1f}%", textposition="outside",
                               showlegend=False, marker_line_width=0)
        base_layout(fig_gen, h=300)
        st.plotly_chart(fig_gen, use_container_width=True)

    st.divider()
    sec("Age Distribution - Churned vs Retained",
        "Churned customers cluster in the 40-55 age band")
    fig_hist = px.histogram(
        fdf, x="Age", color="Status", barmode="overlay", nbins=35,
        color_discrete_map={"Retained": RETAIN_COLOR, "Churned": CHURN_COLOR},
        opacity=0.72, labels={"Age":"Customer Age","count":"Customers"},
    )
    base_layout(fig_hist, h=300, extra=dict(legend_title="Status", bargap=0.04))
    st.plotly_chart(fig_hist, use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        sec("Churn Rate by Tenure Group")
        ten = churn_by("Tenure_Group", fdf)
        st.plotly_chart(bar_chart(ten, "Tenure_Group", h=280, xlab="Tenure"),
                        use_container_width=True)

    with c4:
        sec("Gender x Age Group Churn Heatmap")
        heat_dem = (
            fdf.groupby(["Gender","Age_Group"], observed=True)["Exited"]
            .mean().mul(100).round(1).unstack()
        )
        fig_hd = px.imshow(
            heat_dem,
            color_continuous_scale=["#2E7D32","#FFFDE7","#C62828"],
            text_auto=True, aspect="auto",
            labels={"color":"Churn %","x":"Age Group","y":"Gender"},
        )
        base_layout(fig_hd, h=280)
        st.plotly_chart(fig_hd, use_container_width=True)

# ─────────────────────────────────────────────────────────
#  TAB 4 — FINANCIAL
# ─────────────────────────────────────────────────────────
with tab_fin:
    c1, c2 = st.columns(2)

    with c1:
        sec("Churn Rate by Balance Segment", "Mid-high balance customers show elevated risk")
        bal = churn_by("Balance_Group", fdf)
        st.plotly_chart(bar_chart(bal, "Balance_Group", h=300, xlab="Balance Segment"),
                        use_container_width=True)

    with c2:
        sec("Churn Rate by Credit Score Band", "Poor credit slightly elevates churn risk")
        cr = churn_by("Credit_Group", fdf)
        st.plotly_chart(
            bar_chart(cr, "Credit_Group", h=300,
                      color_seq=["#C62828","#F9A825","#2E7D32","#1565C0"],
                      xlab="Credit Band"),
            use_container_width=True,
        )

    st.divider()
    c3, c4 = st.columns(2)

    with c3:
        sec("Balance Distribution - Churned vs Retained",
            "Churned customers hold significantly more in their accounts")
        fig_box = px.box(
            fdf[fdf["Balance"] > 0], x="Status", y="Balance",
            color="Status",
            color_discrete_map={"Retained": RETAIN_COLOR, "Churned": CHURN_COLOR},
            points="outliers", notched=True,
            labels={"Balance":"Account Balance ($)"},
        )
        fig_box.update_layout(showlegend=False)
        base_layout(fig_box, h=320)
        st.plotly_chart(fig_box, use_container_width=True)

    with c4:
        sec("Estimated Salary - Churned vs Retained",
            "Salary alone is not a strong churn predictor")
        fig_sal = px.violin(
            fdf, x="Status", y="EstimatedSalary",
            color="Status",
            color_discrete_map={"Retained": RETAIN_COLOR, "Churned": CHURN_COLOR},
            box=True, points=False,
            labels={"EstimatedSalary":"Estimated Annual Salary ($)"},
        )
        fig_sal.update_layout(showlegend=False)
        base_layout(fig_sal, h=320)
        st.plotly_chart(fig_sal, use_container_width=True)

    st.divider()
    sec("Premium Customer Churn (Balance > $150k)",
        "High-value customer loss represents the greatest revenue risk")
    hv       = fdf[fdf["Balance"] > 150_000]
    hv_total = len(hv)
    hv_churn = int(hv["Exited"].sum())
    hv_rate  = (hv_churn / hv_total * 100) if hv_total else 0
    hv_bal   = hv["Balance"].mean() if hv_total else 0

    h1,h2,h3,h4 = st.columns(4)
    h1.metric("Premium Customers",   f"{hv_total:,}")
    h2.metric("Premium Churned",     f"{hv_churn:,}")
    h3.metric("Premium Churn Rate",  f"{hv_rate:.1f}%")
    h4.metric("Avg Premium Balance", f"${hv_bal:,.0f}")

    if hv_total > 0:
        hv_geo = hv.groupby("Geography")["Exited"].mean().mul(100).round(1).reset_index()
        hv_geo.columns = ["Geography","Churn Rate (%)"]
        hv_sorted  = hv_geo.sort_values("Churn Rate (%)", ascending=True).reset_index(drop=True)
        _hv_clr    = {
            row["Geography"]: ["#2E7D32","#F57F17","#C62828"][min(i, 2)]
            for i, row in enumerate(hv_sorted.to_dict("records"))
        }
        fig_hv = px.bar(
            hv_sorted, x="Geography", y="Churn Rate (%)",
            color="Geography", text="Churn Rate (%)",
            color_discrete_map=_hv_clr,
            title="Premium Customer Churn Rate by Country",
        )
        fig_hv.update_traces(texttemplate="%{text:.1f}%", textposition="outside",
                             marker_line_width=0, showlegend=False)
        base_layout(fig_hv, h=280, margin=dict(l=10,r=10,t=36,b=10))
        st.plotly_chart(fig_hv, use_container_width=True)

# ─────────────────────────────────────────────────────────
#  TAB 5 — SEGMENTS
# ─────────────────────────────────────────────────────────
with tab_seg:
    sec("Multi-Dimensional Segment Churn Rates",
        "Bubble size = number of churned customers in that pocket")

    seg_grp = (
        fdf.groupby(["Geography","Age_Group"], observed=True)
        .agg(Total=("Exited","count"), Churned=("Exited","sum"))
        .reset_index()
    )
    seg_grp["Churn Rate (%)"] = (seg_grp["Churned"] / seg_grp["Total"] * 100).round(1)

    fig_bub = px.scatter(
        seg_grp,
        x="Age_Group", y="Geography",
        size="Churned", color="Churn Rate (%)",
        color_continuous_scale=["#2E7D32","#F9A825","#C62828"],
        size_max=60, text="Churn Rate (%)",
        labels={"Age_Group":"Age Group","Churn Rate (%)":"Churn %"},
        hover_data={"Total":True,"Churned":True,"Churn Rate (%)":":.1f"},
    )
    fig_bub.update_traces(texttemplate="%{text:.1f}%", textposition="top center")
    base_layout(fig_bub, h=360)
    st.plotly_chart(fig_bub, use_container_width=True)

    st.divider()
    c1, c2 = st.columns(2)

    with c1:
        sec("Churn Rate by Balance x Activity Status")
        bal_act = (
            fdf.groupby(["Balance_Group","Active_Label"], observed=True)["Exited"]
            .mean().mul(100).round(1).reset_index()
        )
        bal_act.columns = ["Balance Segment","Activity","Churn Rate (%)"]
        fig_ba = px.bar(
            bal_act, x="Balance Segment", y="Churn Rate (%)",
            color="Activity", barmode="group", text="Churn Rate (%)",
            color_discrete_map={"Active": RETAIN_COLOR, "Inactive": CHURN_COLOR},
        )
        fig_ba.update_traces(texttemplate="%{text:.1f}%", textposition="outside",
                              marker_line_width=0)
        base_layout(fig_ba, h=320, extra=dict(legend_title="Activity"))
        st.plotly_chart(fig_ba, use_container_width=True)

    with c2:
        sec("Churn Rate by Tenure x Geography")
        ten_geo = (
            fdf.groupby(["Tenure_Group","Geography"], observed=True)["Exited"]
            .mean().mul(100).round(1).reset_index()
        )
        ten_geo.columns = ["Tenure","Geography","Churn Rate (%)"]
        fig_tg = px.bar(
            ten_geo, x="Tenure", y="Churn Rate (%)",
            color="Geography", barmode="group", text="Churn Rate (%)",
            color_discrete_sequence=CHART_SEQ,
        )
        fig_tg.update_traces(texttemplate="%{text:.1f}%", textposition="outside",
                              marker_line_width=0)
        base_layout(fig_tg, h=320, extra=dict(legend_title="Country"))
        st.plotly_chart(fig_tg, use_container_width=True)

    st.divider()
    sec("Segment Summary Table", "Ranked by churn rate - use to prioritise retention")
    seg_full = (
        fdf.groupby(["Geography","Gender","Age_Group"], observed=True)
        .agg(
            Total=("Exited","count"),
            Churned=("Exited","sum"),
            Avg_Balance=("Balance","mean"),
            Avg_CreditScore=("CreditScore","mean"),
        )
        .reset_index()
    )
    seg_full["Churn Rate (%)"]  = (seg_full["Churned"] / seg_full["Total"] * 100).round(1)
    seg_full["Avg_Balance"]     = seg_full["Avg_Balance"].round(0).astype(int)
    seg_full["Avg_CreditScore"] = seg_full["Avg_CreditScore"].round(0).astype(int)
    seg_full = seg_full.sort_values("Churn Rate (%)", ascending=False).reset_index(drop=True)
    seg_full.index += 1
    seg_full.columns = ["Country","Gender","Age Group","Total","Churned",
                        "Avg Balance ($)","Avg Credit Score","Churn Rate (%)"]
    st.dataframe(
        seg_full.style.background_gradient(subset=["Churn Rate (%)"], cmap="RdYlGn_r"),
        use_container_width=True, height=380,
    )

# ─────────────────────────────────────────────────────────
#  TAB 6 — INSIGHTS
# ─────────────────────────────────────────────────────────
with tab_ins:
    sec("Key Business Insights", "Data-driven findings from the filtered customer population")

    geo_top   = churn_by("Geography", fdf).sort_values("Churn Rate (%)", ascending=False).iloc[0]
    age_top   = churn_by("Age_Group", fdf).sort_values("Churn Rate (%)", ascending=False).iloc[0]
    gen_top   = churn_by("Gender", fdf).sort_values("Churn Rate (%)", ascending=False).iloc[0]
    act_df    = churn_by("Active_Label", fdf)
    inactive_r = act_df[act_df["Active_Label"]=="Inactive"]["Churn Rate (%)"].values[0] if len(act_df) > 0 else 0
    active_r   = act_df[act_df["Active_Label"]=="Active"]["Churn Rate (%)"].values[0]   if len(act_df) > 0 else 1
    hv_count   = len(fdf[fdf["Balance"] > 150_000])
    hv_churn_r = (fdf[fdf["Balance"] > 150_000]["Exited"].mean() * 100) if hv_count else 0

    insights = [
        {
            "icon": "🌍",
            "title": f"Geographic Risk: {geo_top['Geography']} leads with {geo_top['Churn Rate (%)']:.1f}% churn",
            "body": f"{geo_top['Geography']} accounts for a disproportionate share of churned customers. "
                    "Targeted retention campaigns — personalised offers or dedicated relationship managers — "
                    "could meaningfully reduce overall attrition.",
            "tag": "High Priority", "tag_color": "#C62828",
        },
        {
            "icon": "🎂",
            "title": f"Age Risk: {age_top['Age_Group']} age band at {age_top['Churn Rate (%)']:.1f}% churn",
            "body": f"Customers aged {age_top['Age_Group']} are the highest-risk demographic. "
                    "This cohort may be evaluating competitors offering better rates or digital experiences. "
                    "Proactive outreach and product re-engagement programmes are recommended.",
            "tag": "High Priority", "tag_color": "#C62828",
        },
        {
            "icon": "⚡",
            "title": f"Engagement Gap: Inactive members churn at {inactive_r:.1f}% vs {active_r:.1f}% for active",
            "body": f"Inactive members are {(inactive_r / active_r):.1f}x more likely to churn. "
                    "An early-warning system that flags declining engagement and triggers re-engagement "
                    "workflows could be the single highest-ROI intervention.",
            "tag": "Actionable", "tag_color": "#1565C0",
        },
        {
            "icon": "👤",
            "title": f"Gender Gap: {gen_top['Gender']} customers churn at {gen_top['Churn Rate (%)']:.1f}%",
            "body": f"{gen_top['Gender']} customers show higher churn rates across most segments. "
                    "Product features, communication style, or service gaps may be contributing. "
                    "Segment-specific satisfaction surveys are recommended.",
            "tag": "Investigate", "tag_color": "#B45309",
        },
        {
            "icon": "💰",
            "title": f"Premium Risk: {hv_churn_r:.1f}% churn among {hv_count:,} high-balance customers",
            "body": "Each lost premium customer represents outsized revenue impact. "
                    "A dedicated relationship banking tier with proactive adviser contact is strongly recommended.",
            "tag": "Revenue Critical", "tag_color": "#4A1D96",
        },
        {
            "icon": "📦",
            "title": "Product Trap: Customers with 3-4 products show extreme churn",
            "body": "Counter-intuitively, customers holding more products churn at very high rates. "
                    "This may reflect cross-selling into products that do not fit customer needs. "
                    "A product suitability review and needs-based selling approach is recommended.",
            "tag": "Investigate", "tag_color": "#B45309",
        },
    ]

    for ins in insights:
        st.markdown(f"""
        <div style="background:#1A2130; border-radius:14px; border:1px solid #1E2D40;
                    padding:20px 24px; margin-bottom:14px;
                    border-left:5px solid {ins['tag_color']};
                    box-shadow:0 4px 16px rgba(0,0,0,0.35);">
            <div style="display:flex; align-items:center; gap:12px; margin-bottom:8px;">
                <span style="font-size:24px;">{ins['icon']}</span>
                <span style="font-size:15px; font-weight:700; color:#E2E8F0; flex:1;">{ins['title']}</span>
                <span style="background:{ins['tag_color']}18; color:{ins['tag_color']};
                             border:1px solid {ins['tag_color']}44; font-size:11px; font-weight:700;
                             padding:3px 10px; border-radius:20px; letter-spacing:0.05em;
                             white-space:nowrap;">{ins['tag']}</span>
            </div>
            <div style="font-size:13px; color:#64748B; line-height:1.65; padding-left:36px;">
                {ins['body']}
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    sec("Strategic Recommendations Summary")
    recs = [
        ("1", "Launch a Germany-first retention programme",              "Geographic risk mitigation"),
        ("2", "Build an engagement score & early-warning alert system",  "Highest-ROI single intervention"),
        ("3", "Create a dedicated Premium Banking tier (>$150k)",        "Revenue protection"),
        ("4", "Conduct gender-segmented satisfaction research",          "Root-cause investigation"),
        ("5", "Audit cross-selling practices for 3-4 product holders",   "Product fit improvement"),
        ("6", "Run age-targeted digital re-engagement campaigns (46-60)","Demographic retention"),
    ]
    for num, title, tag in recs:
        st.markdown(f"""
        <div style="display:flex; align-items:center; gap:16px;
                    background:#1A2130; border:1px solid #1E2D40;
                    border-radius:12px; padding:14px 20px; margin-bottom:10px;
                    box-shadow:0 4px 16px rgba(0,0,0,0.35);">
            <div style="width:32px; height:32px; border-radius:50%;
                        background:{PRIMARY}; color:white;
                        display:flex; align-items:center; justify-content:center;
                        font-size:13px; font-weight:800; flex-shrink:0;">{num}</div>
            <div style="flex:1;">
                <div style="font-size:14px; font-weight:600; color:#E2E8F0;">{title}</div>
                <div style="font-size:12px; color:#475569; margin-top:2px;">{tag}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════════
st.divider()
st.markdown(f"""
<div style="text-align:center; padding:14px 0 6px 0; font-size:13px; color:#334155;">
    <span style="color:{PRIMARY}; font-weight:700;">🏦 European Banking Churn Analytics</span>
    &nbsp;·&nbsp; Designed & Developed by <b style="color:#64748B;">Mahi Ahalawat</b>
    &nbsp;·&nbsp; Powered by <span style="color:{SECONDARY};">Streamlit & Plotly</span>
    &nbsp;·&nbsp; 2026
</div>
""", unsafe_allow_html=True)