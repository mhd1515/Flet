
import socket
import qrcode

# پیدا کردن IP کامپیوتر در شبکه
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
finally:
    s.close()

# آدرس ماشین حساب
url = f"http://{ip}:8550"

# ساخت QR Code
qr = qrcode.make(url)
qr.save("calculator_qr.png")

print("آدرس ماشین حساب:", url)
print("QR Code در فایل calculator_qr.png ذخیره شد.")
