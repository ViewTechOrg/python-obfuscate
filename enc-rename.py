import requests
import json

def obfuscate_code_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        source_code = file.read()

    payload = {
        "append_source": True,
        "remove_docstrings": True,
        "rename_nondefault_parameters": True,
        "rename_default_parameters": False,
        "preserve": "",
        "source": source_code
    }

    headers = {
        "Content-Type": "application/json",
        "Origin": "https://pyob.oxyry.com",
        "Referer": "https://pyob.oxyry.com/",
        "User-Agent": "Mozilla/5.0 (Linux; Android 10)"
    }

    try:
        response = requests.post("https://pyob.oxyry.com/obfuscate", headers=headers, json=payload)
        response.raise_for_status()

        # Ambil hasil obfuscasi dari key 'dest'
        result = response.json()
        obfuscated_code = result.get("dest", "")

        # Simpan ke file baru
        with open("output_obfuscated.py", "w", encoding="utf-8") as out:
            out.write(obfuscated_code)

        print("[✓] Obfuscate selesai! Hasil disimpan di: output_obfuscated.py")

    except requests.RequestException as e:
        print(f"[!] Gagal kirim ke server: {e}")
    except Exception as e:
        print(f"[!] Error lain: {e}")

if __name__ == "__main__":
    file = input("Input File Source: ")
    obfuscate_code_from_file(file)
