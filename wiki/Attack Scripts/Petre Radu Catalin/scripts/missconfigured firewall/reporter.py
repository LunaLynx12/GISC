from datetime import datetime

def generate_firewall_report(ip, findings, output_file="firewall_misconfig_report.html"):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    total_ports = len(findings)

    rows = ""
    for f in findings:
        rows += f"""
        <tr>
            <td>{f['port']}</td>
            <td>{f['service']}</td>
            <td>{f['banner']}</td>
        </tr>
        """

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Firewall Misconfiguration Report</title>
    <style>
        body {{ font-family: Arial; background: #f4f4f4; padding: 40px; color: #333; }}
        .header {{ background: #dc3545; color: white; padding: 20px; border-radius: 8px; }}
        .report-table {{ margin-top: 20px; border-collapse: collapse; width: 100%; background: white; }}
        .report-table th, .report-table td {{ padding: 12px; border: 1px solid #ccc; }}
        .report-table th {{ background-color: #343a40; color: white; }}
        .disclaimer {{ margin-top: 40px; padding: 20px; background: #fff3cd; color: #856404; border-left: 5px solid #ffc107; border-radius: 5px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Firewall Misconfiguration Report</h1>
        <p>Target IP: <strong>{ip}</strong></p>
        <p>Scan Time: <strong>{now}</strong></p>
    </div>

    <h2>Open Risky Ports</h2>
    <table class="report-table">
        <tr>
            <th>Port</th>
            <th>Service</th>
            <th>Banner</th>
        </tr>
        {rows}
    </table>

    <div class="disclaimer">
        <h3>Disclaimer - Educational Simulation</h3>
        <ul>
            <li>This is a simulated assessment for educational purposes.</li>
            <li>No exploitation or damage was attempted or performed.</li>
            <li>Only well-known ports were scanned.</li>
        </ul>
    </div>
</body>
</html>"""

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[+] Report saved to {output_file}")
