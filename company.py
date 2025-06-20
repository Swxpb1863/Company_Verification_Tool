import streamlit as st
import requests
from bs4 import BeautifulSoup
import whois
from datetime import datetime
from urllib.parse import quote
import re
import time
from difflib import SequenceMatcher

# --- Constants ---
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}
DELAY = 2

# --- Functions ---
def similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()

def check_mca_registration(company_name):
    try:
        url = f"https://www.mca.gov.in/mcafoportal/companySearch.do?companyName={quote(company_name)}"
        response = requests.get(url, headers=HEADERS)
        time.sleep(DELAY)
        if "No matching records found" in response.text:
            return {"status": "UNREGISTERED", "confidence": 0, "source": "MCA"}
        return {"status": "REGISTERED", "confidence": 90, "source": "MCA"}
    except Exception as e:
        return {"error": str(e), "confidence": 0, "source": "MCA"}

def check_msme_registration(company_name):
    try:
        return {"status": "UNKNOWN", "confidence": 30, "source": "MSME", "detail": "Live check restricted"}
    except Exception as e:
        return {"error": str(e), "confidence": 0, "source": "MSME"}

def check_rbi_nbfc(company_name):
    try:
        nbfc_lists = [
            ("Active NBFCs", "https://www.rbi.org.in/Scripts/bs_viewcontent.aspx?Id=2009"),
            ("Microfinance NBFCs", "https://www.rbi.org.in/Scripts/bs_viewcontent.aspx?Id=2078")
        ]
        for list_name, list_url in nbfc_lists:
            response = requests.get(list_url, headers=HEADERS)
            time.sleep(DELAY)
            if company_name.upper() in response.text:
                return {
                    "is_registered": True,
                    "confidence": 95,
                    "source": "RBI",
                    "list": list_name
                }
        return {
            "is_registered": False,
            "confidence": 70,
            "source": "RBI"
        }
    except Exception as e:
        return {"error": str(e), "confidence": 0, "source": "RBI"}

def scrape_zauba(company_name):
    try:
        url = f"https://www.zauba.com/company-{company_name.replace(' ', '-')}"
        response = requests.get(url, headers=HEADERS)
        time.sleep(DELAY)
        soup = BeautifulSoup(response.text, 'html.parser')
        if soup.find(string=re.compile("No records found")):
            return {"has_trade_history": False, "confidence": 30, "source": "Zauba"}
        else:
            return {"has_trade_history": True, "confidence": 80, "source": "Zauba"}
    except Exception as e:
        return {"error": str(e), "confidence": 0, "source": "Zauba"}

def analyze_domain(company_name):
    try:
        domain = f"{company_name.replace(' ', '').lower()}.com"
        w = whois.whois(domain)
        creation_date = w.creation_date[0] if isinstance(w.creation_date, list) else w.creation_date
        age_days = (datetime.now() - creation_date).days if creation_date else 0
        age_years = round(age_days / 365, 1)
        return {
            "domain": domain,
            "age_years": age_years,
            "registrar": w.registrar,
            "confidence": min(100, age_days / 365 * 100),
            "source": "WHOIS"
        }
    except:
        return {
            "error": "Domain invalid",
            "confidence": 0,
            "source": "WHOIS"
        }

def search_news(company_name):
    try:
        sources = [
            ("Livemint", f"https://www.livemint.com/search/{quote(company_name)}"),
            ("Economic Times", f"https://economictimes.indiatimes.com/topic/{quote(company_name)}")
        ]
        scam_reports = []
        for source_name, url in sources:
            response = requests.get(url, headers=HEADERS)
            time.sleep(DELAY)
            if "scam" in response.text.lower():
                scam_reports.append({"source": source_name, "url": url})
        confidence = 100 - len(scam_reports) * 25
        return {
            "scam_reports": scam_reports,
            "confidence": max(0, confidence),
            "source": "News"
        }
    except Exception as e:
        return {"error": str(e), "confidence": 50, "source": "News"}

def generate_verification_report(company_name):
    checks = {
        "mca": check_mca_registration(company_name),
        "msme": check_msme_registration(company_name),
        "rbi_nbfc": check_rbi_nbfc(company_name),
        "zauba": scrape_zauba(company_name),
        "domain": analyze_domain(company_name),
        "news": search_news(company_name)
    }

    weights = {
        "mca": 0.35,
        "msme": 0.25 if checks["msme"].get("status") == "REGISTERED" else 0.15,
        "rbi_nbfc": 0.3 if checks["rbi_nbfc"].get("is_registered", False) else 0.1,
        "domain": 0.2,
        "zauba": 0.15,
        "news": 0.05
    }

    composite_score = sum(
        check.get("confidence", 0) * weights[key] for key, check in checks.items()
    )
    composite_score = min(100, composite_score * (1 / sum(weights.values())))

    if composite_score >= 75:
        verdict = "✅ LEGITIMATE"
    elif composite_score >= 50:
        verdict = "⚠️ NEEDS REVIEW"
    else:
        verdict = "🚩 HIGH RISK"

    report = {
        "company_name": company_name,
        "verdict": verdict,
        "composite_score": round(composite_score, 1),
        "checks": checks,
        "weights": weights
    }
    return report

# --- Streamlit App ---
st.set_page_config(page_title="Company Verification", layout="centered")
st.title("🏢 Company Verification Engine")
st.markdown("Check MCA, MSME, RBI NBFC, WHOIS, News and Trade History")

company_name = st.text_input("Enter Company Name")
if st.button("Verify") and company_name:
    with st.spinner("Running verification checks..."):
        report = generate_verification_report(company_name)
    
    st.success(f"Final Verdict: {report['verdict']}")
    st.progress(int(report['composite_score']))

    st.subheader("📊 Composite Score")
    st.metric("Confidence Score", f"{report['composite_score']}/100")

    st.subheader("🔍 Detailed Results")
    for key, check in report["checks"].items():
        with st.expander(f"{key.upper()} ({check['source']})"):
            if "error" in check:
                st.error(f"Error: {check['error']}")
            else:
                st.info(f"Confidence: {check['confidence']} / 100")
                for k, v in check.items():
                    if k not in ["confidence", "source"]:
                        st.write(f"**{k.replace('_',' ').title()}**: {v}")
