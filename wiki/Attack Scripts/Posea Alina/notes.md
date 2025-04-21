## Project Overview
- **Objective**: Identify and exploit vulnerabilities in a DVWA (Damn Vulnerable Web App) environment.
- **Scope**: Manual testing, automated scanning, and scripting for vulnerability validation.

## Tools Utilized
- **Burp Suite**: Used for intercepting web requests.
- **SQLMap**: Employed for automated SQL injection testing.

## Activities Performed

1. **Password Brute-Force on DVWA**
   - Accessed the DVWA (Damn Vulnerable Web Application) platform.
   - Used the `rockyou.gz` wordlist to brute-force the login credentials.
   - Successfully logged in as `admin` using the password from the wordlist.

2. **Burp Suite Intruder**
   - Enabled Intercept in Burp Suite to capture login requests.
   - Sent the captured request to the Intruder module.
   - Configured the Intruder with usernames and passwords as payloads.
   - Ran the attack and identified valid login credentials.

3. **SQL Injection with SQLMap**
   - Identified injectable fields.
   - Used SQLMap to automate the exploitation of SQL injection vulnerabilities.
   - Likely dumped data from the backend database.

## Contributors
**Primary Researcher:**

- **Posea Alina** (Lead Tester) – Conducted exploits, scans, and vulnerability validation

**Acknowledgments:**

- **Petre Radu** (Team Lead) – Helped with CSRF exploitation and converting the PDF report into markdown
