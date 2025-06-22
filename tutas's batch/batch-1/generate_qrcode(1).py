import qrcode

# Data yang ingin dimasukkan ke dalam QR
data = ""

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
img.save("qrcode_mnf.png")
