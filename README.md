

 🔍 Web Application Vulnerability Scanner

During my internship at Elevate Labs, I built a lightweight Python tool to help identify common web vulnerabilities. This scanner focuses on:

- ✅ Cross-Site Scripting (XSS)  
- ✅ SQL Injection (SQLi)  
- ✅ Cross-Site Request Forgery (CSRF)  

It’s mainly for educational and internal testing purposes — the idea is to simulate real-world attacks so developers can better understand and patch security holes.


 🛠️ What It Does

- Crawls websites automatically and extracts forms using BeautifulSoup  
- Injects payloads to test for XSS, SQLi, and CSRF vulnerabilities  
- Keeps detailed logs of every scan, including:  
  - When the scan happened  
  - What payloads were used  
  - How severe the vulnerabilities are  
- Comes with a simple Flask web interface for easy use  
- Lets you download the scan logs directly from the UI  



 🚀 Tools & Tech I Used

| Tool / Library     | What It’s For                              |
|--------------------|--------------------------------------------|
| Python 3           | The main language behind the tool          |
| Flask              | To build the web interface                  |
| Requests           | For sending HTTP requests                    |
| BeautifulSoup4     | Parsing HTML and grabbing forms             |
| Validators         | Making sure URLs are valid                   |
| HTML (index.html)  | The frontend UI                              |
| Kali Linux         | My dev and testing environment               |

