# 📘 DVWA Exploitation Guide (Burp Suite + SQLMap)

## 🎯 Objective

The goal of this exercise is to:

1. Brute-force the DVWA login form using **Burp Suite Intruder** and the `rockyou.txt` password list.
2. Use **SQLMap** to exploit a SQL Injection vulnerability in DVWA and extract data from the backend database.

---

## 🛠️ Prerequisites

- A virtual lab with **DVWA (Damn Vulnerable Web Application)** running.
- **Burp Suite** installed (Community or Professional Edition).
- **SQLMap** installed.
- Kali Linux or a similar penetration testing environment.
- The **rockyou.txt** wordlist, usually located at `/usr/share/wordlists/rockyou.txt.gz`.

---

## 🧩 Step 1: Setup and Prepare DVWA

1. **Launch DVWA**:
   - Open a browser and go to your DVWA instance (e.g., `http://127.0.0.1/dvwa/`).

![DVWA main page](https://github.com/LunaLynx12/GISC/blob/main/wiki/Attack%20Scripts/Posea%20Alina/images/1.png?raw=true)



2. **Login with Default Credentials**:
   - Username: `admin`
   - Password: `password`
   - Click **Login**.

3. **Set DVWA Security Level to Low**:
   - Navigate to the **DVWA Security** tab.
   - Set the security level to **Low** and click **Submit**.

---

## 🔍 Step 2: Configure Burp Suite

1. **Start Burp Suite**.
2. Go to the **Proxy → Intercept** tab and make sure **Intercept is ON**.

![Burp suite intercept](https://github.com/LunaLynx12/GISC/blob/main/wiki/Attack%20Scripts/Posea%20Alina/images/2.png?raw=true)

3. Go to **Proxy → Options** and verify that Burp is listening on **127.0.0.1:8080**.
4. Configure your browser to use the proxy:
   - HTTP Proxy: `127.0.0.1`
   - Port: `8080`
5. Open DVWA in your browser again while Burp is running.

---

## 🧪 Step 3: Capture the Login Request

1. Navigate back to the **DVWA login page**.
2. Type in any username and password (e.g., `test` / `test`).
3. Submit the form.
4. Go to Burp and check the **Proxy → HTTP history** tab.
5. Locate the POST request to `login.php`.
6. Right-click on the request and choose **Send to Intruder**.

---

## 🎯 Step 4: Brute-Force Login Using Burp Suite Intruder

1. Switch to the **Intruder** tab in Burp Suite.

![Burp suite Intruder 1](https://github.com/LunaLynx12/GISC/blob/main/wiki/Attack%20Scripts/Posea%20Alina/images/3.png?raw=true)

2. Go to the **Positions** sub-tab.
3. You’ll see several parameters with `§` markers.
   - Click **Clear** to remove all positions.
   - Highlight only the **username** and **password** values.
   - Click **Add** to mark them as payload positions.
   - You’ll now have 2 positions: one for username, one for password.

![Burp suite Intruder 2](https://github.com/LunaLynx12/GISC/blob/main/wiki/Attack%20Scripts/Posea%20Alina/images/4.png?raw=true)

4. Go to the **Payloads** tab.
5. For **Payload Set 1 (username)**:
   - Enter a single payload like `admin`.
6. For **Payload Set 2 (password)**:
   - Click **Load** and select the wordlist: `/usr/share/wordlists/rockyou.txt`.
   - If it’s compressed (`.gz`), extract it first:

     ```bash
     gunzip /usr/share/wordlists/rockyou.txt.gz
     ```

7. Click **Start Attack** (Community Edition is slower but works).
8. Monitor the **response length** or **status code**:
   - Look for a different length or message indicating a successful login.

![Burp suite Intruder 3](https://github.com/LunaLynx12/GISC/blob/main/wiki/Attack%20Scripts/Posea%20Alina/images/5.png?raw=true)

---

### 🧩 Step 5: Navigate to the CSRF Module

1. Open the DVWA application in your browser.
2. From the main menu, click on the **CSRF** module.

![CSRF Module](https://github.com/LunaLynx12/GISC/blob/main/wiki/Attack%20Scripts/Posea%20Alina/images/6.png?raw=true)

---

### 🧪 Step 6: Analyze the CSRF Form

1. Observe the form presented in the CSRF module.
2. Note the fields available, such as the **password** field and the **Submit** button.

![CSRF Form](https://github.com/LunaLynx12/GISC/blob/main/wiki/Attack%20Scripts/Posea%20Alina/images/7.png?raw=true)

---

### 🛠️ Step 7: Intercept the Request with Burp Suite

1. Turn **Intercept ON** in Burp Suite.
2. Submit the form with any input (e.g., a test password).
3. Capture the HTTP request in Burp Suite.

![Intercept Request](https://github.com/LunaLynx12/GISC/blob/main/wiki/Attack%20Scripts/Posea%20Alina/images/8.png?raw=true)

---

### 🧠 Step 8: Craft a Malicious CSRF Exploit

1. Copy the intercepted request details.
2. Create a malicious HTML form that mimics the CSRF request.
3. Example of a crafted CSRF exploit form:

   ```html
   <form action="http://<DVWA-IP>/dvwa/vulnerabilities/csrf/" method="POST">
       <input type="hidden" name="password_new" value="maliciouspassword">
       <input type="hidden" name="password_conf" value="maliciouspassword">
       <input type="hidden" name="Change" value="Change">
       <input type="submit" value="Submit">
   </form>
   ```

4. Save the HTML file and open it in a browser.

![Crafted Exploit](https://github.com/LunaLynx12/GISC/blob/main/wiki/Attack%20Scripts/Posea%20Alina/images/9.png?raw=true)

---

### 🚀 Step 9: Execute the Exploit

1. Host the crafted HTML file on a web server or open it locally.
2. When the victim accesses the malicious page, the form will automatically submit the request to DVWA.
3. Verify that the password has been changed in DVWA.

![Exploit Execution](https://github.com/LunaLynx12/GISC/blob/main/wiki/Attack%20Scripts/Posea%20Alina/images/10.png?raw=true)

---

### 🔒 Step 10: Mitigation and Prevention

1. Implement anti-CSRF tokens in forms to prevent such attacks.
2. Educate users about the risks of clicking on unknown links or visiting untrusted websites.
3. Regularly update and patch web applications to address known vulnerabilities.




## ⚙️ Step 11: Identify SQL Injection Point in DVWA

1. Go to the **DVWA main menu**.
2. Click on the **SQL Injection** module.
3. Enter a numeric ID like `1` in the form and click **Submit**.
4. If the app displays user data, it's likely vulnerable.

![SQL Injection 1](https://github.com/LunaLynx12/GISC/blob/main/wiki/Attack%20Scripts/Posea%20Alina/images/11.png?raw=true)

---

## 🧠 Step 12: Intercept and Copy the Request

1. Turn **Intercept ON** again in Burp.
2. Submit the SQL injection form with a basic input like `1`.

![SQL Injection 2](https://github.com/LunaLynx12/GISC/blob/main/wiki/Attack%20Scripts/Posea%20Alina/images/12.png?raw=true)

3. In Burp, go to the **HTTP History** tab.
4. Find the GET or POST request related to the SQL Injection module.
5. Right-click → **Copy to file** or note down the **full request** and **cookies**.


![SQL Injection 3](https://github.com/LunaLynx12/GISC/blob/main/wiki/Attack%20Scripts/Posea%20Alina/images/13.png?raw=true)

---

## 🧨 Step 13: Use SQLMap to Exploit the SQL Injection

There are two ways: using the URL or using the full request saved to a file.

### Option A: Use SQLMap with URL and Cookies

```bash
sqlmap -u "http://<IP>/dvwa/vulnerabilities/sqli/?id=1&Submit=Submit" --cookie="PHPSESSID=xyz; security=low" --dbs --batch
```

Replace:

<IP> with your DVWA host IP.

PHPSESSID=xyz with your actual session ID from Burp.

![SQLMap 1](https://github.com/LunaLynx12/GISC/blob/main/wiki/Attack%20Scripts/Posea%20Alina/images/14.png?raw=true)

Option B: Use SQLMap with a Burp Request File
Save the full HTTP request in Burp (Right-click → Save item).

Run:

```bash
sqlmap -r request.txt --batch --dbs
```
This tells SQLMap to use the exact request as intercepted by Burp.

![SQLMap 2](https://github.com/LunaLynx12/GISC/blob/main/wiki/Attack%20Scripts/Posea%20Alina/images/15.png?raw=true)

![SQLMap 3](https://github.com/LunaLynx12/GISC/blob/main/wiki/Attack%20Scripts/Posea%20Alina/images/16.png?raw=true)

## 🧬 Step 14: Dump Database Contents
Once SQLMap finds the database names, you can:

Get tables:

```bash
sqlmap -u "<target>" -D dvwa --tables --cookie="PHPSESSID=xyz; security=low"
```

![SQLMap 4](https://github.com/LunaLynx12/GISC/blob/main/wiki/Attack%20Scripts/Posea%20Alina/images/17.png?raw=true)


![SQLMap 5](https://github.com/LunaLynx12/GISC/blob/main/wiki/Attack%20Scripts/Posea%20Alina/images/18.png?raw=true)

Dump data:

```bash
sqlmap -u "<target>" -D dvwa -T users -C user,password --dump --cookie="PHPSESSID=xyz; security=low"
```

![SQLMap 6](https://github.com/LunaLynx12/GISC/blob/main/wiki/Attack%20Scripts/Posea%20Alina/images/19.png?raw=true)

![SQLMap 7](https://github.com/LunaLynx12/GISC/blob/main/wiki/Attack%20Scripts/Posea%20Alina/images/20.png?raw=true)

![SQLMap 8](https://github.com/LunaLynx12/GISC/blob/main/wiki/Attack%20Scripts/Posea%20Alina/images/21.png?raw=true)

## Next step:

Set security level back to Medium or High for further testing.

