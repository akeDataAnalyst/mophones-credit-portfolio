# Credit Portfolio Health Monitor
**A Production-Grade Credit Analytics & Self-Service BI Solution**

---

## Project Overview

This project demonstrates the full end-to-end data analytics lifecycle for a fintech lending portfolio — from raw data to production-grade modeling and self-service BI dashboard. It closely mirrors the real challenges faced by MoPhones in managing credit risk while driving growth through device financing.

---

## Problem Statement

Credit teams often struggle with:
- Fragmented data across payment systems and credit bureaus
- Delayed identification of rising delinquency rates
- Lack of visibility into true default drivers (device model, promo campaigns, customer segments)
- Heavy dependency on analysts for every report
- No self-service access to key portfolio health metrics (PAR30, Vintage curves, etc.)

---

## Solution Delivered

I built a complete Credit Portfolio Health Monitoring System with four major components:

### 1. Data Foundation
- Generated realistic synthetic Kenyan fintech dataset (15,000 customers, 19k+ loans)
- Designed professional star schema in MySQL with proper indexing and relationships

### 2. dbt Data Transformation Layer
- Implemented modern ELT pipeline using dbt
- Created layered architecture: `Staging`, `Intermediate`, `Marts`
- Added data quality tests and documentation

### 3. Deep Credit Analytics
- Portfolio Overview KPIs
- Delinquency Metrics (PAR30, PAR60, PAR90)
- Vintage Analysis (most important credit KPI)
- Risk Segmentation (by location, income band, device model, promo)
- Device Performance Analysis

### 4. Self-Service BI Dashboard
- Interactive Streamlit dashboard with toggle buttons
- Real-time KPI cards
- Visualizations (Vintage trends, Risk heatmaps, Device performance)

---

## Tech Stack

| Layer                | Technology                          |
|----------------------|-------------------------------------|
| Database             | MySQL 8.0                           |
| Data Modeling        | dbt (Data Build Tool)               |
| Language             | Python 3                            |
| Dashboard            | Streamlit + Plotly                  |
| Data Access          | SQLAlchemy, pandas                  |
| Visualization        | Plotly Express                      |
| Environment          | Virtual Environment + dotenv        |

---

## Key Deliverables

- Production-grade dimensional modeling (Star Schema)
- Automated calculation of 30/60/90 DPD and Vintage Curves
- Self-service interactive dashboard with collapsible sections
- Data quality tests and documentation using dbt
- Clean, modular, and scalable code structure

---
Developed by Aklilu Abera | E2E Data Analyst
