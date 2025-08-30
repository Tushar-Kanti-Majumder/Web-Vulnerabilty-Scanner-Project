from flask import Flask, render_template, request, send_file, flash, redirect, url_for
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
import os
import validators

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Needed for flash messages

# --- Get all forms on a web page ---
def get_forms(url):
    try:
        res = requests.get(url)
        soup = BeautifulSoup(res.content, "html.parser")
        return soup.find_all("form")
    except Exception as e:
        print(f"[ERROR] Failed to fetch forms from {url} — {e}")
        return []

# --- Submit form with a given payload ---
def submit_form(form, url, payload):
    action = form.get("action")
    method = form.get("method", "get").lower()
    inputs = form.find_all("input")
    data = {}

    for input_tag in inputs:
        name = input_tag.get("name")
        input_type = input_tag.get("type", "text")
        if name:
            data[name] = payload if input_type == "text" else "test"

    target_url = url + action if action else url
    try:
        if method == "post":
            return requests.post(target_url, data=data)
        else:
            return requests.get(target_url, params=data)
    except Exception as e:
        print(f"[ERROR] Form submission failed — {e}")
        return None

# --- Test for XSS vulnerabilities ---
def test_xss(url):
    forms = get_forms(url)
    payload = "<script>alert('XSS')</script>"
    results = []

    for i, form in enumerate(forms, start=1):
        response = submit_form(form, url, payload)
        if response and payload in response.text:
            severity = "Medium"
            msg = (
                f"[XSS] Vulnerability #{i} at {url}\n"
                f" - Severity: {severity}\n"
                f" - Payload: {payload}\n"
                f" - Form Action: {form.get('action')}\n"
                f" - Method: {form.get('method', 'GET').upper()}\n"
            )
            print(msg)
            results.append(msg)
        else:
            print(f"[XSS] No vulnerability found in form #{i} at {url}")
    return results

# --- Test for SQL Injection vulnerabilities ---
def test_sqli(url):
    forms = get_forms(url)
    payload = "' OR '1'='1"
    results = []

    sql_error_patterns = [
        r"you have an error in your sql syntax",
        r"warning: mysql",
        r"unclosed quotation mark",
        r"quoted string not properly terminated",
        r"syntax error.*?in query",
        r"mysql_fetch_array",
        r"pg_query\(\)",
        r"sqlstate\[\w+\]",
    ]

    for i, form in enumerate(forms, start=1):
        response = submit_form(form, url, payload)
        if response:
            for pattern in sql_error_patterns:
                if re.search(pattern, response.text, re.IGNORECASE):
                    severity = "High"
                    msg = (
                        f"[SQLi] Vulnerability #{i} at {url}\n"
                        f" - Severity: {severity}\n"
                        f" - Payload: {payload}\n"
                        f" - Form Action: {form.get('action')}\n"
                        f" - Method: {form.get('method', 'GET').upper()}\n"
                        f" - Matched Pattern: {pattern}\n"
                    )
                    print(msg)
                    results.append(msg)
                    break
            else:
                print(f"[SQLi] No vulnerability found in form #{i} at {url}")
    return results

# --- Route to download the latest scan results ---
@app.route("/download")
def download_results():
    path = "logs/scan_results.txt"
    if os.path.exists(path):
        return send_file(path, as_attachment=True)
    else:
        flash("No scan results available for download.", "error")
        return redirect(url_for("index"))

# --- Main Route ---
@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    history = ""
    if request.method == "POST":
        url = request.form["url"].strip()

        # Validate URL
        if not validators.url(url):
            flash("Invalid URL. Please enter a valid URL including http:// or https://", "error")
            return render_template("index.html", result="", history=get_scan_history())

        xss_results = test_xss(url)
        sqli_results = test_sqli(url)
        combined_results = xss_results + sqli_results

        if combined_results:
            result = "\n".join(combined_results)
        else:
            result = "No vulnerabilities detected."

        # Save results to log file with timestamp
        os.makedirs("logs", exist_ok=True)
        with open("logs/scan_results.txt", "a") as log_file:
            log_file.write(f"--- Scan on {datetime.now()} ---\n")
            log_file.write(f"Target URL: {url}\n")
            log_file.write(result + "\n\n")

        # Save to history file
        with open("logs/history.txt", "a") as hist_file:
            hist_file.write(f"{datetime.now()} - {url}\n")

    history = get_scan_history()
    return render_template("index.html", result=result, history=history)

def get_scan_history():
    history_path = "logs/history.txt"
    if os.path.exists(history_path):
        with open(history_path, "r") as f:
            return f.read()
    else:
        return ""

if __name__ == "__main__":
    app.run(debug=True)
