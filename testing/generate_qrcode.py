import qrcode

# Data yang ingin dimasukkan ke dalam QR
data = "https://www.notion.so/Muhammad-Adi-Anugerah-Arrahman-1e92524a322e80e4bdfcf582ef1cd457?pvs=4"

# Membuat QR code
qr = qrcode.QRCode(
    version=1,  # ukuran QR code (1-40), semakin besar, semakin banyak data
    error_correction=qrcode.constants.ERROR_CORRECT_H,  # tingkat koreksi error
    box_size=10,  # ukuran tiap kotak (piksel)
    border=4,  # tebal border (default 4)
)

qr.add_data(data)
qr.make(fit=True)

# Membuat image QR
img = qr.make_image(fill_color="black", back_color="white")

# Simpan gambar
img.save("qrcode_example.png")
