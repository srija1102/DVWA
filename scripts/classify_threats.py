# import os
# import pandas as pd

# def classify(log_file):
#     if not os.path.exists(log_file):
#         print(f"⚠️ File '{log_file}' not found. Skipping classification.")
#         return

#     try:
#         df = pd.read_json(log_file)
#         if 'severity' not in df.columns:
#             print("⚠️ No 'severity' column found. Classification skipped.")
#             return

#         # Normalize severity string and classify
#         df['threat_level'] = df['severity'].str.upper().apply(
#             lambda x: 'High' if x in ['HIGH', 'CRITICAL'] else 'Low'
#         )
#         df.to_csv('logs/classified_results.csv', index=False)
#         print(f"✅ Threat classification complete for {log_file}. Output: logs/classified_results.csv")

#     except Exception as e:
#         print(f"❌ Error during classification: {e}")

# if __name__ == "__main__":
#     if os.path.exists('logs/zap_results.json'):
#         classify('logs/zap_results.json')
#     elif os.path.exists('logs/checkov.json'):
#         classify('logs/checkov.json')
#     elif os.path.exists('logs/trivy_results.json'):
#         classify('logs/trivy_results.json')
#     else:
#         print("❌ No log files found. Cannot perform classification.")



import os
import pandas as pd
import json

def classify_severity(severity):
    if not severity:
        return 'Unknown'
    severity = severity.upper()
    if severity in ['HIGH', 'CRITICAL']:
        return 'High'
    else:
        return 'Low'


def parse_zap(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    alerts = data.get('site', [{}])[0].get('alerts', [])
    records = []
    for alert in alerts:
        records.append({
            'tool': 'ZAP',
            'name': alert.get('name'),
            'description': alert.get('description'),
            'severity': alert.get('riskdesc', '').split(' ')[0]  # Extracts e.g., "High (Medium)"
        })
    return pd.DataFrame(records)

def parse_checkov(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    records = []
    for result in data.get('results', {}).get('failed_checks', []):
        records.append({
            'tool': 'Checkov',
            'name': result.get('check_id'),
            'description': result.get('check_name'),
            'severity': result.get('severity')
        })
    return pd.DataFrame(records)

def parse_trivy(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    records = []
    for result in data.get('Results', []):
        for vuln in result.get('Vulnerabilities', []):
            records.append({
                'tool': 'Trivy',
                'name': vuln.get('VulnerabilityID'),
                'description': vuln.get('Title'),
                'severity': vuln.get('Severity')
            })
    return pd.DataFrame(records)

def classify_logs():
    dfs = []
    if os.path.exists('logs/zap_results.json'):
        print("✅ Processing ZAP results")
        dfs.append(parse_zap('logs/zap_results.json'))
    if os.path.exists('logs/checkov.json'):
        print("✅ Processing Checkov results")
        dfs.append(parse_checkov('logs/checkov.json'))
    if os.path.exists('logs/trivy_results.json'):
        print("✅ Processing Trivy results")
        dfs.append(parse_trivy('logs/trivy_results.json'))

    if not dfs:
        print("❌ No log files found. Cannot perform classification.")
        return

    combined_df = pd.concat(dfs, ignore_index=True)

    if 'severity' not in combined_df.columns or combined_df.empty:
        print("⚠️ No 'severity' data found. Classification skipped.")
        return

    combined_df['threat_level'] = combined_df['severity'].apply(classify_severity)

    os.makedirs('logs', exist_ok=True)
    output_file = 'logs/classified_results.csv'
    combined_df.to_csv(output_file, index=False)
    print(f"✅ Threat classification complete. Output: {output_file}")

if __name__ == "__main__":
    classify_logs()
