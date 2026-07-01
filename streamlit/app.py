import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------------------
# Load Dataset
# -------------------------------------

@st.cache_data
def load_data():
    df = pd.read_csv("../data/cleaned_bank_churn.csv")
    return df

df = load_data()

# -------------------------------------
# Sidebar Filters
# -------------------------------------

st.sidebar.header("🔍 Filter Customers")

countries = st.sidebar.multiselect(
    "Geography",
    options=sorted(df["Geography"].unique()),
    default=sorted(df["Geography"].unique())
)

genders = st.sidebar.multiselect(
    "Gender",
    options=sorted(df["Gender"].unique()),
    default=sorted(df["Gender"].unique())
)

age_groups = st.sidebar.multiselect(
    "Age Group",
    options=sorted(df["Age"].unique()),
    default=sorted(df["Age"].unique())
)

balance_segments = st.sidebar.multiselect(
    "Balance Segment",
    options=sorted(df["Balance"].unique()),
    default=sorted(df["Balance"].unique())
)

filtered_df = df[
    (df["Geography"].isin(countries)) &
    (df["Gender"].isin(genders)) &
    (df["Age"].isin(age_groups)) &
    (df["Balance"].isin(balance_segments))
]

st.sidebar.markdown("---")

st.sidebar.metric(
    "Customers Selected",
    len(filtered_df)
)

st.subheader("Filtered Dataset")

# -------------------------------------
# Executive KPI Cards
# -------------------------------------

total_customers = len(filtered_df)

churned_customers = filtered_df["Exited"].sum()

retained_customers = total_customers - churned_customers

churn_rate = (churned_customers / total_customers) * 100 if total_customers > 0 else 0

retention_rate = 100 - churn_rate

total_balance = filtered_df["Balance"].sum()

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "👥 Total Customers",
    f"{total_customers:,}"
)

col2.metric(
    "❌ Churned",
    f"{churned_customers:,}"
)

col3.metric(
    "✅ Retained",
    f"{retained_customers:,}"
)

col4.metric(
    "📉 Churn Rate",
    f"{churn_rate:.2f}%"
)

col5.metric(
    "💰 Total Balance",
    f"${total_balance:,.0f}"
)

st.divider()

st.subheader("📊 Customer Churn Overview")

st.markdown("""
This dashboard provides an interactive overview of customer churn across demographic,
behavioral, and financial dimensions. Use the filters in the sidebar to explore
specific customer segments and analyze how churn varies across different groups.
""")


chart_df = filtered_df.copy()

chart_df["Exited"] = chart_df["Exited"].map({
    0: "Retained",
    1: "Churned"
})

fig = px.pie(
    chart_df,
    names="Exited",
    title="Overall Customer Churn Distribution",
    hole=0.55,
    color="Exited",
    color_discrete_map={
        "Retained": "#2E8B57",
        "Churned": "#DC143C"
    }
)

fig.update_traces(
    textinfo="percent+label"
)

st.plotly_chart(
    fig,
    use_container_width=True
)
