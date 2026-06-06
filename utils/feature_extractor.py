import re
import pandas as pd
import whois
import datetime
from urllib.parse import urlparse
from utils.model_loader import TRAINING_COLUMNS

#Converts URL into  255 different features.

def get_whois_features(domain):
    suspicious_tlds = ['xyz', 'top', 'club', 'online', 'info', 'biz', 'ru', 'cn', 'tk']

    domain_age_days = -1
    suspicious_tld = 0
    if not domain:
        return domain_age_days, suspicious_tld
    try:
        w = whois.whois(domain)
        creation_date = w.creation_date

        if isinstance(creation_date, list):
            creation_date = creation_date[0]

        if creation_date:
            domain_age_days = (datetime.datetime.now() - creation_date).days
    except:
        pass

    tld = domain.split(".")[-1].lower()
    if tld in suspicious_tlds:
        suspicious_tld = 1

    return domain_age_days, suspicious_tld


def extract_features_from_url(url):
    #if not url.startswith(("http://", "https://")):
     #url = "https://" + url

    parsed = urlparse(url)
    domain = parsed.hostname
    
    if domain is None:
        domain = ""
    path = parsed.path
    domain_age_days, suspicious_tld = get_whois_features(domain)

    features = {
        'url_len': len(url),
        'hostname_len': len(domain),
        'path_length': len(path),
        'has_ip': int(bool(re.search(r'\d+\.\d+\.\d+\.\d+', domain))),
        'num_dots': url.count('.'),
        'num_hyphens': url.count('-'),
        'num_subdomains': max(0, domain.count('.') - 1),
        'uses_https': int(url.lower().startswith("https")),
        'query_length': len(parsed.query),
        'has_at': int('@' in url),
        'has_suspicious_words': int(any(word in url.lower()
            for word in ['secure','account','webscr','login','verify','banking'])),
        'has_http_token': int('http' in domain.lower()),
        'is_shortened': int(any(short in domain for short in
            ['bit.ly','tinyurl','goo.gl','t.co'])),
        'num_special_chars': len(re.findall(r'[^a-zA-Z0-9]', url)),
        'digit_count': sum(c.isdigit() for c in url),
        'domain_len': len(domain),
        'suspicious_tld': suspicious_tld,
        'domain_age_days': domain_age_days,
        'header_status_code': -1,
        'header_has_csp': False,
        'geo_country': 'NA',
        'geo_org': 'NA',
        'has_port': int(':' in domain),
        'https_in_domain': int('https' in domain.lower()),
    }

    return features


def preprocess_input(df):
    df = df.copy()

    for col in ["header_has_csp", "geo_country", "geo_org"]:
        if col in df.columns:
            df[col] = df[col].astype("category")

    df = pd.get_dummies(
        df,
        columns=["header_has_csp", "geo_country", "geo_org"],
        drop_first=True
    )

    for col in TRAINING_COLUMNS:
        if col not in df.columns:
            df[col] = 0

    df = df[TRAINING_COLUMNS]

    return df