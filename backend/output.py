import streamlit as st
import pandas as pd
import numpy as np
import re
import seaborn as sns
import matplotlib.pyplot as plt
from urllib.parse import urlparse
from joblib import load
from sklearn.metrics import classification_report, confusion_matrix
import whois
import datetime

# Set Streamlit page
st.set_page_config(page_title="ML Prediction Dashboard", layout="wide")
st.title("Machine Learning Prediction Dashboard")

# Sidebar: Upload
st.sidebar.header("Upload Data")
uploaded_file = st.sidebar.file_uploader("Upload CSV for batch prediction", type=["csv"])

# Sidebar: Model selection
model_choice = st.sidebar.selectbox(
    "Select a Model",
    ("Stacking Classifier", "Logistic Regression", "SVM", "XGBoost")
)

# Load models and training column list
@st.cache_resource
def load_models():
    models = {
        "Stacking Classifier": load("stacking_model.joblib"),
        #"Random Forest": load("random_forest_model.joblib"),
        "Logistic Regression": load("logistic_regression_model.joblib"),
        "SVM": load("svm_model.joblib"),
        "XGBoost": load("xgboost_model.joblib"),
    }
    return models, load("training_columns.pkl")

models, training_columns = load_models()
selected_model = models[model_choice]

# Helper: WHOIS domain age and suspicious TLD
def get_whois_features(domain):
    suspicious_tlds = ['xyz', 'top', 'club', 'online', 'info', 'biz', 'ru', 'cn', 'tk']  # example suspicious TLDs
    domain_age_days = -1
    suspicious_tld_flag = 0

    try:
        w = whois.whois(domain)
        creation_date = w.creation_date
        if isinstance(creation_date, list):
            creation_date = creation_date[0]
        if creation_date and isinstance(creation_date, datetime.datetime):
            domain_age_days = (datetime.datetime.now() - creation_date).days
    except Exception:
        # If WHOIS fails, keep domain_age_days as -1
        domain_age_days = -1

    # Check if TLD is suspicious
    tld = domain.split('.')[-1].lower()
    if tld in suspicious_tlds:
        suspicious_tld_flag = 1

    return domain_age_days, suspicious_tld_flag

# Helper: extract features from URL
def extract_features_from_url(url):
    parsed = urlparse(url)
    domain = parsed.netloc
    path = parsed.path

    # WHOIS features
    domain_age_days, suspicious_tld = get_whois_features(domain)

    features = {
        'url_len': len(url),
        'hostname_len': len(domain),
        'path_length': len(path),
        'has_ip': int(bool(re.search(r'\d+\.\d+\.\d+\.\d+', domain))),
        'num_dots': url.count('.'),
        'num_hyphens': url.count('-'),
        'num_subdomains': domain.count('.') - 1 if domain.count('.') > 1 else 0,
        'uses_https': int(url.lower().startswith("https")),
        'query_length': len(parsed.query),
        'has_at': int('@' in url),
        'has_double_slash': int('//' in path),
        'has_suspicious_words': int(any(word in url.lower() for word in ['secure', 'account', 'webscr', 'login', 'verify', 'banking'])),
        'has_http_token': int(bool(re.search(r'http', domain, re.IGNORECASE))),
        'is_shortened': int(any(short in domain for short in ['bit.ly', 'tinyurl', 'goo.gl', 't.co'])),
        'num_special_chars': len(re.findall(r'[!#$%&\'*+,-./:;<=>?@[\\\]^_`{|}~]', url)),
        'num_subdirs': path.count('/'),
        'digit_count': sum(c.isdigit() for c in url),
        'domain_len': len(domain),
        'suspicious_tld': suspicious_tld,
        'domain_age_days': domain_age_days,
        'hostname_len': len(domain),
        # Set placeholders for header and geo features to be filled later or zero if missing
        'header_status_code': -1,
        'header_has_csp': False,
        'geo_country': 'NA',
        'geo_org': 'NA',
        'has_port': int(':' in domain and domain.split(':')[-1].isdigit()),
        'https_in_domain': int('https' in domain),
    }
    return features

# Helper: preprocess input like training time
def preprocess_input(data):
    data = data.copy()
    # Drop unused columns if present
    drop_cols = ["geo_asn", "header_powered_by", "header_server", "url", "domain"]
    data.drop(columns=[col for col in drop_cols if col in data.columns], inplace=True, errors="ignore")

    # Fill missing values
    fill_map = {
        "header_status_code": -1,
        "header_has_csp": False,
        "geo_country": "NA",
        "geo_org": "NA",
        "domain_age_days": -1,
        "suspicious_tld": 0,
    }
    for key, val in fill_map.items():
        if key in data.columns:
            data[key].fillna(val, inplace=True)

    # Cast categories
    for col in ["header_has_csp", "geo_country", "geo_org"]:
        if col in data.columns:
            data[col] = data[col].astype("category")

    # One-hot encode categorical features
    data = pd.get_dummies(data, columns=["header_has_csp", "geo_country", "geo_org"], drop_first=True)

    # Align columns with training data columns
    for col in training_columns:
        if col not in data.columns:
            data[col] = 0
    data = data[training_columns]

    return data

# Tabs
tabs = st.tabs(["Batch Upload", "Live Test"])

# ==== Batch Upload ====
with tabs[0]:
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.subheader("Preview of Uploaded Data")
        st.dataframe(df.head())

        if 'target' in df.columns:
            X = df.drop(columns=['target'])
            y_true = df['target']
        else:
            X = df
            y_true = None

        # If no WHOIS features present in batch, extract them
        if 'domain_age_days' not in X.columns or 'suspicious_tld' not in X.columns:
            st.info("Extracting WHOIS features for batch URLs (may take a while)...")
            # Attempt to extract from a URL column if present
            if 'url' in X.columns:
                whois_feats = X['url'].apply(lambda u: pd.Series(get_whois_features(urlparse(u).netloc)))
                whois_feats.columns = ['domain_age_days', 'suspicious_tld']
                X = pd.concat([X, whois_feats], axis=1)
            else:
                st.warning("No 'url' column found to extract WHOIS features.")

        try:
            X_processed = preprocess_input(X)
            y_pred = selected_model.predict(X_processed)

            st.subheader("Prediction Results")
            st.write(pd.DataFrame({"Prediction": y_pred}))

            if y_true is not None:
                st.subheader("Classification Report")
                report = classification_report(y_true, y_pred, output_dict=True)
                st.dataframe(pd.DataFrame(report).transpose())

                st.subheader("Confusion Matrix")
                cm = confusion_matrix(y_true, y_pred)
                fig, ax = plt.subplots()
                sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=ax)
                ax.set_xlabel("Predicted")
                ax.set_ylabel("Actual")
                st.pyplot(fig)

            # Feature importance
            st.subheader("Feature Importances")
            try:
                if hasattr(selected_model, 'feature_importances_'):
                    importances = selected_model.feature_importances_
                elif hasattr(selected_model, 'named_estimators_') and 'rf' in selected_model.named_estimators_:
                    importances = selected_model.named_estimators_['rf'].feature_importances_
                else:
                    raise AttributeError("Model does not expose feature_importances_")

                feat_imp = pd.Series(importances, index=training_columns).sort_values(ascending=False)
                st.bar_chart(feat_imp)
                st.write("Most Dominant Feature:", feat_imp.idxmax())

            except Exception as e:
                st.warning(f"Could not extract feature importances: {e}")

        except Exception as e:
            st.error(f"Prediction failed: {e}")
    else:
        st.info("Upload a CSV file to get started.")

# ==== Live Test ====
with tabs[1]:
    st.subheader("Live URL Prediction Test")
    url_input = st.text_input("Enter a URL to predict")

    if url_input:
        try:
            features_dict = extract_features_from_url(url_input)
            input_df = pd.DataFrame([features_dict])
            # Align features to training columns
            for col in training_columns:
                if col not in input_df.columns:
                    input_df[col] = 0
            input_df = input_df[training_columns]
            prediction = selected_model.predict(input_df)[0]
            prob = selected_model.predict_proba(input_df)[0][int(prediction)]

            st.success(f"Prediction: {'Malicious' if prediction == 1 else 'Benign'} ({prob*100:.2f}% confidence)")

            # Feature contributions
            st.subheader("Feature Contributions")
            try:
                if hasattr(selected_model, 'feature_importances_'):
                    importances = selected_model.feature_importances_
                    feat_imp = pd.Series(importances, index=training_columns).sort_values(ascending=False)
                elif hasattr(selected_model, 'named_estimators_') and 'rf' in selected_model.named_estimators_:
                    importances = selected_model.named_estimators_['rf'].feature_importances_
                    feat_imp = pd.Series(importances, index=training_columns).sort_values(ascending=False)
                else:
                    feat_imp = pd.Series(dtype=float)

                for f in feat_imp.index[:5]:
                    if f in input_df.columns:
                        st.write(f"{f}: {input_df.iloc[0][f]}")

            except Exception as e:
                st.warning(f"Feature explanation failed: {e}")

        except Exception as e:
            st.error(f"Error processing input: {e}")
   