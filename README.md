# Smart Expense Platform 💰

A multi-user personal finance analytics platform built with Python, FastAPI, MySQL, Streamlit, Pandas and Scikit-learn.

The application allows users to manage and analyze their expenses, create budgets, identify unusual spending patterns and forecast future expenses.

## Features

### 🔐 User Authentication
- User registration and login
- Secure password hashing using bcrypt
- Separate financial data for each user

### 📊 Expense Analytics
- Total income and expenses
- Savings calculation
- Savings percentage
- Category-wise spending
- Monthly spending trends
- Top merchants

### 📁 Transaction Management
- Manual transaction management
- CSV and Excel upload
- Automatic data cleaning
- Automatic transaction categorization
- Duplicate transaction prevention

### 💰 Budget Management
- Create monthly budgets by category
- Compare budget against actual spending
- Calculate remaining budget
- Track budget usage percentage
- Identify exceeded budgets

### 🚨 Spending Anomaly Detection
Uses Isolation Forest from Scikit-learn to identify unusually high transactions compared with a user's normal spending pattern.

### 📈 Expense Forecasting
Uses Linear Regression to estimate next month's expenses based on historical monthly spending.

## Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Core programming |
| FastAPI | Backend REST API |
| MySQL | Database |
| SQLAlchemy | ORM |
| Pandas | Data processing and analysis |
| Scikit-learn | Machine learning |
| Streamlit | Frontend/dashboard |
| Plotly | Data visualization |
| bcrypt | Password hashing |

## Project Structure

```text
smart-expense-platform/
│
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── routers/
│   └── services/
│
├── frontend/
│   └── app.py
│
├── data/
│   └── sample_transactions.csv
│
├── requirements.txt
├── .gitignore
└── README.md