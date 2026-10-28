# server.py
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import joblib
import pandas as pd
import mysql.connector
from mysql.connector import errorcode
from dotenv import load_dotenv
import os

app = Flask(__name__)
CORS(app)

# Load .env
load_dotenv()

# Load your saved pipeline/model
model = joblib.load("model.pkl")

# MySQL connection config from .env
db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME')
}

# Function to ensure table exists
def ensure_table_exists():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS financial_inputs (
                id INT AUTO_INCREMENT PRIMARY KEY,
                company_name VARCHAR(255),
                roa FLOAT,
                net_worth_assets FLOAT,
                retained_earnings FLOAT,
                per_share_net_profit FLOAT,
                net_income_to_equity FLOAT,
                current_liability_assets FLOAT,
                net_value_per_share FLOAT,
                operating_profit FLOAT,
                liability_assets_flag FLOAT,
                total_expense_assets FLOAT,
                equity_to_long_term FLOAT,
                cfo_to_assets FLOAT,
                tax_rate FLOAT,
                cash_to_assets FLOAT,
                prediction INT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        cursor.close()
        conn.close()
    except mysql.connector.Error as e:
        print("Table creation/check failed:", e)

# Ensure table exists at startup
ensure_table_exists()

# Home page
@app.route("/")
def home():
    return render_template("main.html")

# Predict endpoint
@app.route("/predict", methods=["POST"])
def predict():
    try:
        input_data = request.get_json()

        # X_train column adları
        columns = [
            ' ROA(C) before interest and depreciation before interest',
            ' Net worth/Assets',
            ' Retained Earnings to Total Assets',
            ' Per Share Net profit before tax (Yuan ¥)',
            ' Net Income to Stockholder\'s Equity',
            ' Current Liability to Current Assets',
            ' Net Value Per Share (B)',
            ' Operating Profit Per Share (Yuan ¥)',
            ' Liability-Assets Flag',
            ' Total expense/Assets',
            ' Equity to Long-term Liability',
            ' CFO to Assets',
            ' Tax rate (A)',
            ' Cash/Total Assets'
        ]

        # Company name
        company_name = input_data.get('company_name')
        if not company_name or company_name.strip() == "":
            company_name = "Unknown"
        
        # Input list: eyni sıralama ilə
        input_list = [input_data[col] for col in columns]

        # DataFrame şəklinə salırıq
        df_input = pd.DataFrame([input_list], columns=columns)

        # USD → Yuan çevrilməsi
        import requests

        # USD → Yuan çevrilməsi (real-time API ilə)
        try:
            response = requests.get("https://api.frankfurter.dev/v2/latest?base=USD&symbols=CNY")
            data = response.json()
            usd_to_yuan = data["rates"]["CNY"]
        except Exception as e:
            print("Currency API failed, using fallback rate:", e)
            usd_to_yuan = 7.3  # fallback

        yuan_columns = [
            ' Per Share Net profit before tax (Yuan ¥)',
            ' Operating Profit Per Share (Yuan ¥)'
        ]

        df_input[yuan_columns] = df_input[yuan_columns] * usd_to_yuan

        # Make prediction
        prediction = model.predict(df_input)[0]
        message = "Your company will not go bankrupt." if prediction == 0 else "Your company will go bankrupt."
        # ---- MySQL insert ----
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()

            insert_query = """
            INSERT INTO financial_inputs (
                company_name,
                roa, net_worth_assets, retained_earnings, per_share_net_profit,
                net_income_to_equity, current_liability_assets, net_value_per_share,
                operating_profit, liability_assets_flag, total_expense_assets,
                equity_to_long_term, cfo_to_assets, tax_rate, cash_to_assets, prediction
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            values = [
                company_name,
                input_list[0],
                input_list[1],
                input_list[2],
                input_list[3],
                input_list[4],
                input_list[5],
                input_list[6],
                input_list[7],
                input_list[8],
                input_list[9],
                input_list[10],
                input_list[11],
                input_list[12],
                input_list[13],
                int(prediction)
            ]

            cursor.execute(insert_query, values)
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as db_err:
            print("DB insert failed:", db_err)

        return jsonify({"prediction": int(prediction), "message": message})

    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True)