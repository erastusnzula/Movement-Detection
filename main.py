import os
import winsound
import cv2

camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)

frame_one = None


def capture_image():
    global frame_one
    while camera.isOpened():
        _, frame_one = camera.read()
        _, frame_two = camera.read()
        frame_difference = cv2.absdiff(frame_one, frame_two)
        gray_scale = cv2.cvtColor(frame_difference, cv2.COLOR_RGB2GRAY)
        blurred_image = cv2.GaussianBlur(gray_scale, (5, 5), 0)
        _, image_thresh = cv2.threshold(blurred_image, 20, 255, cv2.THRESH_BINARY)
        image_dilated = cv2.dilate(image_thresh, None, iterations=3)
        contours, _ = cv2.findContours(image_dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            if cv2.contourArea(contour) > 2000:
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(frame_one, (x, y), (x + w, y + h), (255, 0, 0), 2)
                print("Movement detected.")
                winsound.PlaySound('alert.wav', winsound.SND_ASYNC)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

        elif key == ord('c'):
            save_image_capture()

        cv2.imshow('Press c to capture an image.', frame_one)


def save_image_capture():
    global frame_one
    os.makedirs('images', exist_ok=True)
    name = 'Image1.png'
    if name in os.listdir('images'):
        name = f"{os.path.splitext(name)[0][:-1]}{len(os.listdir('images')) + 1}" \
               f"{os.path.splitext(name)[1]}"
    cv2.imwrite(os.path.join('images', name), frame_one)
    print(f"{name} captured successfully.")


capture_image()
