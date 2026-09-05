# Customer Segmentation & Churn Pattern Analytics in European Banking

## Live Demo

🔗 **Dashboard:** [Your Streamlit Dashboard](https://banking-churn-analysis.streamlit.app/)

> An interactive dashboard for exploring customer churn patterns, customer segments, geographic risk, financial behavior, and engagement trends across European banking customers.

---

## Overview

Customer churn is a critical challenge in the banking sector. When customers leave a bank, it results in reduced revenue, lower customer lifetime value, and increased customer acquisition costs. Understanding why customers leave and identifying high-risk customer groups is essential for developing effective retention strategies.

This project focuses on analyzing customer churn patterns in European banking using customer demographic, financial, and engagement data. Through segmentation-driven analytics, the project aims to uncover actionable insights that can help banks make data-driven business decisions and improve customer retention.

---

## Problem Statement

Although banks collect extensive customer data, they often struggle to answer important questions such as:

* Which customer segments are most likely to churn?
* How does churn vary across countries, age groups, and financial profiles?
* Are high-value customers leaving the bank?
* What role do customer activity and tenure play in churn behavior?

Without structured analytics, retention strategies remain reactive and less effective. This project addresses these challenges through comprehensive exploratory data analysis and customer segmentation.

---

## Objectives

### Primary Objectives

* Measure the overall customer churn rate.
* Analyze churn distribution across customer segments.
* Compare churn behavior across European regions.

### Secondary Objectives

* Understand churn among high-value customers.
* Evaluate engagement and tenure patterns.
* Support strategic planning and marketing decisions through data-driven insights.

---

## Dataset Description

The dataset contains customer-level information from a European bank.

| Column          | Description                                 |
| --------------- | ------------------------------------------- |
| CustomerId      | Unique customer identifier                  |
| Surname         | Customer surname                            |
| CreditScore     | Customer creditworthiness score             |
| Geography       | Customer country (France, Germany, Spain)   |
| Gender          | Male or Female                              |
| Age             | Customer age                                |
| Tenure          | Number of years with the bank               |
| Balance         | Account balance                             |
| NumOfProducts   | Number of bank products used                |
| HasCrCard       | Credit card ownership status                |
| IsActiveMember  | Customer activity indicator                 |
| EstimatedSalary | Estimated annual salary                     |
| Exited          | Churn indicator (0 = Retained, 1 = Churned) |

---

## Project Workflow

The project follows a structured analytics pipeline:

1. Data Collection and Validation
2. Data Cleaning and Preparation
3. Exploratory Data Analysis (EDA)
4. Customer Segmentation
5. Churn Distribution Analysis
6. KPI Generation
7. Dashboard Development
8. Business Insights and Recommendations

---

## Customer Segmentation Strategy

### Geographic Segmentation

* France
* Germany
* Spain

### Age Segmentation

* Below 30 Years
* 30–45 Years
* 46–60 Years
* Above 60 Years

### Credit Score Segmentation

* Low Credit Score
* Medium Credit Score
* High Credit Score

### Tenure Segmentation

* New Customers
* Mid-Term Customers
* Long-Term Customers

### Balance Segmentation

* Zero Balance Customers
* Low Balance Customers
* High Balance Customers

---

## Key Performance Indicators (KPIs)

The following KPIs are used to evaluate churn behavior:

* Overall Churn Rate
* Segment Churn Rate
* High-Value Customer Churn Ratio
* Geographic Risk Index
* Engagement Drop Indicator
* Customer Activity Rate
* Average Customer Balance

---

## Features

* Customer churn analysis
* Customer segmentation by demographics and financial profile
* Geography-wise churn comparison
* Age and tenure-based churn insights
* High-value customer churn exploration
* Interactive Streamlit dashboard
* Dynamic KPI tracking and visualization
* Data-driven business recommendations

---

## Project Structure

```text
customer-segmentation-churn-analytics/
│
├── data/
│   └── Churn_Modelling.csv
│   └── assets/
│       ├── img1 (1).png
│       ├── img1 (2).png
│       └── img1 (3).png
├── notebooks/
│   ├── 01_data_cleaning.ipynb
│   ├── 02_exploratory_data_analysis.ipynb
│   ├── 03_customer_segmentation.ipynb
│   └── 04_churn_analysis.ipynb
│
├── dashboard/
│   └── app.py
│
├── images/
│   └── dashboard_preview.png
│
├── reports/
│   ├── research_paper.pdf
│   └── executive_summary.pdf
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Installation

### Clone the Repository

```bash
git clone https://github.com/your-username/customer-segmentation-churn-analytics.git

cd customer-segmentation-churn-analytics
```

### Create a Virtual Environment

```bash
python -m venv venv
```

### Activate the Virtual Environment

**Windows**

```bash
venv\Scripts\activate
```

**Linux / macOS**

```bash
source venv/bin/activate
```

### Install Required Dependencies

```bash
pip install -r requirements.txt
```

---

## How to Run the Dashboard

Launch the Streamlit application:

```bash
streamlit run dashboard/app.py
```

After running the command, open the following URL in your browser:

```text
http://localhost:8501
```

---

## Technologies Used

* Python
* Pandas
* NumPy
* Matplotlib
* Seaborn
* Plotly
* Streamlit
* Jupyter Notebook
* Git & GitHub

---

## Expected Outcomes

This project aims to:

* Identify customer segments with the highest churn risk.
* Compare churn behavior across countries and demographics.
* Evaluate churn among high-value customers.
* Provide actionable recommendations for customer retention.
* Support business decision-making through data analytics.

---

## Future Enhancements

Potential future improvements include:

* Machine Learning-based churn prediction
* Customer Lifetime Value (CLV) analysis
* Advanced customer clustering techniques
* Automated churn risk scoring
* Real-time dashboard integration
* Personalized retention strategy recommendations

---

## 📊 Dashboard & Analytics Preview

The interactive **ChurnScope** dashboard provides multiple analytical views for exploring customer churn across demographic, geographic, financial, and engagement dimensions.

### 🏦 Overview & KPI Dashboard

The overview provides a high-level snapshot of customer churn, retention, average balance, and activity levels. It also highlights the highest-risk customer segments and allows users to filter the analysis dynamically.

<img src="data/assets/img1%20(1).png" alt="ChurnScope Overview Dashboard" width="100%">

**Key capabilities:**
- 📈 Overall churn and retention KPIs
- 👥 Total, churned, and retained customers
- 💰 Average customer balance
- ⚡ Active member percentage
- 🎯 High-risk segment identification
- 📦 Churn analysis by number of products

---

### 🌍 Geographic & Demographic Analysis

The geographic view compares churn rates across **France, Germany, and Spain**, while heatmaps reveal how churn changes across age groups and gender within each country.

<img src="data/assets/img1%20(2).png" alt="Geographic and Demographic Churn Analysis" width="100%">

**Key insights explored:**
- 🌍 Country-level churn rate
- 👥 Customer volume by country
- 🔥 Country × Age Group churn
- 🚻 Country × Gender churn
- 📊 Geographic risk exposure

---

### 🎯 Multi-Dimensional Customer Segmentation

The segmentation view combines multiple customer attributes to identify high-risk customer pockets. Bubble size represents the number of churned customers, allowing high-risk segments to be identified more easily.

<img src="data/assets/img1%20(3).png" alt="Multi-Dimensional Customer Segmentation" width="100%">

**Segmentation dimensions include:**
- 🎂 Age Group
- 🌍 Geography
- 💰 Balance Segment
- ⚡ Activity Status
- 📅 Tenure
- 💳 Financial profile

This enables deeper analysis of **which combinations of customer characteristics are associated with elevated churn risk**.

---

### 🔎 Analytical Views

The dashboard is organized into multiple interactive sections:

| Dashboard View | Purpose |
|---|---|
| 📊 Overview | Monitor overall churn and key KPIs |
| 🌍 Geography | Compare churn across countries |
| 👥 Demographics | Analyze age and gender patterns |
| 💰 Financial | Explore balance and product-related churn |
| 📁 Segments | Identify high-risk customer combinations |
| 💡 Insights | Translate analytical findings into business recommendations |

## Author

**Mahi Ahalawat**

Data Analytics Project – Customer Segmentation & Churn Pattern Analytics in European Banking

---

## License

This project is developed for educational and analytical purposes.
