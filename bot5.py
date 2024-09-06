import requests
import json
import time
import re

# Fungsi untuk mengirim permintaan mining claim
def send_mining_claim_request(url, headers, payload):
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error during request: {e}")
        return None

# Fungsi utama program
def main():
    # URL endpoint API dan header permintaan
    url = "https://api.tontap.xyz/rewards/mining-claim?"
    headers = {
        "accept": "application/json",
        "accept-language": "en-US,en;q=0.9,id;q=0.8",
        "content-type": "application/json",
        "origin": "https://app.tontap.xyz",
        "referer": "https://app.tontap.xyz/",
        "sec-ch-ua": '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": '"Android"',
        "user-agent": "Mozilla/5.0 (Linux; Android 13; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36"
    }

    # Data payload untuk permintaan
    payload = {
        "totalTap": 50,
        "startTime": int(time.time())
    }

    all_clicks_below_100 = False  # Variabel untuk melacak semua akun di bawah 100 klik

    while True:  # Loop tak terbatas
        try:
            with open("data.json", "r") as file:
                data = json.load(file)
                auth_datas = data.get("auth_datas", [])

        except FileNotFoundError:
            print("File data.json tidak ditemukan. Pastikan file ada di direktori yang sama.")
            break  # Keluar dari loop jika file tidak ditemukan

        print(f"Jumlah akun  : {len(auth_datas)}")

        for index, auth_data in enumerate(auth_datas, start=1):
            # Periksa apakah auth_data adalah string atau dictionary
            if isinstance(auth_data, dict):
                # Jika dictionary, ambil nilai dan nama
                auth_value = auth_data.get("value")
                auth_name = auth_data.get("name", f"auth_{index}")
            else:
                # Jika string, gunakan langsung sebagai nilai dan buat nama default
                auth_value = auth_data
                auth_name = f"auth_{index}"

            full_url = url + "auth_data=" + auth_value

            response_data = send_mining_claim_request(full_url, headers, payload)

            if response_data:
                message = response_data.get("message")
                balances = response_data.get("data", {}).get("balances", {})
                available_click = response_data.get("data", {}).get("availableClick")

                print(f"Menjalankan Akun : {auth_name}")
                print(f"Message: TAP {message}")
                print("Balances:")
                for currency, balance in balances.items():
                    print(f"  {currency} = {balance}")
                print(f"Available Clicks: {available_click}")

                # Periksa ketersediaan klik dan tampilkan pesan
                if available_click < 100:
                    print("Click kurang dari 100 ")
                    all_clicks_below_100 = True  # Tandai jika ada akun dengan klik < 100
                else:
                    print("")  # Cetak baris kosong jika klik mencukupi

        # Cooldown jika semua akun memiliki klik kurang dari 100
        if all_clicks_below_100:
            print("Semua akun memiliki Click kurang dari 100. Mulai cooldown 300 detik.")
            for remaining_time in range(300, 0, -1):
                print(f"Sisa waktu cooldown: {remaining_time} detik", end='\r')
                time.sleep(1)
            print("\r")
            all_clicks_below_100 = False  # Reset flag setelah cooldown
        else:
            print("Semua akun telah diproses. Menunggu 1 detik sebelum memulai lagi...")
            for remaining_time in range(1, 0, -1):
                print(f"Sisa waktu: {remaining_time} detik", end='\r')
                time.sleep(1)
            print("\r")

if __name__ == "__main__":
    main()