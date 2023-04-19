import cv2
import time
import serial

cap1 = cv2.VideoCapture(1)
cap2 = cv2.VideoCapture(2)

white_lower = (0, 0, 225)
white_upper = (100, 15, 255)
min_area = 750

SerialPort = serial.Serial()
SerialPort.baudrate = 9600
SerialPort.port = 'COM6'
SerialPort.open()

object_present_in_1 = False
initial_detect_by1_time = time.time()
initial_detect_by2_time = time.time()
#LED_state = False
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

        frame1 = cv2.flip(frame1, 1)
        frame2 = cv2.flip(frame2, 1)
        hsv1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2HSV)
        hsv2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2HSV)

        white_mask1 = cv2.inRange(hsv1, white_lower, white_upper)
        white_mask1 = cv2.erode(white_mask1, None, iterations=2)
        white_mask1 = cv2.dilate(white_mask1, None, iterations=2)

        white_mask2 = cv2.inRange(hsv2, white_lower, white_upper)
        white_mask2 = cv2.erode(white_mask2, None, iterations=2)
        white_mask2 = cv2.dilate(white_mask2, None, iterations=2)

        contours1, _ = cv2.findContours(white_mask1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours2, _ = cv2.findContours(white_mask2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if len(contours1) > 0 and cv2.contourArea(max(contours1, key=cv2.contourArea)) > min_area:
            if not object_present_in_1:
                object_present_in_1 = True
                initial_detect_by1_time = time.time()
                count = 0
                initial_count = 1
                #object_detected_time = time.time()
                #if object_not_detected_time != 0:
                   # y = time.time() - object_not_detected_time
                   # print(f"Object detected by Camera 2 for {y:.2f} seconds")
                   # object_not_detected_time = 0
                   # if y > 10:
                        #SerialPort.write(bytes("1", 'utf-8'))
                        #LED_state = False

            x, y, w, h = cv2.boundingRect(max(contours1, key=cv2.contourArea))
            cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)

            #if count1 == 0:
                #object_not_detected_time = time.time()
                #count1 = 1

            a = time.time() - initial_detect_by1_time
            print(f'Camera 1 Time: {a:.2f} seconds')
            if a > 10 and count == 0:
                print("10 Second threshold met by camera 1")
                SerialPort.write(bytes("2", 'utf-8'))
                count = 1
                #object_not_detected_time = 0

        else:
            if object_present_in_1:
                object_present_in_1 = False
                initial_detect_by2_time = time.time()
                count = 0
                #if object_detected_time != 0:
                    #x = time.time() - object_detected_time
                    #print(f"Object detected by Camera 1 for {x:.2f} seconds")
                    #object_detected_time = 0
                    #if x > 10:
                        #SerialPort.write(bytes("2", 'utf-8'))
                        #LED_state = False

            #if count2 == 0:
                #object_detected_time = time.time()
                #count2 = 1

            b = time.time() - initial_detect_by2_time
            print(f'Camera 2 Time: {b:.2f} seconds')
            if b > 10 and count == 0 and initial_count != 0:
                print("10 Second threshold met by camera 2")
                SerialPort.write(bytes("1", 'utf-8'))
                count = 1
                #object_detected_time = 0

        if len(contours2) > 0 and cv2.contourArea(max(contours2, key=cv2.contourArea)) > min_area:
            #if not object_present:
                #object_present = True
                #object_detected_time = time.time()
                #if object_not_detected_time is not None:
                    #print(f"Object not detected by Camera 1 for {time.time() - object_not_detected_time:.2f} seconds")
                    #object_not_detected_time = None

            x, y, w, h = cv2.boundingRect(max(contours2, key=cv2.contourArea))
            cv2.rectangle(frame2, (x, y), (x + w, y + h), (0, 255, 0), 2)
            #if not LED_state:
             #   SerialPort.write(bytes("2", 'utf-8'))
             #   LED_state = True

        #else:
            #if object_present:
                #object_present = False
                #object_not_detected_time = time.time()
                #if object_detected_time is not None:
                    #print(f"Object detected by Camera 1 for {time.time() - object_detected_time:.2f} seconds")
                    #object_detected_time = None

        cv2.imshow("Camera 1", frame1)
        cv2.imshow("Camera 2", frame2)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

cap1.release()
cap2.release()
cv2.destroyAllWindows()
