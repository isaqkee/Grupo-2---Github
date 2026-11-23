import cv2
from pyzbar.pyzbar import decode

# Inicializa a câmera (0 é a webcam padrão)
cap = cv2.VideoCapture(0)

print("Pressione 'q' para sair.")

while True:
    # Captura frame a frame
    ret, frame = cap.read()
    if not ret:
        break

    # Decodifica QR Codes no frame
    for barcode in decode(frame):
        barcode_data = barcode.data.decode('utf-8')
        barcode_type = barcode.type
        print(f"Tipo: {barcode_type} | Dado: {barcode_data}")
        
        # Desenha um retângulo ao redor do QR Code
        (x, y, w, h) = barcode.rect
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Exibe o vídeo
    cv2.imshow('Teste de Camera/QR', frame)

    # Sai ao pressionar 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()