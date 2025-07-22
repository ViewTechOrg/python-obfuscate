"""
SCRIPT INI DI BUAT OLEH VINDRA GANZZ MENGGUNAKAN METODE SNIFF
KAMU BISA PAKAI SCRIPT INI UNTUK ENCRYPT PYTHON
WEBSITE https://pyobfuscate.com
SCRIPT TIDAK PERLU SALIN ,LANGUSNG MASUKAN FILE .PY

@VINDRA GANZZ
TANKS
SEMUANYA ^__^
"""

import requests
from bs4 import BeautifulSoup
import re
import zlib
import string
import os
from fake_useragent import UserAgent
from requests import Session
ses = Session()
ses = UserAgent()
agent = ses.random

def read_source_code(file_path):
    try:
        with open(file_path, "r") as f:
            return f.read()
    except FileNotFoundError:
        print(f"File tidak ditemukan: {file_path}")
        exit()


def obfuscate_code(source_code):
    try:
        session = requests.Session()
        url = "https://pyobfuscate.com/pyd"
        session.get(url)

        headers = {
            "User-Agent": agent,
            "Content-Type": "application/x-www-form-urlencoded",
            "Referer": url,
            "Origin": "https://pyobfuscate.com"
        }

        res = session.post(url, headers=headers, data={"pyinput": source_code})
        soup = BeautifulSoup(res.text, "html.parser")
        textareas = soup.find_all("textarea")

        if len(textareas) < 2:
            print("Gagal mengambil hasil obfuscate.")
            exit()

        return textareas[1].text
    except Exception as e:
        print(f"agal saat proses obfuscate: {e}")
        exit()


def extract_hex_payload(obfuscated_code):
    match = re.search(r"'lIlIIIlIlIIIlI'\s*,\s*['\"]{3}(.*?)['\"]{3}", obfuscated_code, re.DOTALL)
    if not match:
        print("idak ditemukan hex terenkripsi.")
        exit()

    hex_data = match.group(1).strip()
    return ''.join(filter(lambda c: c in string.hexdigits, hex_data))


def decrypt_hex_payload(hex_string):
    try:
        compressed_bytes = bytes.fromhex(hex_string)
        decrypted_bytes = zlib.decompress(compressed_bytes)
        return decrypted_bytes.decode()
    except Exception as e:
        print(f"Gagal mendekripsi: {e}")
        exit()


def save_file(path, content):
    try:
        with open(path, "w") as f:
            f.write("# Obfuscate by Vindra Ganzz\n\n")
            f.write(content)
    except Exception as e:
        print(f"Gagal menyimpan file {path}: {e}")


def delete_file(path):
    try:
        os.remove(path)
        print(f"File sementara '{path}' dihapus.")
    except Exception as e:
        print(f"Gagal menghapus file: {e}")


def main():
    source_file = input("[>] Masukan File : ")
    output_obf = input(" [>] Output  File : ")
    output_decrypted = input("[>] Output Decrypt File : ")

    # Step 1: Baca source
    source_code = read_source_code(source_file)

    # Step 2: Obfuscate
    obfuscated_code = obfuscate_code(source_code)
    save_file(output_obf, obfuscated_code)
    print(f"File Hasil Berhasil di Encrypt: {output_obf}")

    # Step 3: Decrypt hex
    hex_string = extract_hex_payload(obfuscated_code)
    decrypted_code = decrypt_hex_payload(hex_string)
    save_file(output_decrypted, decrypted_code)
    print(f"File Hasil Decryprt: {output_decrypted}")


    # Step 4: Hapus file sementara
#    delete_file(output_obf)


if __name__ == "__main__":
    main()
