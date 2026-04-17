import cv2
import numpy as np

def capture_iris():
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not cap.isOpened():
        print("Erro: não foi possível acessar a câmera.")
        return None, None

    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

    print("📸 Coloque o olho na câmera e pressione 'q' para capturar...")
    iris_code = None
    features = None

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Erro ao capturar frame da câmera.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        eyes = eye_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in eyes:
            roi = frame[y:y+h, x:x+w]
            roi_gray = gray[y:y+h, x:x+w]

            # Cor predominante (HSV canal H)
            hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
            avg_color = int(np.mean(hsv[:,:,0])) % 100

            # Textura (média de intensidade)
            textura = int(np.mean(roi_gray)) % 100

            # Proporção largura/altura
            proporcao = int((w/h) * 10) % 100

            # Intensidade média geral
            intensidade = int(np.mean(gray)) % 100

            # Código de 4 dígitos
            iris_code = f"{avg_color%10}{textura%10}{proporcao%10}{intensidade%10}"

            # Features = histograma simplificado
            features = cv2.calcHist([roi_gray],[0],None,[16],[0,256]).flatten()

            # Desenha círculo verde fino
            cx, cy = x + w//2, y + h//2
            radius = max(w,h)//2
            cv2.circle(frame, (cx, cy), radius, (0,255,0), 1)

        cv2.imshow("Scanner de Olho", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return iris_code, features
