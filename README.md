# 🏢 Company Verification Tool

A web-based tool built using **Streamlit**, **web scraping**, and **WHOIS analysis** to verify the legitimacy of Indian companies. It performs multiple verification checks including government registration, domain age, trade history, and potential scam reports using live data scraping from official and public sources.

---

## ✅ Features

- **MCA Registration Check** – Verifies if the company is registered on the Ministry of Corporate Affairs (MCA) India portal.
- **MSME Status Lookup** – Checks if the company is a registered MSME (static placeholder due to API restrictions).
- **RBI NBFC Validation** – Checks for NBFC registrations using RBI lists (Active NBFCs and Microfinance NBFCs).
- **Zauba Trade History Check** – Scrapes Zauba to analyze trade activity.
- **Domain WHOIS Analysis** – Retrieves domain age and registrar information.
- **News Sentiment Scan** – Searches for potential scam-related news on top financial portals like Livemint and Economic Times.
- **Composite Risk Scoring** – Generates a normalized score (0–100) with a final verdict: ✅ LEGITIMATE, ⚠️ NEEDS REVIEW, or 🚩 HIGH RISK.
- **JSON Output** – All checks and scores are consolidated into a structured JSON report.

---

## 🚀 Demo

To run the tool:

```bash
streamlit run app.py
````

Replace `app.py` with the name of your script file.

---

## 🔧 Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/company-verification-tool.git
   cd company-verification-tool
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

   **requirements.txt**

   ```
   streamlit
   requests
   beautifulsoup4
   python-whois
   ```

3. **Run the app:**

   ```bash
   streamlit run your_script.py
   ```

---

## 📦 JSON Report Sample

```json
{
  "company_name": "ABC Technologies Pvt Ltd",
  "verdict": "✅ LEGITIMATE",
  "composite_score": 82.3,
  "checks": {
    "mca": {"status": "REGISTERED", "confidence": 90, "source": "MCA"},
    "msme": {"status": "UNKNOWN", "confidence": 30, "source": "MSME"},
    "rbi_nbfc": {"is_registered": false, "confidence": 70, "source": "RBI"},
    "zauba": {"has_trade_history": true, "confidence": 80, "source": "Zauba"},
    "domain": {"domain": "abctechnologies.com", "age_years": 5.2, "confidence": 95, "source": "WHOIS"},
    "news": {"scam_reports": [], "confidence": 100, "source": "News"}
  }
}
```

---

## 🧠 Tech Stack

* **Frontend/UI**: Streamlit
* **Web Scraping**: BeautifulSoup, Requests
* **Domain Intelligence**: `whois`
* **NLP Filter**: Regex + Keyword match for scam detection

---

## ⚠️ Disclaimer

This tool uses **public data** and **web scraping**. Some results may vary due to network restrictions or real-time changes in target websites. Always cross-check from official government sources when in doubt.

---

## 📬 Contact

For feedback or contributions, reach out at: \[[swapb2704@gmail.com](swapb2704@gmail.com)]

---

## 📜 License

MIT License – Feel free to fork and enhance for educational or non-commercial use.

```

