# FinGuard Elite - Real-Time Fraud Detection Intelligence

In the fast-paced world of fintech, **FinGuard Analytics** serves as a shield against digital theft. This project implements a high-fidelity fraud detection engine capable of identifying fraudulent patterns in real-time, despite the extreme challenge of highly imbalanced data.

## The Challenge (Problem Statement)
Financial fraud cases represent less than **0.2%** of all transactions. Standard machine learning models often fail by "missing" the fraud (High False Negatives) or slowing down the customer experience.

**The goal of FinGuard is twofold:**
1.  **High-Fidelity Detection:** Catching subtle fraudulent patterns in imbalanced data.
2.  **Real-Time Efficiency:** Maintaining a system latency of **< 50ms** to ensure a seamless customer journey.

## Key Features
* **Dual Intelligence Engines:** Choose between **XGBoost** (Customer-First approach) and an **ANN** (Security-First approach).
* **Responsive UI:** A professional dashboard built with Streamlit, optimized for both desktop and mobile viewing.
* **Dimensional Analysis:** Uses 28 PCA-transformed behavioral signals to detect digital signatures of fraud.
* **Privacy Preserving:** All features are PCA-transformed to protect sensitive user data.

## Model Performance & Trade-offs
FinGuard offers two distinct strategies to match different business risk appetites:

| Model | Strategy | Primary Benefit |
| :--- | :--- | :--- |
| **XGBoost:** Used for Customer-First. It has **High Precision** and  minimizes false alarms. Best for keeping genuine users moving fast. |
| **ANN:** Used for Security-First. It has **High Recall**. It caught **85%** of fraud in testing. Best for deep-scan security. |



## Tech Stack
* **Language:** Python
* **Framework:** Streamlit (Frontend Dashboard)
* **ML/DL:** XGBoost, TensorFlow/Keras (ANN), Scikit-Learn
* **Data Handling:** Pandas, NumPy, Joblib (Model Serialization)
* https://finguard-detection-system-1.onrender.com
