Bankruptcy Prediction
A machine-learning project that predicts whether a company is likely to
go bankrupt based on selected financial indicators. The project combines
a Logistic Regression pipeline, a Flask web application, MySQL storage
for submitted inputs and predictions, and a Power BI report.
Project Structure
``` text
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
├── README.md
├── .env                 # local secrets; do not commit
└── .gitignore
```
`data.csv` --- original dataset.
`bankruptcy_model_data.csv` --- processed dataset used for modeling.
`bank.ipynb` --- exploratory analysis, feature selection, model
training, and evaluation.
`model.pkl` --- serialized fitted scikit-learn pipeline loaded by
the web application.
`server.py` --- Flask application and prediction endpoint.
`templates/main.html`, `static/style.css`, `static/script.js` ---
web interface files.
`Bankruptcy1.pbix` --- Power BI report file.
Workflow
Feature analysis: Variance Inflation Factor (VIF) was used to
identify features with high multicollinearity. Features with high
VIF values were removed.
Correlation analysis: Feature correlations were reviewed and
additional features considered weakly informative for the model were
removed.
Preprocessing: The selected features were exported to
`bankruptcy_model_data.csv` and then loaded for model development.
Model pipeline: `StandardScaler` and `LogisticRegression` were
combined in a scikit-learn `Pipeline`.
Hyperparameter tuning: `GridSearchCV` evaluated 16 combinations
using 5-fold `StratifiedKFold` cross-validation, optimizing the
F1-score.
Decision threshold selection: A threshold was selected from the
precision-recall curve subject to a minimum precision target of
0.40.
Deployment: The saved pipeline is loaded by Flask and used to
return a bankruptcy prediction. Submitted inputs and predictions are
stored in MySQL when the database is available.
Best hyperparameters
`C`: `0.1`
`solver`: `lbfgs`
`class_weight`: `balanced`
Best cross-validation F1-score: 0.2674
Evaluation Results
The reported evaluation used 1,364 test observations, including 44
positive (`Class 1`) cases.
Metric                 Class 1 result
---
Precision                      0.5000
Recall                         0.4318
F1-score                       0.4634
Selected threshold             0.9205
Overall accuracy               0.9677
Confusion matrix:
``` text
[[1301   19]
 [  25   19]]
```
Because the positive class is relatively rare, accuracy alone does not
fully describe the model's ability to identify companies at risk of
bankruptcy. Precision, recall, and F1-score for Class 1 are important
when interpreting the results.
Evaluation note: In the current notebook code, the decision
threshold is selected using `X_test` and `y_test`, and performance is
then reported on that same test set. This can make the reported test
metrics optimistic. For a more robust final evaluation, select the
threshold using a separate validation set or out-of-fold predictions,
and keep the test set untouched until final evaluation.
Web Application
The Flask application provides:
A home page rendered from `templates/main.html`.
A `POST /predict` endpoint that accepts JSON financial inputs and
returns a prediction and message.
A MySQL table named `financial_inputs` for storing company inputs,
the prediction, and the timestamp.
USD-to-CNY conversion for the two per-share fields, using the
Frankfurter API with a fallback rate of `7.3` if the request fails.
The app expects the serialized model file to be named `model.pkl` and
located in the project root.
Setup
1. Create and activate a virtual environment
``` bash
python -m venv .venv
```
Windows:
``` bash
.venv\Scripts\activate
```
macOS/Linux:
``` bash
source .venv/bin/activate
```
2. Install dependencies
``` bash
pip install -r requirements.txt
```
3. Configure environment variables
Create a local `.env` file in the project root:
``` env
DB_HOST=localhost
DB_USER=your_mysql_username
DB_PASSWORD=your_mysql_password
DB_NAME=your_database_name
```
Create the database named by `DB_NAME` in MySQL before starting the app.
The application attempts to create the `financial_inputs` table at
startup. Keep `.env` out of version control.
4. Add the trained model
Ensure `model.pkl` exists in the project root. It must contain the
fitted pipeline expected by `server.py`.
5. Run the application
``` bash
python server.py
```
Open `http://127.0.0.1:5000` in your browser.
Dataset
The original and processed CSV files are included in the repository. The
dataset source and license should be added here before public release.
Limitations
This is a machine-learning project and should not be treated as a
definitive financial or investment decision tool.
The model's performance depends on the dataset, feature selection,
and class imbalance.
The web app currently uses a fallback exchange rate if the currency
API is unavailable.
Database storage is best-effort: prediction responses may still be
returned if inserting a record into MySQL fails.
Future Improvements
Evaluate threshold selection with a separate validation set.
Compare Logistic Regression with additional classification models.
Add calibration and more detailed risk explanations.
Document the dataset source, licensing, and data dictionary.
Add automated tests and deployment configuration.