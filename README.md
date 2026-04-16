# Health Intelligence System

## 📌 Problem Statement

Modern health data (from wearables, apps, etc.) is abundant but **not actionable**. Users are often presented with raw metrics like steps, heart rate, or sleep duration without any meaningful interpretation.

The key problem this project solves is:

> How do we transform raw, noisy health data into **interpretable risk insights and actionable recommendations** in a structured, scalable way?

This project bridges that gap by combining **data engineering and machine learning**.

---

## 🚀 Solution Overview

This project is an **end-to-end health intelligence system** that:

1. Ingests and processes raw health data
2. Engineers meaningful physiological features
3. Uses a machine learning model to classify health risk
4. Stores predictions in a structured database
5. Presents insights through an interactive dashboard

The system is designed to simulate a **real-world production workflow**, not just a notebook-based model.

---

## 🧠 System Architecture

```
Raw Data → Feature Engineering → ML Model → PostgreSQL → Dashboard
                ↑
            Airflow Pipeline
```

---

## ⚙️ Data Engineering Component

The backbone of this project is a **data pipeline built using Airflow**, which ensures that data is processed consistently and automatically.

### 🔹 1. Data Ingestion

* Raw health-related data is loaded into the system
* Includes user-level time-series signals such as:

  * Sleep
  * Stress
  * Heart rate
  * Physical activity

---

### 🔹 2. Data Transformation & Feature Engineering

This is the **most critical part of the pipeline**.

Raw signals are transformed into meaningful features such as:

* `avg_sleep`
* `avg_stress`
* `avg_hr`
* `avg_steps`

Additional transformations include:

* Handling missing values
* Encoding categorical variables (e.g., gender)
* Time-based ordering for realistic training
* Normalization/scaling for model stability

A **composite health score** is also engineered to represent overall condition.

---

### 🔹 3. Data Storage (PostgreSQL)

Instead of working with temporary data:

* Processed features and predictions are stored in **PostgreSQL**
* This enables:

  * Persistent storage
  * Structured querying
  * Separation between pipeline and dashboard

This mirrors real-world systems where dashboards never rely on raw files.

---

### 🔹 4. Workflow Orchestration (Airflow)

Airflow is used to:

* Automate data processing steps
* Ensure correct execution order
* Enable repeatable and scalable workflows

This converts the project from:

```
scripts → system
```

---

## 🤖 Machine Learning Component

### 🔹 Model Type

* **Supervised Multi-class Classification**
* Predicts:

  * High Risk
  * Moderate Risk
  * Low Risk

---

### 🔹 Model Used

* **XGBoost Classifier**
* Chosen for:

  * High performance on tabular data
  * Ability to handle feature interactions
  * Robustness to noise

---

### 🔹 Training Strategy

* Time-based train-test split (avoids leakage)
* Feature scaling using StandardScaler
* Class imbalance handled using sample weights

---

### 🔹 Output

The model predicts **health risk category**, which is:

* Easier to interpret than raw numbers
* More actionable for users

---

## 📊 Dashboard (Streamlit)

The dashboard is designed to answer **real user questions**, not just display data.

<img width="1907" height="898" alt="Screenshot 2026-04-16 201920" src="https://github.com/user-attachments/assets/da31b580-f8f7-4208-bfe0-59d3f4b74d4f" />

<img width="1919" height="883" alt="Screenshot 2026-04-16 202020" src="https://github.com/user-attachments/assets/c9bec8b8-ab0a-4c5d-ae12-32fd63027d53" />

---

## 🛠️ Tech Stack

* **Python**
* **Airflow** – workflow orchestration
* **PostgreSQL** – data storage
* **XGBoost** – machine learning
* **Streamlit** – dashboard
* **Pandas / Scikit-learn** – data processing



