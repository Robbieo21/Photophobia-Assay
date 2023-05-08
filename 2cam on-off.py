import cv2
import time
import serial

cap1 = cv2.VideoCapture(1)
cap2 = cv2.VideoCapture(2)

#BGR Threholding
white_lower = (0, 65, 0)
white_upper = (255, 255, 255)

# HSV Thresholding
#white_lower = (0, 0, 245)
#white_upper = (255, 210, 255)

min_area = 2500
max_area = 20000

SerialPort = serial.Serial()
SerialPort.baudrate = 9600
SerialPort.port = 'COM6'
SerialPort.open()

object_present_in_1 = False
initial_detect_by1_time = time.time()
initial_detect_by2_time = time.time()
count = 0
initial_count = 0

prev = 0
frame_rate = 30

while True:
    time_elapsed = time.time() - prev

    if time_elapsed > 1./frame_rate:
        prev = time.time()

        ret1, frame1 = cap1.read()
        ret2, frame2 = cap2.read()

        #HSV Conversion
        #hsv1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2HSV)
        #hsv2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2HSV)

        #Leave as BGR
        hsv1 = frame1
        hsv2 = frame2

        white_mask1 = cv2.inRange(hsv1, white_lower, white_upper)
        white_mask1 = cv2.erode(white_mask1, None, iterations=2)
        white_mask1 = cv2.dilate(white_mask1, None, iterations=2)

        white_mask2 = cv2.inRange(hsv2, white_lower, white_upper)
        white_mask2 = cv2.erode(white_mask2, None, iterations=2)
        white_mask2 = cv2.dilate(white_mask2, None, iterations=2)

        contours1, _ = cv2.findContours(white_mask1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours2, _ = cv2.findContours(white_mask2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if len(contours1) > 0 and cv2.contourArea(max(contours1, key=cv2.contourArea)) > min_area and cv2.contourArea(max(contours1, key=cv2.contourArea)) < max_area:
            if not object_present_in_1:
                object_present_in_1 = True
                initial_detect_by1_time = time.time()
                count = 0
                initial_count = 1

            #qprint(cv2.contourArea(max(contours1, key=cv2.contourArea)))
            x, y, w, h = cv2.boundingRect(max(contours1, key=cv2.contourArea))
            cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)

            a = time.time() - initial_detect_by1_time
            print(f'Camera 1 Time: {a:.2f} seconds')
            if a > 30 and count == 0:
                print("30 Second threshold met by camera 1")
                SerialPort.write(bytes("1", 'utf-8'))
                count = 1

        else:
            if object_present_in_1:
                object_present_in_1 = False
                initial_detect_by2_time = time.time()
                count = 0

            b = time.time() - initial_detect_by2_time
            print(f'Camera 2 Time: {b:.2f} seconds')
            if b > 30 and count == 0:
                print("30 Second threshold met by camera 2")
                SerialPort.write(bytes("1", 'utf-8'))
                count = 1

        if len(contours2) > 0 and cv2.contourArea(max(contours2, key=cv2.contourArea)) > min_area and cv2.contourArea(max(contours2, key=cv2.contourArea)) < max_area:

            #print(cv2.contourArea(max(contours2, key=cv2.contourArea)))
            x, y, w, h = cv2.boundingRect(max(contours2, key=cv2.contourArea))
            cv2.rectangle(frame2, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.imshow("Camera 1", frame1)
        cv2.imshow("Camera 2", frame2)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

cap1.release()
cap2.release()
cv2.destroyAllWindows()
