# 🏧 Banking System

This is a banking system application built with **`Python`**, **`Streamlit`**, and **`MySQL`**. The application allows users to create accounts, perform transactions (deposits, withdrawals, transfers), view transaction history, and close accounts. It uses environment variables to manage database credentials securely and ensures data integrity with proper error handling and security measures.


---

- [🏧 Banking System](#-banking-system)
  - [Features](#features)
  - [Tech Stack](#tech-stack)
  - [Directory Structure:](#directory-structure)
  - [Installation](#installation)
    - [Database Setup](#database-setup)
  - [Database\_Schema](#database_schema)
  - [Code-Logic](#code-logic)
    - [Explanation:](#explanation)
    - [Explanation:](#explanation-1)
    - [Explanation:](#explanation-2)
    - [Explanation:](#explanation-3)
    - [Explanation:](#explanation-4)
    - [Explanation:](#explanation-5)
    - [Explanation:](#explanation-6)
  - [Error Handling](#error-handling)
  - [Contributing](#contributing)
  - [Acknowledgments](#acknowledgments)
  - [Stay Connected:](#stay-connected)
---

## Features

- **User Registration and Login**
- **Account Management**
  - Create accounts
  - View account details
  - Close accounts
- **Transactions**
  - Deposit funds
  - Withdraw funds
  - Transfer funds between accounts
  - View transaction history
- **Secure Password Management**
- **Environment Variable Configuration**
---

## Tech Stack

- **Frontend**: `Streamlit` (for building the web interface)
- **Backend**: `Python` (for logic and API calls)
- **Database**: `MySQL` (for storing student records)
- **Environment**: `.env` file for storing sensitive information like database credentials

---
## Directory Structure:
    
```bash
project/
│
├── .env             # Contains database credentials      # Database-related logic
├── main.py          # Streamlit app for visualization

```

---
## Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/banking-system.git
cd banking-system
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. Install required dependencies:
```bash
pip install -r requirements.txt
```

4. Set up database credentials: Create a .env file in the root directory and populate it with your MySQL credentials:
     
```bash
DB_HOST=your_database_host
DB_USER=your_database_username
DB_PASSWORD=your_database_password
DB_NAME=your_database_name
```

5. Initialize the database and tables: Run the setup script to ensure the database and tables are created:

```bash
from banking_system import setup_database
setup_database()
```

6. Run the application:

```bash
streamlit run main.py
```

---

### Database Setup

* The application will automatically set up the database and create the necessary table on the first run.
* Make sure your MySQL database server is running, and the credentials in the .env file are correct.

---

## Database_Schema

The application uses the following database schema:

- **users**: Stores user credentials.
    - `user_id` (INT, PRIMARY KEY, AUTO_INCREMENT)
    - `username` (VARCHAR(255), NOT NULL, UNIQUE)
    - `password` (VARCHAR(255), NOT NULL)
    
- **accounts**: Stores account details.
    - `account_number` (INT, PRIMARY KEY, AUTO_INCREMENT)
    - `account_holder` (VARCHAR(255), NOT NULL)
    - `initial_balance` (DECIMAL(10, 2), NOT NULL)
    - `account_type` (VARCHAR(50), NOT NULL)

- **transactions**: Stores transaction details.
    - `transaction_id` (INT, PRIMARY KEY, AUTO_INCREMENT)
    - `account_number` (INT, FOREIGN KEY REFERENCES accounts(account_number))
    - `transaction_date` (DATETIME)
    - `transaction_type` (VARCHAR(50))
    - `amount` (DECIMAL(10, 2))
    - `balance` (DECIMAL(10, 2))

---
## Code-Logic
1. Database Connection Functions

```python

# Connect to MySQL Database
def connect_db(use_database=True):
    """
    Creates a MySQL connection.
    If use_database is True, it connects to the specified database.
    """
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME if use_database else None
        )
        return connection
    except Error as err:
        print(f"Error creating connection: {err}")
        raise

# Context manager for handling the connection
class DBConnection:
    def __enter__(self):
        self.conn = connect_db()
        self.cursor = self.conn.cursor(dictionary=True)
        return self.cursor

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

```

### Explanation:

- **connect_db**: Function to create a MySQL connection. It connects to the specified database if use_database is True.
- **DBConnection**: Context manager class to handle database connections. It ensures that the connection is properly committed and closed after use.

2. Setup Database and Tables 

```python
    def setup_database():
    try:
        conn = create_connection(use_database=False)
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        print(f"Database '{DB_NAME}' ensured to exist.")
        conn.database = DB_NAME

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            age INT,
            grade VARCHAR(10)
        )
        """)
        print("Table 'students' ensured to exist.")
        conn.commit()
        conn.close()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
```
### Explanation:

**setup_database**: Function to ensure the database and necessary tables exist. It creates the database if it doesn't exist and sets up the users, accounts, and transactions tables.

3. User Authentication Functions

```python
# Validate user credentials during login
def validate_user(username, password):
    try:
        with DBConnection() as cursor:
            cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
            user_data = cursor.fetchone()
            if user_data:
                return True
            else:
                return False
    except Error as err:
        print(f"Error validating user: {err}")
        raise

# Function to display the login form
def show_login_form():
    st.title("Login Page")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username and password:
            if validate_user(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success(f"Welcome, {username}!")
            else:
                st.error("Invalid username or password.")
        else:
            st.error("Please enter both username and password.")

# Function to handle logout
def show_logout():
    st.session_state.logged_in = False
    st.session_state.username = None
    st.success("You have logged out successfully.")
    st.rerun()
```
### Explanation:

- **validate_user**: Function to validate user credentials during login.
- **show_login_form**: Function to display the login form in the Streamlit interface.
- **show_logout**: Function to handle user logout and reset the session state.

4. Account Management Functions

```python
# Create a new account
def create_account(holder_name, initial_balance=0, account_type="Checking"):
    try:
        with DBConnection() as cursor:
            if not holder_name:
                raise ValueError("Account holder name cannot be empty.")

            if initial_balance < 0:
                raise ValueError("Initial balance cannot be negative.")

            cursor.execute("""
                INSERT INTO accounts (account_holder, initial_balance, account_type)
                VALUES (%s, %s, %s)
            """, (holder_name, initial_balance, account_type))
            account_number = cursor.lastrowid
            return account_number
    except mysql.connector.Error as err:
        print(f"Error creating account: {err}")
        raise  # Re-raise the exception to be handled by the calling function
    except ValueError as err:
        print(f"Invalid input: {err}")
        return None

# Get account by account number
def get_account(account_number):
    try:
        with DBConnection() as cursor:
            cursor.execute("SELECT * FROM accounts WHERE account_number = %s", (account_number,))
            account_data = cursor.fetchone()
        return account_data
    except Error as err:
        print(f"Error fetching account: {err}")
        raise

# Get all accounts
def get_all_accounts():
    try:
        with DBConnection() as cursor:
            cursor.execute("SELECT * FROM accounts")
            accounts_data = cursor.fetchall()
        return accounts_data
    except Error as err:
        print(f"Error fetching accounts: {err}")
        raise
```

### Explanation:

- create_account: Function to create a new bank account.
- get_account: Function to retrieve account details by account number.
- get_all_accounts: Function to retrieve all accounts from the database.

5. Transaction Management Functions

```python
# Save a transaction
def save_transaction(account_number, transaction_type, amount, balance):
    try:
        with DBConnection() as cursor:
            transaction_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute("""
                INSERT INTO transactions (account_number, transaction_date, transaction_type, amount, balance)
                VALUES (%s, %s, %s, %s, %s)
            """, (account_number, transaction_date, transaction_type, amount, balance))
    except Error as err:
        print(f"Error saving transaction: {err}")
        raise

# Get transaction history
def get_transaction_history(account_number):
    try:
        with DBConnection() as cursor:
            cursor.execute("SELECT * FROM transactions WHERE account_number = %s", (account_number,))
            transactions = cursor.fetchall()
        return transactions
    except Error as err:
        print(f"Error fetching transaction history: {err}")
        raise
```

### Explanation:

- **save_transaction**: Function to save a transaction record to the database.
- **get_transaction_history**: Function to retrieve the transaction history for a specific account.

6. Bank Account and Banking System Classes

```python
# Bank Account class
class BankAccount:
    def __init__(self, account_number, account_holder, initial_balance=0, account_type="Checking"):
        self.account_number = account_number
        self.account_holder = account_holder
        self.balance = Decimal(initial_balance)  # Ensure balance is a Decimal
        self.account_type = account_type

    def deposit(self, amount):
        amount = Decimal(amount)
        if amount <= 0:  # Validate amount
            st.error("Deposit amount must be greater than zero.")
            return False
        self.balance += amount
        update_account_balance(self.account_number, self.balance)
        save_transaction(self.account_number, "Deposit", amount, self.balance)

        # Update session state with the new balance
        st.session_state.selected_account.balance = self.balance

        return True

    def withdraw(self, amount):
        amount = Decimal(amount)
        if amount <= 0:  # Validate amount
            st.error("Withdrawal amount must be greater than zero.")
            return False
        if amount > self.balance:
            st.error("Insufficient funds.")
            return False
        self.balance -= amount
        update_account_balance(self.account_number, self.balance)
        save_transaction(self.account_number, "Withdrawal", amount, self.balance)

        # Update session state with the new balance
        st.session_state.selected_account.balance = self.balance

        return True

    def get_balance(self):
        return self.balance

    def get_transaction_history(self):
        return get_transaction_history(self.account_number)

# Banking System class
class BankingSystem:
    def __init__(self):
        if 'accounts' not in st.session_state:
            st.session_state.accounts = {}
            st.session_state.next_account_number = 1  # Account numbers will start from 1

    def create_account(self, holder_name, initial_balance=0, account_type="Checking"):
        account_number = create_account(holder_name, initial_balance, account_type)
        account = BankAccount(account_number, holder_name, initial_balance, account_type)
        return account_number

    def get_account(self, account_number):
        account_data = get_account(account_number)
        if account_data:
            return BankAccount(
                account_number=account_data["account_number"],
                account_holder=account_data["account_holder"],
                initial_balance=account_data["initial_balance"],
                account_type=account_data["account_type"]
            )
        return None

    def get_all_accounts(self):
        accounts = get_all_accounts()
        return [BankAccount(
            account_number=acc["account_number"],
            account_holder=acc["account_holder"],
            initial_balance=acc["initial_balance"],
            account_type=acc["account_type"]
        ) for acc in accounts]
```

### Explanation:

- **BankAccount**: Class to represent a bank account with methods for depositing, withdrawing, getting the balance, and retrieving transaction history.
- **BankingSystem**: Class to manage the banking system, including creating accounts, retrieving account details, and getting all accounts.

7. Streamlit Interface for the Banking System
```python
# Streamlit interface for the banking system
def main():
    # Initialize banking system only if logged in
    banking_system = BankingSystem()

    if 'logged_in' not in st.session_state or not st.session_state.logged_in:
        show_login_form()
        return
    st.set_page_config(page_title="Modern Banking System", layout="wide", page_icon="🏧")

    # Initialize banking system
    banking_system = BankingSystem()

    # Sidebar navigation
    st.sidebar.title("Banking Operations")
    operation = st.sidebar.radio(
        "Select Operation",
        ["Create Account", "Account Operations", "View All Accounts", "Transfer Between Accounts", "Close Account", "Logout"]
    )

    if operation == "Logout":
        show_logout()

    # Main content area styling
    st.markdown("""
        <style>
        .main {
            padding: 2rem;
        }
        .stButton>button {
            width: 100%;
        }
        </style>
    """, unsafe_allow_html=True)

    # Use Streamlit state to store account data for real-time updates
    if "selected_account" not in st.session_state:
        st.session_state.selected_account = None

    elif operation == "Create Account":
        st.title("Create New Account")
        with st.form("create_account_form"):
            holder_name = st.text_input("Account Holder Name")
            initial_balance = st.number_input("Initial Balance", min_value=0.0, value=0.0)
            account_type = st.selectbox("Account Type", ["Checking", "Savings", "Business"])
            submit_button = st.form_submit_button("Create Account")

            if submit_button and holder_name:
                account_number = banking_system.create_account(holder_name, initial_balance, account_type)
                st.success(f"Account created successfully! Your account number is: {str(account_number).zfill(7)}")

    elif operation == "Account Operations":
        st.title("Account Operations")

        # Fetch all accounts to populate the dropdown
        accounts = banking_system.get_all_accounts()
        account_numbers = [str(acc.account_number).zfill(7) for acc in accounts]

        account_number = st.selectbox("Select Account Number", account_numbers)
        account_number = int(account_number)

        # Use Streamlit state to store account data for real-time updates
        if "selected_account" not in st.session_state:
            st.session_state.selected_account = None

        if account_number != (st.session_state.selected_account.account_number if st.session_state.selected_account else None):
            st.session_state.selected_account = banking_system.get_account(account_number)

        account = st.session_state.selected_account

        if account:
            # Fetch transaction history for real-time updates
            transactions = account.get_transaction_history()

            # Calculate totals and net balance changes
            total_deposits = sum(Decimal(txn["amount"]) for txn in transactions if txn["transaction_type"] == "Deposit")
            total_withdrawals = sum(Decimal(txn["amount"]) for txn in transactions if txn["transaction_type"] == "Withdrawal")
            net_balance_change = total_deposits - total_withdrawals
            current_balance = Decimal(account.get_balance())

            # Display metrics
            st.subheader("Account Summary")
            col1, col2 = st.columns(2)
            col1.metric("Total Deposits", f"${total_deposits:.2f}")
            col1.metric("Total Withdrawals", f"${total_withdrawals:.2f}")
            col2.metric("Net Balance Change", f"${net_balance_change:.2f}")
            col2.metric("Current Balance", f"${current_balance:.2f}")

            # Display the current Available balance
            st.write(f"**Current Available Balance:** ${account.get_balance():.2f}")

            # Deposit and withdrawal forms
            col3, col4 = st.columns(2)

            with col3:
                with st.form("deposit_form"):
                    deposit_amount = st.number_input("Deposit Amount", min_value=0.0, key="deposit_amount")
                    if st.form_submit_button("Deposit"):
                        if account.deposit(deposit_amount):
                            st.success(f"Successfully deposited ${deposit_amount:.2f}")
                            st.session_state.selected_account = banking_system.get_account(account_number)  # Refresh account state
                            # Show the updated balance after deposit
                            st.write(f"Available Balance: ${account.get_balance():.2f}")
                        else:
                            st.error("Invalid deposit amount")

            with col4:
                with st.form("withdraw_form"):
                    withdraw_amount = st.number_input("Withdraw Amount", min_value=0.0, key="withdraw_amount")
                    if st.form_submit_button("Withdraw"):
                        if account.withdraw(withdraw_amount):
                            st.success(f"Successfully withdrawn ${withdraw_amount:.2f}")
                            st.session_state.selected_account = banking_system.get_account(account_number)  # Refresh account state
                            # Show the updated balance after withdrawal
                            st.write(f"Available Balance: ${account.get_balance():.2f}")
                        else:
                            st.error("Invalid withdrawal amount or insufficient funds")

            # Interest Calculation Section
            st.subheader("Interest Calculation")
            with st.form("interest_form"):
                annual_interest_rate = Decimal(st.number_input("Annual Interest Rate (%)", min_value=0.0, max_value=100.0, value=5.0, step=0.1))
                duration = Decimal(st.number_input("Duration (in years)", min_value=0.0, step=0.01))
                compound_frequency = st.selectbox("Compounding Frequency", ["Annually", "Semi-Annually", "Quarterly", "Monthly"], index=0)

                if st.form_submit_button("Calculate Interest"):
                    # Mapping compounding frequencies to periods
                    compounding_periods = {
                        "Annually": 1,
                        "Semi-Annually": 2,
                        "Quarterly": 4,
                        "Monthly": 12
                    }
                    n = compounding_periods[compound_frequency]

                    # Calculate interest using the compound interest formula
                    P = current_balance
                    r = annual_interest_rate / Decimal(100)
                    t = duration
                    A = P * (1 + r / Decimal(n)) ** (n * t)
                    interest_earned = A - P

                    st.write(f"**Interest Earned:** ${interest_earned:.2f}")
                    st.write(f"**Balance After Interest:** ${A:.2f}")

                    # Apply interest option
                    if st.form_submit_button("Apply Interest"):
                        account.deposit(float(interest_earned))  # Convert Decimal back to float for deposit method
                        st.success(f"Interest of ${interest_earned:.2f} applied to the account!")
                        st.session_state.selected_account = banking_system.get_account(account_number)  # Refresh account state

            # Transaction History
            st.subheader("Transaction History")
            if transactions:
                df = pd.DataFrame(transactions)
                df['transaction_date'] = pd.to_datetime(df['transaction_date']).dt.strftime('%Y-%m-%d %H:%M:%S')
                df.rename(columns={
                    "transaction_date": "Date",
                    "transaction_type": "Type",
                    "amount": "Amount",
                    "balance": "Balance"
                }, inplace=True)
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No transactions yet.")
        else:
            st.warning("Account not found. Please check the account number.")

    elif operation == "Transfer Between Accounts":
        st.title("Transfer Between Accounts")

        # Fetch accounts
        accounts = banking_system.get_all_accounts()
        account_numbers = [str(acc.account_number).zfill(7) for acc in accounts]

        # Select source and destination accounts
        source_account_number = st.selectbox("Select Source Account", account_numbers)
        source_account_number = int(source_account_number)

        dest_account_number = st.selectbox("Select Destination Account", account_numbers)
        dest_account_number = int(dest_account_number)

        # Input transfer amount
        transfer_amount = st.number_input("Enter Transfer Amount", min_value=0.0)

        # Perform the transfer
        if st.button("Transfer"):
            if source_account_number == dest_account_number:
                st.error("Source and destination accounts must be different.")
            elif transfer_between_accounts(banking_system, source_account_number, dest_account_number, transfer_amount):
                st.success(f"Transfer of ${transfer_amount:.2f} completed successfully.")
            else:
                st.error("Transfer failed. Please try again.")

    elif operation == "Close Account":
        st.title("Close Account")

        accounts = banking_system.get_all_accounts()
        account_numbers = [str(acc.account_number).zfill(7) for acc in accounts]

        account_to_close = st.selectbox("Select Account to Close", account_numbers)
        account_to_close = int(account_to_close)

        if st.button("Close Account"):
            if close_account(banking_system, account_to_close):
                st.success(f"Account {account_to_close} has been closed.")
            else:
                st.error("Account closure failed.")

    elif operation == "View All Accounts":
        st.title("All Accounts")

        # Get all accounts from the banking system
        accounts = banking_system.get_all_accounts()

        if accounts:
            # Display the accounts in a table
            data = {
                "Account Number": [str(account.account_number).zfill(7) for account in accounts],
                "Account Holder": [account.account_holder for account in accounts],
                "Balance": [f"${account.get_balance():.2f}" for account in accounts],
                "Account Type": [account.account_type for account in accounts],
            }

            # Convert to DataFrame for display
            df = pd.DataFrame(data)
            st.dataframe(df)
        else:
            st.info("No accounts available.")

if __name__ == "__main__":
    setup_database()
    main()
```

### Explanation:

- **main**: The main function to run the Streamlit interface. It handles user authentication, account creation, account operations, transfers, account closure, and viewing all accounts.
- **Streamlit Interface**: The interface allows users to perform various banking operations through a web-based interface.

---

## Error Handling

The application includes basic error handling to ensure smooth operation. If any errors occur (e.g., database issues or invalid input), they will be displayed to the user in a user-friendly format.

---

## Contributing

Feel free to contribute to this project by opening issues or submitting pull requests.

## Acknowledgments

- Special thanks to the contributors of the dataset and the libraries used in this project.

## Stay Connected:
 * [![Git](https://img.shields.io/badge/Git-F05032?logo=git&logoColor=fff)](https://www.github.com/palakgandhi98)
 * [![LinkedIn](https://img.shields.io/badge/Linkedin-%230077B5.svg?logo=linkedin&logoColor=white)](https://www.linkedin.com/in/palakgandhi98)

Let's build something amazing together!


License
This project is licensed under the MIT License.