import hashlib
import os
import time
import shutil

import tkinter as tk
from tkinter import messagebox

# Predefined list of known malicious file hashes (for demonstration purposes)
malicious_hashes = {
    "malware.exe": "81051bcc2cf1bedf378224b0a93e2877",
    "suspicious.doc": "5a5ef08ff7480a7e0537670c69e9e65e"
}


def calculate_file_hash(file_path):
    """Calculate the MD5 hash of a file."""
    hasher = hashlib.md5()
    with open(file_path, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def scan_file(file_path):
    """Scan a file for potential malware."""
    file_name = os.path.basename(file_path)
    file_hash = calculate_file_hash(file_path)
    if file_name in malicious_hashes and file_hash == malicious_hashes[file_name]:
        print(f"Warning: {file_name} is identified as potential malware!")
        return True
    return False


def scan_directory(directory_to_scan):
    """Scan a directory for any new or modified files."""
    results = []
    try:
        print("Starting real-time scanning...")
        scanned_files = set()
        total_files = sum(len(files) for _, _, files in os.walk(directory_to_scan))
        files_scanned = 0
        while True:
            for root, _, files in os.walk(directory_to_scan):
                for file_name in files:
                    file_path = os.path.join(root, file_name)
                    # Check if the file has been scanned before
                    if file_path not in scanned_files:
                        print(f"Scanning {file_name}...")
                        if scan_file(file_path):
                            # Move the file to quarantine
                            quarantine_file(file_path)
                        scanned_files.add(file_path)
                        files_scanned += 1
                progress = (files_scanned / total_files) * 100
                print(f"Progress: {progress:.2f}%")
            time.sleep(10)  # Scan every 10 seconds
            if files_scanned == total_files:
                break
    except KeyboardInterrupt:
        print("\nScan interrupted by user.")
    return results


def quarantine_file(file_path):
    """Move a file to the quarantine directory."""
    quarantine_directory = "quarantine"
    if not os.path.exists(quarantine_directory):
        os.makedirs(quarantine_directory)
    shutil.move(file_path, os.path.join(quarantine_directory, os.path.basename(file_path)))
    print(f"{file_path} moved to quarantine.")


def main():
    # Path to the directory to scan
    directory_to_scan = "files_to_scan"
    try:
        # Start real-time scanning
        results = scan_directory(directory_to_scan)

        # Display results in a popup
        if results:
            show_popup("\n".join(results))
        else:
            show_popup("No threats fonud!")

    except KeyboardInterrupt:
        print("\nScan intrupted by user.")
        show_popup("Scan interrupted by user.")



def show_popup(message):
    """Display a popup with the given message."""
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    messagebox.showinfo("Scan Results", message)
    root.destroy()

if __name__ == "__main__":
    main()