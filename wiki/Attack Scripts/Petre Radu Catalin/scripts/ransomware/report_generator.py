# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from datetime import datetime

class RansomwareReporter:
    @staticmethod
    def generate_report(
        target_dir: str,
        files_encrypted: int,
        encryption_algorithm: str,
        ransom_amount: str,
        payment_wallet: str,
        contact_email: str,
        simulation_version: str = "v1.0.0"
    ):
        soup = BeautifulSoup(features='html.parser')
        soup.append(soup.new_tag("!DOCTYPE html"))
        
        # HTML Structure
        html = soup.new_tag('html', lang='en')
        head = soup.new_tag('head')
        body = soup.new_tag('body')
        
        # Head Section
        meta = soup.new_tag('meta', charset='UTF-8')
        title = soup.new_tag('title')
        title.string = "Ransomware Simulation Report | Educational Tool"
        style = soup.new_tag('style')
        style.string = """
            body { font-family: 'Segoe UI', sans-serif; margin: 40px; background: #f8f9fa; }
            .header { 
                background: linear-gradient(135deg, #8B0000, #FF4500);
                color: white; 
                padding: 30px; 
                border-radius: 10px;
                margin-bottom: 30px;
            }
            .report-table {
                width: 100%;
                border-collapse: collapse;
                box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                background: white;
            }
            .report-table th {
                background: #8B0000;
                color: white;
                padding: 15px;
                text-align: left;
            }
            .report-table td {
                padding: 12px;
                border-bottom: 1px solid #eee;
            }
            .legal {
                margin-top: 40px;
                padding: 20px;
                background: #fff3cd;
                border-left: 4px solid #ffc107;
                color: #856404;
                border-radius: 5px;
            }
            .signature {
                margin-top: 30px;
                padding: 15px;
                background: #e9ecef;
                text-align: center;
                border-radius: 5px;
            }
            .ransom-note {
                margin: 20px 0;
                padding: 20px;
                background: #ffe6e6;
                border-left: 4px solid #ff0000;
                border-radius: 5px;
            }
        """
        
        head.extend([meta, title, style])
        
        # Body Content
        # Header
        header = soup.new_tag('div', **{'class': 'header'})
        h1 = soup.new_tag('h1')
        h1.string = "Ransomware Simulation Report"
        header.append(h1)
        body.append(header)
        
        # Metadata Table
        meta_table = soup.new_tag('table', **{'class': 'report-table'})
        header_row = soup.new_tag('tr')
        header_row.append(soup.new_tag('th', string="Attack Parameters"))
        header_row.append(soup.new_tag('th', string="Values"))
        meta_table.append(header_row)
        
        rows = [
            ("Target Directory", target_dir),
            ("Files Encrypted", f"{files_encrypted}"),
            ("Encryption Algorithm", encryption_algorithm),
            ("Simulation Date", datetime.now().strftime("%Y-%m-%d %H:%M")),
            ("Tool Version", simulation_version),
            ("Ransom Amount", ransom_amount),
            ("Payment Wallet", payment_wallet),
            ("Contact Email", contact_email)
        ]
        
        for row in rows:
            tr = soup.new_tag('tr')
            td1 = soup.new_tag('td', string=row[0])
            td2 = soup.new_tag('td', string=str(row[1]))
            tr.append(td1)
            tr.append(td2)
            meta_table.append(tr)
        
        body.append(meta_table)
        
        # Ransom Note Section
        ransom_note_div = soup.new_tag('div', **{'class': 'ransom-note'})
        ransom_note_div.append(soup.new_tag('h3', string="Simulated Ransom Note"))
        note_content = f"""
            <p>Your files have been encrypted!</p>
            <p>To decrypt your files, pay {ransom_amount} to {payment_wallet}.</p>
            <p>Contact us at {contact_email} after payment.</p>
            <p><strong>WARNING:</strong> Do not attempt to decrypt files without paying. This is a simulation.</p>
        """
        ransom_note_div.append(BeautifulSoup(note_content, 'html.parser'))
        body.append(ransom_note_div)
        
        # Legal Disclaimer
        legal = soup.new_tag('div', **{'class': 'legal'})
        legal.append(soup.new_tag('h3', string="Simulation Disclaimer"))
        legal.append(soup.new_tag('p', string="This report is part of a ransomware simulation conducted for educational purposes only. Key points:"))
        ul = soup.new_tag('ul')
        ul.extend([
            soup.new_tag('li', string="No actual files were encrypted or harmed."),
            soup.new_tag('li', string="This simulation does not execute real encryption or malicious actions."),
            soup.new_tag('li', string="Conducted in a controlled environment with proper authorization."),
            soup.new_tag('li', string="Unauthorized use of such simulations is illegal and unethical.")
        ])
        legal.append(ul)
        legal.append(soup.new_tag('p', string="Always comply with laws and ethical guidelines when conducting security tests."))
        body.append(legal)
        
        # Signature Block
        signature = soup.new_tag('div', **{'class': 'signature'})
        signature.append(soup.new_tag('p', string="Generated by:"))
        sig_text = soup.new_tag('div', style="margin-top:10px; font-weight:bold; color: #2c3e50")
        sig_text.string = "Petre Radu Catalin | Certified Ethical Hacker"
        signature.append(sig_text)
        signature.append(soup.new_tag('p', style="margin-top:5px;", 
                                    string=f"© {datetime.now().year} LunaLynx12. All rights reserved."))
        body.append(signature)
        
        # Final Assembly
        html.extend([head, body])
        soup.append(html)
        
        # Save Report
        filename = "ransomware_simulation_report.html"
        with open(filename, "w", encoding='utf-8') as f:
            f.write(soup.prettify())
        print(f"[+] Generated report: {filename}")