from urllib.parse import urlparse

import pandas as pd
from utils.model_loader import MODEL
from utils.feature_extractor import extract_features_from_url, preprocess_input
'''complete prediction pipeline
 1.Converts URL into features
 2.preprocess
 3.model.predict()
 4.confidence
 5.result JSON
'''
TRUSTED_DOMAINS = [
    "google.com",
    "youtube.com",
    "github.com",
    "microsoft.com",
    "amazon.com",
    "apple.com",
    "openai.com",
    "linkedin.com"
    "chatgpt.com"
]
def is_trusted_domain(url):
    domain = urlparse(url).netloc.lower()

    # remove www.
    if domain.startswith("www."):
        domain = domain[4:]

    return any(
        domain == d or domain.endswith("." + d)
        for d in TRUSTED_DOMAINS
    )

def predict_url(url):
    features = extract_features_from_url(url)
    signals = {
        "uses_ip": features["has_ip"],
        "https": features["uses_https"],
        "subdomain_count": features["num_subdomains"],
        "url_length": features["url_len"],
        "hyphen_count": features["num_hyphens"],
        "has_at_symbol": features["has_at"],
        "suspicious_words": features["has_suspicious_words"],
        "shortened_url": features["is_shortened"],
        "http_in_domain": features["has_http_token"],
        "special_chars": features["num_special_chars"],
        "digit_count": features["digit_count"],
        "suspicious_tld": features["suspicious_tld"],
        "has_port": features["has_port"],
        "https_in_domain": features["https_in_domain"]
    }

    df = pd.DataFrame([features])
    X = preprocess_input(df)

    pred = int(MODEL.predict(X)[0])
    prob = MODEL.predict_proba(X)[0]
    try:
        prob = float(MODEL.predict_proba(X)[0][pred])
    except:
        prob = 0.0
    
    label = "Malicious" if pred == 1 else "Benign"
    risk = "High" if pred == 1 else "Low"
    note = ""
    if is_trusted_domain(url) and pred == 1:
        risk = "Low"
        note = "Trusted domain detected. Possible false positive."
    return {
        "url": url,
        "prediction": pred,
        "label": label,
        "confidence": round(prob, 4),
        "signals":  signals,
        "risk": risk,
        "note": note
    }