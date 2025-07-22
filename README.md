# Data Management Project: End-to-End System for Fictional Gym Chain

This repository contains a comprehensive data management project developed for the **Data Management** module of the MSc Business Analytics programme at Warwick Business School. The goal was to simulate the creation of a full-scale data product for a fictional gym company operating across the West Midlands in the UK.

---

## 📂 Repository Contents

- [**`1_member_payment_checkins.py`**](./1_member_payment_checkins.py): Generates and manages member records, membership payments, and check-in/out data.
- [**`2_sessions.py`**](./2_sessions.py): Synthesizes class session data based on trainer availability, business rules, and scheduling logic.
- [**`3_attendance.py`**](./3_attendance.py): Allocates session attendance and simulates member behavior and class feedback.
- [**`4_format.py`**](./4_format.py): Formats and standardizes raw tables into final, clean CSV files.
- [**`SQL_DDL_Queries.py`**](./SQL_DDL_Queries.py): SQLite DDL queries and data ingestion pipeline for loading all tables into the database.
- [**`Data_management_final_report.pdf`**](./Data_management_final_report.pdf): Final project report summarising design choices, schema, data generation methods, and insights.

---

## 🏋️ Business Scenario

We built a fictional but realistic **gym chain** focused on offering a variety of fitness classes and memberships across the West Midlands. The data product was designed to:
- Track **memberships**, **payments**, and **class attendance**
- Support **performance insights** per gym branch
- Analyse **seasonal trends**, **trainer utilization**, and **member churn**

---

## 🛠️ Database Schema Overview

The relational database was implemented in SQLite and consists of the following key tables:

| Table Name          | Description |
|---------------------|-------------|
| `Branch`            | Locations with city, address, and opening date |
| `Members`           | Member details and home branch |
| `Memberships`       | Payment and plan information |
| `Trainers`          | Trainer profiles and specialisations |
| `Class`             | Types and durations of classes offered |
| `Class_Sessions`    | Scheduled sessions at branches |
| `CheckIns`          | Member gym visit data |
| `Class_Attendance`  | Member participation and feedback ratings |
| `Membership_Type`   | Plan categories and prices |

Referential integrity and constraints (e.g. date formats, uniqueness, cardinality) were strictly enforced.

---

## 🧪 Synthetic Data Generation

Python scripts were used to generate realistic data:
- Each focus entity contains at least **500 records**
- Temporal logic governs availability, join dates, and class scheduling
- **Attendance rates** vary by class type (e.g., Cardio has high attendance, Strength lower)
- Ratings simulate noisy real-world behavior, with random nulls and biases introduced

---

## 📈 Business Insights & Reporting

Advanced SQL queries were developed to provide business intelligence including:

- 📊 **Membership Sales by Branch and Year**
- 💸 **Total Revenue by Membership Type**
- 🏋️ **Class Popularity across Branches**
- 📅 **Seasonal Check-in Trends**
- 🚨 **Churn Analysis** by membership type and branch
- ⭐ **Visit Ratings and Feedback**

These reports allow stakeholders to monitor operational performance, design better membership offerings, and optimize staffing or capacity planning.

---

## 📎 How to Use This Repository

1. Run the Python scripts sequentially (`1_` to `4_`) to prepare all final CSV files.
2. Use `SQL_DDL_Queries.py` to:
   - Create database schema
   - Load generated CSV data
   - Execute business insight queries
3. Refer to the final report for diagrams, assumptions, and query interpretation.

---

## 💡 Highlights

- Enforced **normalized schema** with logical entity relationships
- Data logic includes capacity constraints, session conflicts, realistic ratings
- Fully **automated pipeline** from schema creation → data generation → report outputs

---

## 📬 Contact

Feel free to connect with me on [LinkedIn](https://www.linkedin.com/in/benjamin-sachse-consultant/) or reach out if you'd like to discuss this project, database design, or synthetic data pipelines.
