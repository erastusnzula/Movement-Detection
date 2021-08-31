import random
import winsound
import cv2

camera = cv2.VideoCapture(0)


def capture_image():
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
                cv2.rectangle(frame_one, (x, y), (x + w, y + h), (0, 255, 0), 2)
                print("Movement detected.")
                winsound.PlaySound('alert.wav', winsound.SND_ASYNC)

        key = cv2.waitKey(1)
        if key == ord('q'):
            break

        elif key == ord('c'):
            image_name = f'image + {random.randint(0, 1000)}.png'
            cv2.imwrite(image_name, frame_one)
            camera.release()

        cv2.imshow('Press c to capture an image.', frame_one)


capture_image()
