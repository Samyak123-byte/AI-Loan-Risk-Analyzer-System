# 🏦 AI Loan Risk Analyzer System

An intelligent, end-to-end **Loan Approval & Risk Analysis System** built using **Machine Learning + Flask + AI Chatbot**.

This project simulates a real-world banking workflow with **role-based access**, **loan prediction**, **analytics dashboard**, and a **smart AI assistant**.

---

## 🚀 Features

### 🔐 Role-Based Authentication

* 👤 **Admin** → Access dashboard & analytics
* 🧑‍💼 **Loan Officer** → Submit loan applications
* 👨 **User** → Apply for loan

---

### 🤖 Machine Learning Prediction

* Predicts loan approval using trained model
* Uses features like:

  * Income
  * Loan Amount
  * Credit History
  * Employment Type
* Displays:

  * ✅ Approval / Rejection
  * 📊 Probability Score

---

### 🧠 Explainable AI

* Provides reasons for decision:

  * Low income
  * Poor credit history
  * High loan amount

---

### 📊 Admin Dashboard

* Total applications
* Approved vs Rejected
* Interactive charts (Chart.js)
* Application history table

---

### 🤖 AI Chatbot (Smart Assistant)

* Integrated AI chatbot for loan advice
* Provides:

  * Personalized suggestions
  * Financial guidance
  * Explanation of results

---

### 🗄️ Database Integration

* SQLite database stores:

  * User accounts
  * Loan applications
  * Prediction results

---

## 🛠️ Tech Stack

* **Frontend:** HTML, CSS, JavaScript
* **Backend:** Flask (Python)
* **Machine Learning:** Scikit-learn
* **Database:** SQLite
* **Visualization:** Chart.js
* **AI Integration:** OpenAI API

---

## 📁 Project Structure

```
project/
│
├── app.py
├── train_model.py
├── model.pkl
├── scaler.pkl
├── accuracy.txt
│
├── loan.db
│
├── templates/
│   ├── login.html
│   ├── index.html
│   ├── officer.html
│   ├── apply.html
│   ├── dashboard.html
│
├── static/
│   └── style.css
│
└── README.md
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository

```
git clone https://github.com/your-username/loan-system.git
cd loan-system
```

---

### 2️⃣ Install dependencies

```
pip install flask numpy pandas scikit-learn openai python-dotenv
```

---

### 3️⃣ Train the model

```
python train_model.py
```

---

### 4️⃣ Run the application

```
python app.py
```

---

### 5️⃣ Open in browser

```
http://127.0.0.1:5000
```

---

## 🔑 Default Login Credentials

| Role    | Username | Password   |
| ------- | -------- | ---------- |
| Admin   | admin    | admin123   |
| Officer | officer  | officer123 |
| User    | user     | user123    |

---

## 📊 Machine Learning Details

* Algorithm: **Random Forest Classifier**
* Accuracy: Stored in `accuracy.txt`
* Features used:

  * Gender
  * Married
  * Age
  * Employment Type
  * Property Area
  * Income
  * Loan Amount
  * Credit History

---

## 🤖 Chatbot Integration

* Uses OpenAI API
* Context-aware (uses last prediction data)
* Provides:

  * Loan advice
  * Risk explanation
  * Improvement suggestions

---

## 🔥 Future Enhancements

* 📄 PDF Report Generation
* 📧 Email Notification System
* 🔐 Secure Password Hashing
* 📊 Advanced Analytics Dashboard
* 🌐 Cloud Deployment (AWS / Render)
* 🧠 SHAP-based Explainable AI

---

## 🎯 Project Objective

To build an **AI-powered loan decision support system** that:

* Automates loan approval prediction
* Provides transparency using explainable AI
* Enhances user interaction through chatbot assistance
* Simulates real-world banking workflow

---

## 👨‍💻 Author

**Samyak Jain**

---

## ⭐ Conclusion

This project demonstrates the integration of:

* Machine Learning
* Web Development
* Database Management
* AI-based interaction

👉 Making it a **complete real-world software system** rather than just a model.

---
