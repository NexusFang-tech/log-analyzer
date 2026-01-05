#!/usr/bin/env python3
"""
Basic Log Analyzer for Threat Detection
Author: Matthew Scott Keith Jr.
Purpose: Identify suspicious authentication activity from logs
"""
import pandas as pd
import re
import matplotlib.pyplot as plt

def parse_logs(file_path):
    records = []
    with open(file_path, "r") as file:
        for line in file:
            match = re.match(
                r"(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2}) (\S+) (\S+) (.*)",
                line
            )
            if match:
                records.append({
                    "date": match.group(1),
                    "time": match.group(2),
                    "ip": match.group(3),
                    "user": match.group(4),
                    "event": match.group(5)
                })
    df = pd.DataFrame(records)
    print(f"[*] Parsed {len(df)} log records.")
    if len(df) > 0:
        print("Sample record:", df.iloc[0].to_dict())
    else:
        print("[!] No logs parsed. Check if 'sample_logs.txt' exists and matches the format: 'YYYY-MM-DD HH:MM:SS IP user event_message'. Or adjust the regex.")
    return df

def detect_bruteforce(df, threshold=5):
    if df.empty or "event" not in df.columns:
        print("[!] Empty DataFrame or missing 'event' column. No analysis possible.")
        return pd.Series()
    failed = df[df["event"].str.contains("failed", case=False)]
    print(f"[*] Found {len(failed)} failed events.")
    ip_counts = failed["ip"].value_counts()
    suspicious_ips = ip_counts[ip_counts >= threshold]
    print("\nSuspicious IPs (Possible Brute Force):")
    print(suspicious_ips)
    return suspicious_ips

def visualize_attempts(ip_counts):
    if not ip_counts.empty:
        ip_counts.plot(kind="bar")
        plt.title("Failed Login Attempts by IP")
        plt.xlabel("IP Address")
        plt.ylabel("Failed Attempts")
        plt.tight_layout()
        plt.savefig("failed_attempts.png")
        print("[*] Graph saved to 'failed_attempts.png'.")
    else:
        print("[*] No suspicious IPs to visualize.")

def main():
    log_file = "sample_logs.txt"
    print("[*] Parsing logs...")
    df = parse_logs(log_file)
    print("[*] Detecting suspicious activity...")
    suspicious = detect_bruteforce(df)
    visualize_attempts(suspicious)

if __name__ == "__main__":
    main()