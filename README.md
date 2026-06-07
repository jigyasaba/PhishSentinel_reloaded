# 🛡️ PhishSentinel
### AI-Powered Phishing URL Detection System using Machine Learning & Generative AI

PhishSentinel is a cybersecurity-focused phishing detection system that identifies malicious and legitimate URLs in real time using Machine Learning, FastAPI, and Explainable AI techniques.

The project includes:
- 🔍 ML-based phishing URL detection
- ⚡ FastAPI backend for real-time prediction
- 🌐 Chrome Extension for live website scanning
- 🤖 Explainable AI risk analysis
- 📊 Confidence score and threat assessment

---

# 🚀 Features

✅ Real-time phishing URL detection  
✅ Machine Learning-based classification  
✅ Chrome Extension support  
✅ Explainable AI-based risk analysis  
✅ Confidence score generation  
✅ WHOIS and domain analysis  
✅ FastAPI REST API backend  
✅ Detection of zero-day phishing URLs  
✅ Modern and responsive UI  

---

# 🧠 Technologies Used

## Frontend
- HTML
- CSS
- JavaScript

## Backend
- Python
- FastAPI
- Uvicorn

## Machine Learning
- Scikit-learn
- Pandas
- NumPy
- Joblib

## URL & Domain Analysis
- python-whois
- urllib
- tldextract

---

# 📂 Project Structure

```text
PhishSentinel_reloaded/
│
├── backend/
│   ├── app.py
│   ├── utils/
│   │   ├── predictor.py
│   │   ├── feature_extractor.py
│   │   ├── model_loader.py
│   │
│   ├── model/
│   │   ├── phishing_model.pkl
│
├── extension/
│   ├── manifest.json
│   ├── popup.html
│   ├── popup.js
│   ├── style.css
│   ├── image.png
│
├── dataset/
│   ├── phishing_urls.csv
│
├── training/
│   ├── train_model.ipynb
│
├── README.md
```

---

# ⚙️ System Architecture

```text
User URL Input
       ↓
Frontend / Chrome Extension
       ↓
FastAPI Backend API
       ↓
Feature Extraction
       ↓
Machine Learning Model
       ↓
Prediction + Confidence
       ↓
Explainable AI Analysis
       ↓
Result Displayed to User
```

---

# 🔍 Feature Extraction

The system extracts multiple phishing-related features from URLs.

## URL-Based Features
- URL Length
- HTTPS usage
- Presence of IP address
- Number of dots
- Number of subdomains
- Suspicious symbols (@, -, //)

## Domain-Based Features
- Domain age
- Expiry duration
- Registration period
- WHOIS availability

## Security Features
- SSL certificate presence
- Redirection behavior

---

# 🤖 Machine Learning Model

Multiple ML algorithms were tested:
- Logistic Regression
- Decision Tree
- Random Forest

✅ Final Model Used:
# Random Forest Classifier

### Why Random Forest?
- High accuracy
- Better handling of mixed features
- Reduced overfitting
- Strong feature importance analysis

---

# 📊 Model Performance

| Metric | Score |
|---|---|
| Accuracy | ~97-99% |
| Precision | High |
| Recall | High |
| F1 Score | High |

---

# 🛡️ Zero-Day Phishing Detection

Traditional blacklist systems fail against newly generated phishing URLs.

PhishSentinel uses:
- Feature-based ML analysis
- Domain intelligence
- URL behavior analysis

to detect:
- Unknown phishing URLs
- Newly created malicious domains
- Zero-day phishing attacks

---

# 🔌 FastAPI Backend

The FastAPI backend:
- Receives URLs from frontend/extension
- Extracts phishing features
- Runs ML prediction
- Returns JSON response

---

# 📡 API Endpoint

## Predict URL

### Endpoint
```http
POST /predict-url
```

### Request
```json
{
  "url": "http://example.com"
}
```

### Response
```json
{
  "prediction": 1,
  "label": "Malicious",
  "confidence": 0.99,
  "explanation": "This URL appears suspicious due to lack of HTTPS and abnormal domain patterns."
}
```

---

# 💻 Backend Setup

## 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/PhishSentinel.git
```

---

## 2️⃣ Navigate to Project

```bash
cd PhishSentinel_reloaded
```

---

## 3️⃣ Create Virtual Environment

```bash
python -m venv phis_sentinel
```

---

## 4️⃣ Activate Virtual Environment

### Windows
```bash
phis_sentinel\Scripts\activate
```

### Linux/Mac
```bash
source phis_sentinel/bin/activate
```

---

## 5️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 6️⃣ Run FastAPI Server

```bash
cd backend
uvicorn app:app --reload
```

Server runs on:

```text
http://127.0.0.1:8000
```

---

# 🌐 Chrome Extension Setup

## 1️⃣ Open Chrome Extensions

Go to:

```text
chrome://extensions
```

---

## 2️⃣ Enable Developer Mode

Turn ON:
- Developer Mode

---

## 3️⃣ Load Extension

Click:
- Load Unpacked

Select:
```text
extension/
```

folder.

---

# 🖥️ Chrome Extension Features

✅ Scan current website  
✅ AI-generated risk analysis  
✅ Confidence score display  
✅ Real-time phishing detection  
✅ Modern cybersecurity-themed UI  

---

# 📷 Sample Workflow

```text
Open Website
      ↓
Click PhishSentinel Extension
      ↓
Scan Current URL
      ↓
Backend API Analysis
      ↓
Prediction + Confidence
      ↓
AI Risk Explanation
```

---

# 🧪 Future Enhancements

- Browser history analysis
- QR phishing detection
- Email phishing detection
- Deep learning integration
- Cloud deployment
- Browser warning system
- Live threat intelligence APIs
- Website screenshot analysis

---

# 📚 Academic Relevance

This project demonstrates:
- Cybersecurity concepts
- Machine Learning integration
- Explainable AI
- REST API development
- Browser extension development
- Full-stack integration

Suitable for:
- MCA Final Year Project
- Cybersecurity Projects
- AI/ML Research Demonstrations

---

# 👨‍💻 Author

## Your Name
MCA Final Year Project

### PhishSentinel — AI Powered Phishing URL Detection System

---
## 🔗 LinkedIn Project Post+Demo Video
[View LinkedIn Post and Demo Video](https://www.linkedin.com/posts/jigyasa-bamola_machinelearning-cybersecurity-python-ugcPost-7469240453029187585-VDS6/?utm_source=social_share_send&utm_medium=member_desktop_web&rcm=ACoAAD9Gs9IBDReBc3cxpi0H-5jLQ7nZI6Rq9-M)
---

# 📄 License

This project is developed for educational and academic purposes.
