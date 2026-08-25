import streamlit as st
import requests
import pandas as pd
import plotly.express as px


# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Smart Expense Analytics",
    page_icon="💰",
    layout="wide"
)


# --------------------------------------------------
# FastAPI configuration
# --------------------------------------------------

API_URL = "http://127.0.0.1:8000"


# --------------------------------------------------
# Function to get data from FastAPI
# --------------------------------------------------

def login_user(email, password):
    """Login through FastAPI."""

    try:
        response = requests.post(
            f"{API_URL}/api/auth/login",
            params={
                "email": email,
                "password": password
            }
        )

        if response.status_code == 200:
            return response.json()

        return None

    except requests.exceptions.ConnectionError:
        return None


def register_user(name, email, password):
    """Create a new account through FastAPI."""

    try:
        response = requests.post(
            f"{API_URL}/api/auth/register",
            params={
                "name": name,
                "email": email,
                "password": password
            }
        )

        if response.status_code == 200:
            return response.json()

        return None

    except requests.exceptions.ConnectionError:
        return None
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_id" not in st.session_state:
    st.session_state.user_id = None

if "user_name" not in st.session_state:
    st.session_state.user_name = None

if "user_email" not in st.session_state:
    st.session_state.user_email = None

def get_data(endpoint):
    """Fetch data from FastAPI for the logged-in user."""

    try:
        response = requests.get(
            f"{API_URL}{endpoint}",
            params={
                "user_id": st.session_state.user_id
            }
        )

        if response.status_code == 200:
            return response.json()

        return None

    except requests.exceptions.ConnectionError:
        return None


# --------------------------------------------------
# Sidebar
# --------------------------------------------------

if not st.session_state.logged_in:

    st.title("💰 Smart Expense Platform")

    st.write(
        "Manage your expenses, budgets and spending insights."
    )

    login_tab, signup_tab = st.tabs(
        ["Login", "Create Account"]
    )

    # -----------------------------------------------
    # LOGIN
    # -----------------------------------------------

    with login_tab:

        st.subheader("Welcome back")

        email = st.text_input(
            "Email",
            key="login_email"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="login_password"
        )

        if st.button(
            "Login",
            use_container_width=True
        ):

            if not email or not password:

                st.warning(
                    "Please enter email and password."
                )

            else:

                result = login_user(
                    email,
                    password
                )

                if result:

                    st.session_state.logged_in = True

                    st.session_state.user_id = (
                        result["user_id"]
                    )

                    st.session_state.user_name = (
                        result["name"]
                    )

                    st.session_state.user_email = (
                        result["email"]
                    )

                    st.success(
                        "Login successful!"
                    )

                    st.rerun()

                else:

                    st.error(
                        "Invalid email or password."
                    )

    # -----------------------------------------------
    # SIGNUP
    # -----------------------------------------------

    with signup_tab:

        st.subheader("Create your account")

        name = st.text_input(
            "Name",
            key="signup_name"
        )

        email = st.text_input(
            "Email",
            key="signup_email"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="signup_password"
        )

        confirm_password = st.text_input(
            "Confirm Password",
            type="password",
            key="confirm_password"
        )

        if st.button(
            "Create Account",
            use_container_width=True
        ):

            if not name or not email or not password:

                st.warning(
                    "Please fill all fields."
                )

            elif password != confirm_password:

                st.error(
                    "Passwords do not match."
                )

            elif len(password) < 6:

                st.error(
                    "Password must contain at least 6 characters."
                )

            else:

                result = register_user(
                    name,
                    email,
                    password
                )

                if result:

                    st.success(
                        "Account created successfully! "
                        "You can now login."
                    )

                else:

                    st.error(
                        "Unable to create account. "
                        "The email may already be registered."
                    )

    st.stop()

st.sidebar.title("💰 Smart Expense")

st.sidebar.write(
    f"Welcome, {st.session_state.user_name}!"
)

st.sidebar.caption(
    st.session_state.user_email
)

if st.sidebar.button("Logout"):

    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.session_state.user_name = None
    st.session_state.user_email = None

    st.rerun()
page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Transactions",
        "Upload Data",
        "Budgets",
        "Anomalies",
        "Forecast"
    ]
)

# --------------------------------------------------
# Dashboard
# --------------------------------------------------

if page == "Dashboard":

    st.title("💰 Smart Expense & Financial Analytics")

    st.write(
        "Analyze your income, expenses, savings and spending patterns."
    )

    # Get summary data
    summary = get_data(
        "/api/analytics/summary"
    )

    if summary is None:
        st.error(
            "Unable to connect to the backend. "
            "Make sure FastAPI is running on port 8000."
        )
        st.stop()

    # --------------------------------------------------
    # Financial Overview
    # --------------------------------------------------

    st.subheader("Financial Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Income",
        f"₹{summary['total_income']:,.2f}"
    )

    col2.metric(
        "Total Expenses",
        f"₹{summary['total_expenses']:,.2f}"
    )

    col3.metric(
        "Savings",
        f"₹{summary['savings']:,.2f}"
    )

    col4.metric(
        "Savings Rate",
        f"{summary['savings_rate']:.2f}%"
    )

    # --------------------------------------------------
    # Additional Metrics
    # --------------------------------------------------

    st.write("")

    col1, col2 = st.columns(2)

    col1.metric(
        "Total Transactions",
        summary["total_transactions"]
    )

    col2.metric(
        "Average Transaction",
        f"₹{summary['average_transaction']:,.2f}"
    )

    st.divider()

    # --------------------------------------------------
    # Get category data
    # --------------------------------------------------

    category_data = get_data(
        "/api/analytics/categories"
    )

    category_df = pd.DataFrame(
        category_data if category_data else []
    )

    # --------------------------------------------------
    # Get merchant data
    # --------------------------------------------------

    merchant_data = get_data(
        "/api/analytics/top-merchants"
    )

    merchant_df = pd.DataFrame(
        merchant_data if merchant_data else []
    )

    # --------------------------------------------------
    # Category + Merchant Charts
    # --------------------------------------------------

    col1, col2 = st.columns(2)

    # Category chart
    with col1:

        st.subheader("Spending by Category")

        if not category_df.empty:

            fig = px.pie(
                category_df,
                names="category",
                values="amount",
                hole=0.4,
                title="Expense Distribution"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:

            st.info(
                "No expense data available."
            )

    # Merchant chart
    with col2:

        st.subheader("Top Spending Merchants")

        if not merchant_df.empty:

            fig = px.bar(
                merchant_df,
                x="amount",
                y="merchant",
                orientation="h",
                title="Top 5 Merchants by Spending",
                labels={
                    "amount": "Amount (₹)",
                    "merchant": "Merchant"
                }
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:

            st.info(
                "No merchant data available."
            )

    # --------------------------------------------------
    # Monthly Spending
    # --------------------------------------------------

    st.subheader("Monthly Spending")

    monthly_data = get_data(
        "/api/analytics/monthly"
    )

    monthly_df = pd.DataFrame(
        monthly_data if monthly_data else []
    )

    if not monthly_df.empty:

        fig = px.bar(
            monthly_df,
            x="month",
            y="amount",
            title="Monthly Expense Trend",
            labels={
                "month": "Month",
                "amount": "Expense (₹)"
            }
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:

        st.info(
            "No monthly expense data available."
        )


# --------------------------------------------------
# Transactions page
# --------------------------------------------------

elif page == "Transactions":

    st.title("📋 Transactions")

    transactions = get_data(
        "/api/transactions/"
    )

    if transactions:

        transaction_df = pd.DataFrame(
            transactions
        )

        st.dataframe(
            transaction_df,
            use_container_width=True
        )

    else:

        st.info(
            "No transactions available."
        )


# --------------------------------------------------
# Upload page
# --------------------------------------------------

elif page == "Upload Data":

    st.title("📤 Upload Transactions")

    st.write(
        "Upload a CSV or Excel file containing your transactions."
    )

    uploaded_file = st.file_uploader(
        "Choose a file",
        type=["csv", "xlsx", "xls"]
    )

    if uploaded_file is not None:

        st.success(
            f"File selected: {uploaded_file.name}"
        )

        if st.button("Upload Transactions"):

            try:

                files = {
                    "file": (
                        uploaded_file.name,
                        uploaded_file.getvalue()
                    )
                }

                response = requests.post(
                    f"{API_URL}/api/transactions/upload",
                    params={
                        "user_id": st.session_state.user_id
                    },
                    files=files
                )

                if response.status_code == 200:

                    result = response.json()

                    st.success(
                        result["message"]
                    )

                    st.info(
                        f"Transactions imported: "
                        f"{result['transactions_imported']}"
                    )

                else:

                    st.error(
                        f"Upload failed: {response.text}"
                    )

            except requests.exceptions.ConnectionError:

                st.error(
                    "Could not connect to FastAPI. "
                    "Make sure the backend is running."
                )
elif page == "Budgets":

    st.title("💰 Budget Management")

    budget_data = get_data(
        "/api/budgets/status"
    )

    if budget_data:

        budget_df = pd.DataFrame(
            budget_data
        )

        st.subheader("Monthly Budget Status")

        st.dataframe(
            budget_df,
            use_container_width=True,
            hide_index=True
        )

        st.subheader("Budget Usage")

        fig = px.bar(
            budget_df,
            x="category",
            y="usage_percentage",
            title="Budget Usage by Category",
            labels={
                "usage_percentage": "Budget Used (%)",
                "category": "Category"
            }
        )

        fig.add_hline(
            y=100,
            line_dash="dash",
            annotation_text="Budget Limit"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        exceeded = budget_df[
            budget_df["status"] == "Exceeded"
        ]

        if not exceeded.empty:

            st.warning(
                "⚠️ You have exceeded your budget "
                "in one or more categories."
            )

    else:

        st.info(
            "No budgets have been created yet."
        )
elif page == "Anomalies":

    st.title("🚨 Unusual Spending")

    anomaly_data = get_data(
        "/api/anomalies/"
    )

    if anomaly_data:

        anomaly_df = pd.DataFrame(
            anomaly_data
        )

        st.warning(
            f"{len(anomaly_df)} unusual "
            "transaction(s) detected."
        )

        st.dataframe(
            anomaly_df,
            use_container_width=True,
            hide_index=True
        )

        st.subheader(
            "Unusual Transaction Amounts"
        )

        fig = px.bar(
            anomaly_df,
            x="description",
            y="amount",
            title="Detected Unusual Transactions",
            labels={
                "description": "Transaction",
                "amount": "Amount (₹)"
            }
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:

        st.success(
            "No unusual transactions detected."
        )
elif page == "Forecast":

    st.title("📈 Expense Forecast")

    forecast = get_data(
        "/api/forecast/"
    )

    if forecast is None:

        st.error(
            "Unable to connect to the backend."
        )

    elif "message" in forecast:

        st.info(
            forecast["message"]
        )

    else:

        st.subheader(
            "Next Month Expense Prediction"
        )

        col1, col2 = st.columns(2)

        col1.metric(
            "Predicted Expenses",
            f"₹{forecast['predicted_expenses']:,.2f}"
        )

        col2.metric(
            "Forecast Month",
            forecast["next_month"]
        )

        st.write(
            f"The prediction is based on "
            f"{forecast['historical_months']} "
            f"months of historical spending."
        )

        # Historical spending
        monthly_data = get_data(
            "/api/analytics/monthly"
        )

        monthly_df = pd.DataFrame(
            monthly_data if monthly_data else []
        )

        if not monthly_df.empty:

            monthly_df["type"] = "Actual"

            forecast_row = pd.DataFrame({
                "month": [
                    forecast["next_month"]
                ],
                "amount": [
                    forecast["predicted_expenses"]
                ],
                "type": [
                    "Predicted"
                ]
            })

            combined_df = pd.concat(
                [
                    monthly_df,
                    forecast_row
                ],
                ignore_index=True
            )

            st.subheader(
                "Historical vs Predicted Spending"
            )

            fig = px.bar(
                combined_df,
                x="month",
                y="amount",
                color="type",
                barmode="group",
                labels={
                    "month": "Month",
                    "amount": "Expenses (₹)",
                    "type": "Data Type"
                }
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )