const urlBox = document.getElementById("urlBox");
const result = document.getElementById("result");
const scanBtn = document.getElementById("scanBtn");

let currentUrl = "";

// Get current active tab URL
chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {

    if (!tabs || !tabs[0] || !tabs[0].url) {
        urlBox.innerHTML = "❌ Unable to fetch current tab URL";
        return;
    }

    currentUrl = tabs[0].url;

    try {
        const parsed = new URL(currentUrl);

        const domain = parsed.hostname.replace("www.", "");

        urlBox.innerHTML = `
            <div class="site-info">
                <strong>🌐 Current Site</strong>
                <p>${domain}</p>
            </div>
        `;
    } catch (err) {
        urlBox.innerHTML = "⚠️ Invalid URL";
    }
});

// Scan button click
scanBtn.addEventListener("click", async () => {

    if (!currentUrl) {
        result.innerHTML = `
            <div class="danger">
                No URL found to scan
            </div>
        `;
        return;
    }

    scanBtn.disabled = true;
    scanBtn.innerText = "Scanning...";

    result.innerHTML = `
        <div class="loading">
            🔍 Analyzing URL Security...
        </div>
    `;

    try {

        const response = await fetch("http://127.0.0.1:8000/predict-url", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ url: currentUrl })
        });

        if (!response.ok) {
            throw new Error("Server Error");
        }

        const data = await response.json();

        let cls = "safe";
        let risk = "LOW RISK";
        let icon = "✅";

        if (data.prediction === 1 && data.confidence >= 0.90) {
            cls = "danger";
            risk = "HIGH RISK";
            icon = "🚨";
        }
        else if (data.prediction === 1) {
            cls = "medium";
            risk = "MEDIUM RISK";
            icon = "⚠️";
        }

        result.innerHTML = `
            <div class="${cls}">
                
                <div class="status-header">
                    <h3>${icon} ${data.label}</h3>
                </div>

                <div class="score-box">
                    <p><strong>Confidence:</strong> ${(data.confidence * 100).toFixed(2)}%</p>
                    <p><strong>Risk Level:</strong> ${risk}</p>
                </div>

                <div class="url-preview">
                    <strong>Scanned URL:</strong>
                    <p>${currentUrl}</p>
                </div>

                <div class="explanation">
                    <strong>AI Analysis:</strong>
                    <p>${data.explanation || "No explanation available."}</p>
                </div>

            </div>
        `;

    } catch (err) {

        result.innerHTML = `
            <div class="danger">
                ❌ Backend not reachable <br><br>
                Make sure FastAPI server is running.
            </div>
        `;

    } finally {

        scanBtn.disabled = false;
        scanBtn.innerText = "Scan URL";
    }
});