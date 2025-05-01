import os
import pandas as pd

def classify(log_file):
    if not os.path.exists(log_file):
        print(f"⚠️ File '{log_file}' not found. Skipping classification.")
        return

    try:
        df = pd.read_json(log_file)
        if 'severity' not in df.columns:
            print("⚠️ No 'severity' column found. Classification skipped.")
            return

        # Normalize severity string and classify
        df['threat_level'] = df['severity'].str.upper().apply(
            lambda x: 'High' if x in ['HIGH', 'CRITICAL'] else 'Low'
        )
        df.to_csv('logs/classified_results.csv', index=False)
        print(f"✅ Threat classification complete for {log_file}. Output: logs/classified_results.csv")

    except Exception as e:
        print(f"❌ Error during classification: {e}")

if __name__ == "__main__":
    if os.path.exists('logs/zap_results.json'):
        classify('logs/zap_results.json')
    elif os.path.exists('logs/checkov.json'):
        classify('logs/checkov.json')
    elif os.path.exists('logs/trivy_results.json'):
        classify('logs/trivy_results.json')
    else:
        print("❌ No log files found. Cannot perform classification.")

