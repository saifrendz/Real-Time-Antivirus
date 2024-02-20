import hashlib

def calculate_file_hash(file_path):
    """Calculate the MD5 hash of a file."""
    hasher = hashlib.md5()
    with open(file_path, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

file_path = "files_to_scan/malware.exe"
file_hash = calculate_file_hash(file_path)
print("MD5 hash of malware.exe:", file_hash)