# PHPMyRecipes & Mutillidae II Testing

## Key Activities

### PHPMyRecipes SQL Injection
- Identified **SQLi vulnerability** in `words_exact` parameter via `/dosearch.php`
- Used sqlmap to:
  - Confirm vulnerability (`--data "words_exact=" -p words_exact`)
  - Extract database names (`--dbs`)
  - Dump `recipes.users` table (`-D recipes -T users --dump`)

### Mutillidae II XSS Testing
- Discovered reflected XSS in DNS lookup page
- Validated with XSSer tool:

  ```bash
  xsser --url 'http://192.94.37.3/index.php?page=dns-lookup.php' -p 'target_host=XSS&dns-lookup-php-submit-button=Lookup+DNS'

### CPU Mining Simulation

- Created Python script `cpu_mining_sim.py` to stress-test CPU cores (simulation for a crypto miner)

- Verified high CPU usage via **htop**

## Contribuitors
**Primary Researcher:**

- **Jose Zamora** (Lead Tester) – Conducted exploits, scans, and vulnerability validation

**Acknowledgments:**

- **Petre Radu** (Team Lead) Assisted with PDF-to-markdown conversion