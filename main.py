import os
import time
from pywhatsapp import WhatsApp
from qrcode import QRCode
import cv2  # Untuk handle gambar profil grup

# CONFIGURASI
TARGET_MEMBERS = ["6287864310700@c.us"]
BASE_GROUP_NAME = "Grup"
DELAY_BETWEEN_GROUPS = 5  # dalam detik
GROUP_PROFILE_PICTURE = "group_profile.jpg"  # Pastikan file ada di direktori yang sama

def display_qr(qr_data):
    qr = QRCode()
    qr.add_data(qr_data)
    qr.print_ascii(invert=True)

def create_multiple_groups(client, count):
    for i in range(1, count + 1):
        try:
            group_name = f"{BASE_GROUP_NAME} {i}"
            print(f"\n📌 Membuat {group_name}...")
            
            # 1. Buat grup
            group_id = client.create_group(group_name, TARGET_MEMBERS)
            print(f"✅ Grup {group_name} berhasil dibuat")
            
            # 2. Set profil grup jika file ada
            if os.path.exists(GROUP_PROFILE_PICTURE):
                try:
                    client.set_group_picture(group_id, GROUP_PROFILE_PICTURE)
                    print("🖼️ Foto profil grup berhasil diubah")
                except Exception as e:
                    print(f"⚠️ Gagal mengubah foto profil: {str(e)}")
            
            # Delay antara pembuatan grup
            if i < count:
                time.sleep(DELAY_BETWEEN_GROUPS)
                
        except Exception as e:
            print(f"❌ Error saat membuat grup: {str(e)}")

def main():
    # Inisialisasi client WhatsApp
    client = WhatsApp(
        auth_method="local",  # Simpan session lokal
        headless=True,       # Mode tanpa GUI
        qr_callback=display_qr
    )
    
    print("Menunggu QR scan...")
    client.wait_for_login()
    
    print("\nBot siap!")
    try:
        count = int(input("Berapa banyak grup yang ingin dibuat? "))
        if count <= 0:
            print("Input invalid. Harap masukkan angka positif.")
            return
            
        create_multiple_groups(client, count)
        
    except ValueError:
        print("Input harus berupa angka!")
    finally:
        client.close()

if __name__ == "__main__":
    main()
