import json
from sklearn.ensemble import RandomForestClassifier
import pandas as pd

# Dummy model logic – replace with your trained model
def classify(log_file):
    df = pd.read_json(log_file)
    df['threat_level'] = df['severity'].apply(lambda x: 'High' if x > 7 else 'Low')
    df.to_csv('logs/classified_results.csv')
    print("Threat classification complete.")

if __name__ == "__main__":
    classify('logs/zap_results.json')  # Example input
