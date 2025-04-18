## Setting Up Nessus on Kali Linux

### Installation Process:
```bash
    wget https://www.tenable.com/downloads/api/v1/public/pages/nessus/downloads/<version>/download?i_agree_to_tenable_license_agreement=true -O Nessus.deb
    sudo dpkg -i Nessus.deb
```

### First-Run service:
- Initialize service:

    ```bash
    sudo /bin/systemctl start nessusd.service
    ```

- Browser configuration:
    - Navigate to https://<kali-ip>:8834
    - Accept self-signed certificate
    - Create admin account using the following credentials:
        - **username:** admin
        - **password:** unitbv

### Plugin Update Monitoring:
```bash
    tail -f /opt/nessus/var/nessus/logs/nessusd.messages
```

Wait for "All plugins loaded" message. It takes a minimum of 30 minutes for Nessus to compile its plugins. During this time, the tool cannot be used.

## Configuring a New Nessus Scan

### Objective
Analyze vulnerabilities on a server running DVWA (Damn Vulnerable Web Application) in the same network as Kali Linux.

### Steps
1. Click on **New Scan** and select **Basic Network Scan**.
2. In the **Targets** field, enter the IP address of the DVWA virtual machine.

![nessus new scan](/wiki/Attack%20Scripts/Ginerica%20Alexandru/images/1.png)

3. Navigate to **Discovery Settings** and ensure **Host Discovery** is enabled.
4. Under **Scan Configuration**, select **Scan All TCP Ports** to ensure all ports are scanned.
5. In **Advanced Settings**, enable **Safe Checks** to prevent crashing services.
6. Save the configuration and launch the scan.
7. Monitor the scan progress and review detected vulnerabilities upon completion.

![nessus new scan result](/wiki/Attack%20Scripts/Ginerica%20Alexandru/images/2.png)

The results weren't that usefull so we decided to try something else

## Verifying DVWA Activity

To confirm that DVWA is active:
1. Run the following command to scan the DVWA server:
    ```bash
    sudo nmap -sS -sV -O -T4 <dvwa-ip>
    ```
This command returned an Apache server running on port 80, which may be vulnerable to exploitation.

![nmap scan](/wiki/Attack%20Scripts/Ginerica%20Alexandru/images/3.png)

2. Access the DVWA site at `http://<dvwa-ip>/DVWA`.

![dvwa homepage](/wiki/Attack%20Scripts/Ginerica%20Alexandru/images/4.png)

## Adjusting DVWA Security Settings
- Navigate to the **DVWA Security** tab.
- Change the security level from **Impossible** (default) to **Low** to enable exploitation.

## Manual Exploitation Procedures

### 1. Command Injection (CWE-78)
- In the **IP Address** section of the **Command Injection** section, input any IP address followed by a semicolon (`;`) to execute chained commands.

#### Commands Used:
- `ls` - Lists elements in a folder.

![command injection 1](/wiki/Attack%20Scripts/Ginerica%20Alexandru/images/5.png)

- `whoami` - Displays the current user.

![command injection 2](/wiki/Attack%20Scripts/Ginerica%20Alexandru/images/6.png)

- `cat` - Prints the content of a file.

![command injection 3](/wiki/Attack%20Scripts/Ginerica%20Alexandru/images/7.png)

## 2. SQL Injection (CWE-89)

- Used the following command to retrieve all valid usernames:
  ```sql
  ' OR '1' = '1
  ```

![sql injection 1](/wiki/Attack%20Scripts/Ginerica%20Alexandru/images/8.png)

- To dump usernames and passwords hashes from the database:
  ```sql
  ' UNION SELECT user, password FROM users#
  ```

![sql injection 2](/wiki/Attack%20Scripts/Ginerica%20Alexandru/images/9.png)

#### Password Cracking
- Extracted hashed passwords were cracked using **John the Ripper**.
- Followed the tutorial at [Kali Wordlists](https://www.kali.org/tools/wordlists/) to extract the `rockyou.txt` wordlist.

![rockyou extraction](/wiki/Attack%20Scripts/Ginerica%20Alexandru/images/10.png)

- Saved the hashes in a `.txt` file and ran **John the Ripper** to reveal the plaintext passwords.

![saved hashes](/wiki/Attack%20Scripts/Ginerica%20Alexandru/images/11.png)

#### John the Ripper command:

```bash
john --format=raw-md5 hashes --wordlist=/usr/share/wordlists/rockyou.txt
```

![john the ripper](/wiki/Attack%20Scripts/Ginerica%20Alexandru/images/12.png)

## 3. Cross-Site Scripting (XSS) (CWE-79)

#### Reflected XSS
![reflected xss 1](/wiki/Attack%20Scripts/Ginerica%20Alexandru/images/14.png)

- Injected a JavaScript `alert` function to display a pop-up with our names.

![reflected xss 2](/wiki/Attack%20Scripts/Ginerica%20Alexandru/images/13.png)

#### Stored XSS
- Similar to Reflected XSS, but input length limitations required us to shorten our names.

![stored xss 1](/wiki/Attack%20Scripts/Ginerica%20Alexandru/images/15.png)

- To bypass the character limit, we created a JavaScript file named `evil.js` containing a larger payload.

![stored xss 3](/wiki/Attack%20Scripts/Ginerica%20Alexandru/images/17.png)

- Hosted the file using Python's `http.server` module.

#### Http.server command:

![stored xss 5](/wiki/Attack%20Scripts/Ginerica%20Alexandru/images/19.png)

```bash
sudo python3 -m http.server 80
```

![stored xss 2](/wiki/Attack%20Scripts/Ginerica%20Alexandru/images/16.png)


#### Testing the Payload
- Verified that the `evil.js` script was accessible and functional.

![stored xss 4](/wiki/Attack%20Scripts/Ginerica%20Alexandru/images/18.png)

## Risk Assessment Matrix

| Vulnerability   | CVSS Score | Impact  | Complexity |
|------------------|------------|---------|------------|
| Command Inj.     | 9.8        | High    | Low        |
| SQLi             | 9.1        | High    | Medium     |
| Stored XSS       | 7.4        | Medium  | High       |

## Next Steps
- Explore manual exploitation techniques for additional vulnerabilities.
- Develop automation scripts to streamline the exploitation process.
