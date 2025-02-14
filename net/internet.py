import cv2
from pyzbar import pyzbar

def decode_qr_code(frame):
    # Decodificar los códigos QR en la imagen
    barcodes = pyzbar.decode(frame)
    for barcode in barcodes:
        # Extraer los datos del código QR
        barcode_data = barcode.data.decode("utf-8")
        barcode_type = barcode.type
        print(f"Tipo: {barcode_type}, Datos: {barcode_data}")

        # Si el código QR es de una red Wi-Fi, extraer SSID y contraseña
        if barcode_data.startswith("WIFI:"):
            wifi_info = barcode_data.split(";")
            ssid = None
            password = None
            for info in wifi_info:
                if info.startswith("S:"):
                    ssid = info[2:]
                elif info.startswith("P:"):
                    password = info[2:]
            if ssid and password:
                print(f"SSID: {ssid}, Contraseña: {password}")
            else:
                print("No se pudo extraer la información de la red Wi-Fi.")

def main():
    # Iniciar la cámara
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("No se pudo abrir la cámara.")
        return

    while True:
        # Capturar frame por frame
        ret, frame = cap.read()

        if not ret:
            print("No se pudo capturar el frame.")
            break

        # Decodificar el código QR
        decode_qr_code(frame)

        # Mostrar el frame en una ventana
        cv2.imshow("QR Code Scanner", frame)

        # Salir del bucle si se presiona la tecla 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Liberar la cámara y cerrar la ventana
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()