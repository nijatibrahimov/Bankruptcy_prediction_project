# Bankruptcy Prediction

A machine learning project that predicts corporate bankruptcy using financial indicators. It combines a **Scikit-learn Logistic Regression pipeline**, a **Flask web application**, **MySQL** database integration, and a **Power BI dashboard**.

## Project Overview

The project covers the complete machine learning workflow, from financial data preprocessing and feature selection to model training, evaluation, and web application integration.

### Technologies

* **Language:** Python
* **Machine Learning:** Scikit-learn, Logistic Regression
* **Data Analysis:** Pandas, NumPy, Matplotlib, Seaborn
* **Web Framework:** Flask
* **Database:** MySQL
* **Visualization:** Power BI

## Project Structure

```text
.
├── static/
│   ├── style.css
│   └── script.js
├── templates/
│   └── main.html
├── bank.ipynb
├── data.csv
├── bankruptcy_model_data.csv
├── Bankruptcy1.pbix
├── model.pkl
├── server.py
├── requirements.txt
└── README.md
```

### Key Files

| File                        | Description                                                |
| --------------------------- | ---------------------------------------------------------- |
| `data.csv`                  | Original dataset                                           |
| `bankruptcy_model_data.csv` | Processed dataset used for modeling                        |
| `bank.ipynb`                | Data analysis, feature selection, training, and evaluation |
| `model.pkl`                 | Serialized trained machine learning pipeline               |
| `server.py`                 | Flask application and prediction endpoint                  |
| `Bankruptcy1.pbix`          | Power BI report                                            |
| `templates/main.html`       | Web interface                                              |
| `static/style.css`          | Interface styling                                          |
| `static/script.js`          | Client-side functionality                                  |
| `requirements.txt`          | Python dependencies                                        |

## Machine Learning Workflow

### 1. Feature Selection

* Used Variance Inflation Factor (VIF) to identify features with high multicollinearity.
* Analyzed feature correlations and removed selected features considered less informative.

### 2. Data Preprocessing

Prepared the selected financial indicators and exported the processed dataset to `bankruptcy_model_data.csv`.

### 3. Model Training

Built a Scikit-learn pipeline combining:

* `StandardScaler`
* `LogisticRegression`

Used `GridSearchCV` with 5-fold `StratifiedKFold` cross-validation to optimize the F1-score.

### 4. Best Hyperparameters

| Parameter                      | Selected Value |
| ------------------------------ | -------------- |
| `C`                            | `0.1`          |
| `solver`                       | `lbfgs`        |
| `class_weight`                 | `balanced`     |
| Best Cross-Validation F1-score | `0.2674`       |

### 5. Decision Threshold

Selected a decision threshold of **0.9205** based on the precision-recall curve, subject to a minimum precision target of 0.40.

## Model Evaluation

The test set contained **1,364 observations**, including 44 positive cases belonging to Class 1.

| Metric              | Result |
| ------------------- | -----: |
| Precision (Class 1) | 0.5000 |
| Recall (Class 1)    | 0.4318 |
| F1-score (Class 1)  | 0.4634 |
| Overall Accuracy    | 0.9677 |
| Selected Threshold  | 0.9205 |

### Confusion Matrix

```text
                 Predicted
                 0       1
Actual 0       1301     19
Actual 1         25     19
```

Because bankruptcy cases are relatively rare in the dataset, accuracy alone does not adequately measure the model's ability to identify at-risk companies. Precision, recall, and F1-score provide additional insight into its performance on the positive class.

> **Evaluation note:** The current notebook selects the decision threshold using the test set and evaluates performance on that same set. This can lead to optimistic performance estimates. A separate validation set or out-of-fold predictions should be used for threshold selection before final evaluation on an untouched test set.

## Web Application

The Flask application provides:

* A web interface for submitting financial indicators.
* A `POST /predict` endpoint that returns a bankruptcy prediction.
* MySQL integration for storing submitted inputs, predictions, and timestamps.
* USD-to-CNY conversion using the Frankfurter API, with a fallback exchange rate of `7.3`.

The application expects `model.pkl` to be present in the project root.

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/bankruptcy-prediction.git
cd bankruptcy-prediction
```

Replace `YOUR_USERNAME` with your GitHub username.

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
DB_HOST=localhost
DB_USER=your_mysql_username
DB_PASSWORD=your_mysql_password
DB_NAME=your_database_name
```

Create the corresponding database in MySQL before starting the application.

**Security:** Never commit your `.env` file or expose database credentials publicly.

### 5. Start the Application

Ensure that `model.pkl` exists in the project root, then run:

```bash
python server.py
```

Open the following address in your browser:

`http://127.0.0.1:5000`

## Dataset

The repository includes the original and processed CSV files used in the project.

The dataset's original source and license should be documented before the project is used for further research or commercial purposes.

## Limitations

* The dataset has an imbalanced target distribution.
* Model performance depends on feature selection, data quality, and the decision threshold.
* Threshold selection should be validated using data separate from the final test set.
* The application uses a fallback exchange rate if the currency API is unavailable.
* MySQL storage may fail independently of prediction generation.
* Predictions should not be treated as definitive financial or investment advice.

## Future Improvements

* Evaluate threshold selection using a separate validation set.
* Compare Logistic Regression with other classification algorithms.
* Improve probability calibration and risk explanations.
* Document the dataset source, license, and feature definitions.
* Add automated tests and deployment configuration.
