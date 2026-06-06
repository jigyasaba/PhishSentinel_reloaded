from dotenv import load_dotenv
import os
from groq import Groq

# Load .env file
load_dotenv()

# Read API key
groq_api_key = os.getenv("GROQ_API_KEY")

# Create Groq client
client = Groq(api_key=groq_api_key)


def explain_url_result(url, prediction, confidence, signals):
    """
    Generate human-friendly phishing explanation
    """
    readable_signals = []
    if signals.get("uses_ip", 0) == 1:
        readable_signals.append("uses an IP address instead of a normal domain")

    if signals.get("https", 1) == 0:
        readable_signals.append("does not use HTTPS")

    if signals.get("subdomain_count", 0) > 2:
        readable_signals.append("contains many subdomains")

    if signals.get("url_length", 0) > 75:
        readable_signals.append("URL is unusually long")

    if signals.get("hyphen_count", 0) > 1:
        readable_signals.append("contains multiple hyphens")

    if signals.get("has_at_symbol", 0) == 1:
        readable_signals.append("contains @ symbol")

    if signals.get("suspicious_words", 0) == 1:
        readable_signals.append("contains words like login, verify, secure")

    if signals.get("shortened_url", 0) == 1:
        readable_signals.append("uses a shortened URL service")

    if signals.get("http_in_domain", 0) == 1:
        readable_signals.append("contains 'http' inside domain name")

    if signals.get("has_port", 0) == 1:
        readable_signals.append("contains custom port number")

    if not readable_signals:
        readable_signals.append("no major suspicious structural signals detected")
    

    # Convert signal list to readable text
    if signals:
        signal_text = ", ".join(readable_signals)
    else:
        signal_text = "No detailed signals provided"

    prompt = f"""
You are a cybersecurity assistant.
Explain only using provided evidence. Avoid generic wording.
Analyze the result below and explain in simple language why the URL was classified this way.

URL: {url}
Prediction: {prediction}
Confidence Score: {confidence}
Signals: {signal_text}

Rules:
- Keep answer under 3 lines
- Use simple language
- mention only provided signals, do not infer beyond them
- Do no use vague phrases like suspicious patterns
- If phishing, advise caution
- If safe, mention no major red flags found
- Be direct and specific
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You explain phishing detection results clearly."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"Explanation service unavailable: {str(e)}"