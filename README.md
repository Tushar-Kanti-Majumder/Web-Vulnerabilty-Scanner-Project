# Web Application Vulnerability Scanner

A Python-based Web Application Vulnerability Scanner developed during my internship at **Elevate Labs**. This tool is designed to help identify common web vulnerabilities such as Cross-Site Scripting (XSS), SQL Injection (SQLi), and Cross-Site Request Forgery (CSRF) through automated scanning. It features a user-friendly Flask web interface and detailed logging for educational and internal security assessment purposes.

---

## Features

- **XSS Detection:** Scans web pages for potential Cross-Site Scripting vulnerabilities by injecting payloads and analyzing responses.
- **SQL Injection (SQLi) Detection:** Tests input fields and URL parameters for SQL injection flaws.
- **CSRF Detection:** Checks for missing or improper CSRF tokens in forms.
- **Logging:** Records scan results with timestamps, payloads used, and severity levels.
- **Web Interface:** Interactive Flask-based UI for easy scanning and result visualization.
- **Educational & Internal Use:** Intended for learning and internal security assessments only.

---

## Tools & Technologies Used

- **Python 3** — Core programming language
- **Flask** — Web framework for the user interface
- **Requests** — HTTP library for sending requests and interacting with web pages
- **BeautifulSoup** — HTML parsing and analysis
- **Kali Linux** — Development and testing environment (optional but recommended)
- Other dependencies listed in `requirements.txt`

---

## Setup Instructions

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/webapp-vuln-scanner.git
   cd webapp-vuln-scanner
