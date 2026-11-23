import qrcode
from PIL import Image, ImageFilter

def generate_samples():
    data = "QR-SMART40-2026-001-A"
    qr = qrcode.QRCode(box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)

    img_ok = qr.make_image(fill_color="black", back_color="white").convert("RGB")
    img_ok.save("qr_sample_ok.png")

    # Desfoque leve (legível, mas com nitidez < 80%)
    img_nok = img_ok.filter(ImageFilter.GaussianBlur(radius=1.8))
    img_nok.save("qr_sample_nok.png")

    print("[OK] Amostras atualizadas!")

if __name__ == "__main__":
    generate_samples()
