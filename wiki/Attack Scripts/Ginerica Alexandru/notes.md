## Project Overview
- **Objective**: Identify and exploit vulnerabilities in a DVWA (Damn Vulnerable Web App) environment.
- **Scope**: Manual testing, automated scanning, and scripting for vulnerability validation.

## Key Findings
✅ **Command Injection**: Executed system commands via DVWA input fields (; ls, ; whoami).

✅ **SQL Injection**: Extracted all user credentials using ' OR '1'='1 and UNION SELECT.

✅ **XSS Exploits**:
- Triggered reflected XSS via **alert()**.
- Bypassed input limits and hosted a malicious **javascript payload** via Python’s **http.server**.

✅ **Password Cracking**: Decrypted 5 hashes using **John the Ripper** + rockyou.txt.

## Tools Utilized
- **Kali Linux** – Primary penetration testing environment for exploits and security tools
- **Chrome DevTools** – Web vulnerability analysis, real-time payload testing, and debugging
- **Nessus** – Automated vulnerability scanning and assessment
- **John the Ripper** – Password hash cracking with **rockyou.txt** wordlist
- **Python HTTP Server** – Hosted malicious scripts for XSS payload delivery

## Contribuitors
**Primary Researcher:**

- **Ginerica Alexandru** (Lead Tester) – Conducted exploits, scans, and vulnerability validation

**Acknowledgments:**

- **Petre Radu** (Team Lead) – Critical debugging support using Chrome DevTools and markdown

- **Google CyberSeminars Instructors** – Foundational training on tooling and methodologies

## Next Steps
- Automate exploits with Python scripts.
- Test against "Medium" DVWA security level.
