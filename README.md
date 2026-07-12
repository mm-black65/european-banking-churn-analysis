# 🏦 Customer Segmentation & Churn Pattern Analytics in European Banking

An end-to-end Banking Analytics and Business Intelligence project developed as part of the **Machine Learning Internship at Unified Mentor**.

The project focuses on customer segmentation, churn pattern analysis, executive KPI reporting, and interactive business intelligence dashboards to support strategic decision-making in retail banking.

---

## 📌 Project Overview

Customer churn is one of the most significant challenges in retail banking. Acquiring new customers is substantially more expensive than retaining existing ones, making churn analysis a critical business function.

This project analyzes customer demographics, financial behavior, and engagement metrics to answer key business questions such as:

- Which customer segments are most likely to churn?
- How does churn vary across different European countries?
- Which age groups contribute the highest churn?
- Are premium customers at greater financial risk?
- How do customer activity and product ownership influence churn?
- Which regions require immediate retention strategies?

---

## 🎯 Objectives

- Measure overall customer churn rate
- Perform customer segmentation analysis
- Compare churn across countries and demographics
- Analyze high-value customer churn
- Evaluate customer engagement and tenure patterns
- Develop executive KPIs for decision makers
- Build an interactive Streamlit Business Intelligence dashboard

---

## 📊 Dashboard Features

### Executive Dashboard

- Executive KPI cards
- Customer churn overview
- Customer retention summary
- Average balance analysis
- Active customer percentage
- Dynamic business insights

### Geography Analytics

- Country-wise churn comparison
- Customer distribution by country
- Country × Age heatmap
- Country × Gender heatmap
- Country × Tenure analysis

### Demographic Analytics

- Age Group analysis
- Gender comparison
- Credit Score segmentation
- Customer activity analysis
- Product ownership analysis

### Financial Analytics

- Balance distribution
- Salary analysis
- Premium customer identification
- High-value customer churn
- Revenue risk estimation

### Customer Segmentation

- Geographic segmentation
- Age segmentation
- Credit Score bands
- Balance segmentation
- Tenure segmentation

### Interactive Features

- Multi-level filtering
- Dynamic KPI updates
- Interactive Plotly visualizations
- Executive business insights
- Professional dark theme UI

---

## 📁 Project Structure

```
European-Banking-Churn-Analytics/
│
├── data/
│   ├── European_Bank.csv
│   ├── cleaned_bank_churn.csv
│   └── analysis figures
│
├── notebook/
│   ├── 01_data_cleaning.ipynb
│   ├── 02_eda.ipynb
│   ├── 03_churn_analysis.ipynb
│   ├── 04_customer_seg.ipynb
│   └── 05_kpi_executive_analytics.ipynb
│
├── streamlit/
│   ├── app.py
│   ├── utils.py
│   ├── assets/
│   │    └── style.css
│   └── pages/
│        ├── executive_kpis.csv
│        ├── overall_kpis.csv
│        ├── financial_kpis.csv
│        └── geographic_risk.csv
│
├── requirements.txt
└── README.md
```

---

## 📈 Analytical Workflow

### 1. Data Ingestion & Validation

- Dataset loading
- Missing value verification
- Duplicate detection
- Data type validation
- Binary variable consistency checks

### 2. Data Cleaning

- Removed non-analytical attributes
- Data validation
- Feature engineering
- Segmentation variable creation

### 3. Exploratory Data Analysis

- Customer demographics
- Financial distribution
- Churn visualization
- Correlation analysis
- Feature relationship exploration

### 4. Customer Segmentation

- Geography
- Age Groups
- Credit Score Bands
- Balance Segments
- Tenure Groups

### 5. Churn Analytics

- Overall churn rate
- Segment-wise churn
- Customer profile comparison
- Geographic risk exposure
- Financial impact assessment

### 6. Executive KPI Analytics

- Overall Churn Rate
- High Value Customer Ratio
- Geographic Risk Index
- Customer Engagement
- Financial Exposure
- Executive Business KPIs

### 7. Interactive Dashboard

- Real-time filtering
- Interactive charts
- Executive insights
- Business Intelligence reporting

---

## 📊 Technologies Used

- Python
- Pandas
- NumPy
- Plotly
- Streamlit
- Matplotlib
- Seaborn
- Jupyter Notebook

---

## 📷 Dashboard Preview

### Executive Dashboard

> *(Insert dashboard screenshot here)*

### Geographic Analytics

> *(Insert dashboard screenshot here)*

### Customer Segmentation

> *(Insert dashboard screenshot here)*

---

## 🚀 Installation

Clone the repository

```bash
git clone https://github.com/yourusername/european-banking-churn-analysis.git
```

Move into the project directory

```bash
cd european-banking-churn-analysis
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the Streamlit application

```bash
cd streamlit

streamlit run app.py
```

---

## 📖 How to Use

1. Launch the Streamlit dashboard.
2. Select customer filters from the sidebar.
3. Explore executive KPIs.
4. Navigate through dashboard sections using the tabs.
5. Analyze customer churn across geography, demographics, financial metrics, and customer segments.
6. Use interactive charts to identify high-risk customer groups and business opportunities.

---

## 💼 Business Insights

The analysis reveals several strategic findings:

- Germany exhibits the highest customer churn rate.
- Middle-aged customers contribute disproportionately to churn.
- Inactive members show significantly higher churn probability.
- Customers owning three or more products experience elevated churn.
- Premium customers represent substantial financial exposure despite smaller population size.
- Geographic and demographic segmentation enables targeted retention campaigns.

---

## 📌 Business Recommendations

- Prioritize customer retention initiatives in Germany.
- Improve engagement among inactive members.
- Develop personalized retention programs for premium customers.
- Strengthen onboarding strategies for new customers.
- Promote cross-selling for customers with limited product adoption.
- Implement proactive churn monitoring using executive KPIs.

---

## 📚 Future Enhancements

- Machine Learning based churn prediction
- Customer Lifetime Value (CLV) estimation
- Churn probability scoring
- Real-time banking dashboard
- SQL integration
- Cloud deployment
- Automated reporting
- Power BI integration

---

## 👨‍💻 Developed By

**Mahi Ahalawat**

Machine Learning Intern — Unified Mentor

GitHub: https://github.com/mm-black65

Portfolio: https://mahiportfolio-five.vercel.app/

---

## License

This project is developed for educational and analytical purposes.
