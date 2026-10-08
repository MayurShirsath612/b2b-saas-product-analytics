# NordicFlow CRM — B2B SaaS Product Analytics

An end-to-end **B2B SaaS product analytics pipeline** that transforms raw CRM and product telemetry data into a curated analytical model for business intelligence and product analytics.

The project follows a **Medallion Architecture** using **DuckDB and SQL** for data processing and transformation, with **Power BI and DAX** for semantic modeling, visualization, and analysis.

---

## 📌 Overview

NordicFlow CRM simulates a SaaS analytics environment where product usage, customer, subscription, and CRM data are transformed through multiple data layers to produce reliable datasets for reporting and decision-making.

The pipeline is designed to demonstrate a complete analytics workflow:

**Raw Data → Bronze → Silver → Gold → Power BI**

The final Gold-layer model is optimized for analytical queries and Power BI reporting, enabling analysis of areas such as:

- Customer retention and churn
- Product and feature engagement
- User activity
- Subscription and recurring revenue metrics
- Customer behavior
- SaaS product KPIs

---

## 🏗️ Architecture

The project follows a **Medallion Architecture**.

```text
                 ┌──────────────────────┐
                 │   Raw Data Sources   │
                 │   CSV / JSON Files   │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │    Bronze Layer      │
                 │ Raw / Ingested Data  │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │    Silver Layer      │
                 │ Cleaned & Enriched   │
                 │ Data                 │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │      Gold Layer      │
                 │ Curated Analytical   │
                 │ Model / Star Schema  │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │      Power BI        │
                 │ DAX + Semantic Model │
                 │ Dashboards & KPIs    │
                 └──────────────────────┘
```

### Bronze Layer

The Bronze layer contains the raw ingested CRM and SaaS telemetry data with minimal transformation.

**Purpose:**
- Preserve source data
- Maintain raw records
- Provide a reproducible ingestion layer

### Silver Layer

The Silver layer prepares the data for analytical use by applying data quality and transformation logic.

**Typical operations include:**
- Data cleansing
- Deduplication
- Standardization
- Filtering
- Data enrichment
- Schema transformation

### Gold Layer

The Gold layer contains curated business-ready datasets designed for analytical workloads.

The layer follows a **dimensional modeling approach / star schema**, making the data easier to consume from Power BI and improving analytical query performance.

---

## 📂 Project Structure

```text
b2b-saas-product-analytics/
│
├── data/
│   ├── raw/                         
│   │   └── # Raw SaaS telemetry & CRM extracts
│   │
│   └── duckdb/                      
│       └── nordicflow.duckdb        # DuckDB analytical database
│
├── sql/
│   ├── 01_bronze/                   
│   │   └── # Bronze ingestion scripts
│   │
│   ├── 02_silver/                   
│   │   └── # Silver transformation scripts
│   │
│   └── 03_gold/                     
│       └── # Gold dimensional modeling scripts
│
├── powerbi/
│   ├── nordicflow_crm.pbix          
│   └── screenshots/                 
│       └── # Dashboard screenshots
│
├── docs/                            
│   └── # Data dictionary & architecture documentation
│
└── README.md
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Data Storage / Processing | DuckDB |
| Data Transformation | SQL |
| Data Modeling | Dimensional Modeling / Star Schema |
| Semantic Modeling | DAX |
| Visualization | Power BI |
| Version Control | Git / GitHub |

---

## 🔄 Data Pipeline

The transformation workflow is executed sequentially:

```text
Raw CSV / JSON
      │
      ▼
Bronze Ingestion
      │
      ▼
Silver Transformation
      │
      ▼
Gold Curation
      │
      ▼
Power BI Semantic Model
      │
      ▼
Interactive Dashboards
```

Each layer has a clearly defined responsibility, making the pipeline modular and easier to maintain.

---

## 📊 Analytics & KPIs

The Power BI semantic model contains DAX measures designed to analyze SaaS product performance and customer behavior.

Example analytical metrics include:

### Revenue

- Monthly Recurring Revenue (MRR)
- Revenue trends
- Customer revenue contribution

### Customer

- Customer count
- Churn rate
- Retention
- Customer activity

### Product Usage

- Daily Active Users (DAU)
- User engagement
- Feature adoption
- Product usage trends

These measures allow stakeholders to analyze both **business outcomes** and **product behavior** from a single analytical model.

---

## 📈 Power BI Dashboard

The Power BI report provides an interactive interface for exploring the curated Gold-layer data.

The dashboard is designed to support questions such as:

- How is customer activity changing over time?
- What is the current churn rate?
- Which features have the highest engagement?
- How many users are actively using the product?
- How is recurring revenue changing?
- Which customer segments contribute the most revenue?
- Where are potential retention risks?

Screenshots of the report are available in:

```text
powerbi/screenshots/
```

---

## 🚀 Getting Started

### Prerequisites

Make sure the following tools are installed:

- [DuckDB](https://duckdb.org/)
- [Power BI Desktop](https://powerbi.microsoft.com/desktop/)
- Git

---

### 1. Clone the Repository

```bash
git clone https://github.com/MayurShirsath612/b2b-saas-product-analytics.git

cd b2b-saas-product-analytics
```

---

### 2. Create / Initialize the DuckDB Database

The project uses DuckDB as the analytical database.

```bash
duckdb data/duckdb/nordicflow.duckdb
```

---

### 3. Run the Bronze Layer

Execute the Bronze ingestion scripts first.

```bash
duckdb data/duckdb/nordicflow.duckdb \
-c ".read sql/01_bronze/bronze_ingest.sql"
```

---

### 4. Run the Silver Layer

After Bronze processing is complete, execute the Silver transformation logic.

```bash
duckdb data/duckdb/nordicflow.duckdb \
-c ".read sql/02_silver/silver_transform.sql"
```

---

### 5. Run the Gold Layer

Finally, build the curated analytical model.

```bash
duckdb data/duckdb/nordicflow.duckdb \
-c ".read sql/03_gold/gold_curate.sql"
```

The resulting Gold-layer tables can then be consumed by Power BI.

---

## 🔎 Validation

Before connecting the database to Power BI, validate the pipeline by checking:

```sql
SELECT COUNT(*)
FROM <gold_table>;
```

and inspecting the resulting Gold-layer tables for:

- Unexpected duplicates
- Missing values
- Invalid keys
- Incorrect date ranges
- Unexpected record counts

This ensures the final analytical layer is suitable for reporting.

---

## 📊 Connect to Power BI

1. Open:

```text
powerbi/nordicflow_crm.pbix
```

2. Configure the DuckDB data source.

3. Point Power BI to:

```text
data/duckdb/nordicflow.duckdb
```

4. Refresh the semantic model.

5. Explore the dashboards and DAX measures.

---

## 🎯 Project Objectives

This project demonstrates the implementation of a complete analytics workflow rather than simply creating a dashboard.

The key objectives are:

**Data Engineering**

Build a structured Bronze → Silver → Gold transformation pipeline using SQL and DuckDB.

**Data Modeling**

Transform operational-style CRM and telemetry data into a curated dimensional model suitable for analytical workloads.

**Business Intelligence**

Create a Power BI semantic model with DAX measures for SaaS KPIs.

**Product Analytics**

Analyze customer behavior, product engagement, retention, churn, and recurring revenue.

---

## 💡 Key Takeaways

The project demonstrates how raw SaaS data can be transformed into business-ready insights through a structured analytical architecture:

```text
Raw Data
   ↓
Data Ingestion
   ↓
Data Cleaning & Transformation
   ↓
Dimensional Modeling
   ↓
Semantic Layer
   ↓
Business Intelligence
   ↓
Product & Customer Insights
```

This architecture provides a foundation that can be extended with additional data sources, KPIs, models, and reporting requirements.

---

## 📁 Documentation

Additional project documentation can be found in:

```text
docs/
```

This includes supporting materials such as:

- Data dictionary
- Architecture documentation
- Data model information

---

## 👤 Author

**Mayur Shirsath**

GitHub:  
[github.com/MayurShirsath612](https://github.com/MayurShirsath612)

Project Repository:  
[github.com/MayurShirsath612/b2b-saas-product-analytics](https://github.com/MayurShirsath612/b2b-saas-product-analytics)

---

## ⭐ Project Summary

**NordicFlow CRM** is a portfolio project demonstrating an end-to-end **B2B SaaS Product Analytics and Business Intelligence pipeline** using:

**DuckDB + SQL + Dimensional Modeling + DAX + Power BI**

The project covers the complete path from raw product and CRM data to a curated analytical model and interactive BI reporting. 
