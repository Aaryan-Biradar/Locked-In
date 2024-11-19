import cv2  # Import the OpenCV library for image and video processing
import time  # Import the time module to track the elapsed time
from mouse_and_keyboard import *
from attention_grabber import main as animation

def main():
    # Initialize the webcam capture (0 refers to the default webcam)
    capture = cv2.VideoCapture(0)

    # Load the pre-trained Haar Cascade classifier for face detection
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Load the pre-trained Haar Cascade classifier for eye detection
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')


    # Variables to track the time since the last detections
    last_face_time = time.time()  # Time since the last face was detected
    last_eye_time = time.time()   # Time since the last eyes were detected
    error_count = 0                # Counter for the error messages
    timeout = 5                   # Time limit for inactivity in seconds


    while True:
        # Capture frame by frame, at 1 frame per second
        #time.sleep(1)  # Introduce a delay to limit the frame rate to 1 frame per second                                                                           



        # Capture each frame from the webcam
        ret, frame = capture.read()  # 'ret' is a boolean indicating success, 'frame' is the captured image

        # Convert the frame to grayscale (Haar cascades work better on grayscale images)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the grayscale image using the face cascade classifier
        # Parameters: (input image, scale factor, minimum neighbors for detection)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)



        # Check if any faces are detected
        if len(faces) > 0:
            # If a face is detected, update the last_face_time to the current time
            last_face_time = time.time()


        # Loop over all the detected faces
        for (x, y, w, h) in faces:
            # Draw a rectangle around each face in the original (colored) frame
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)  # Blue rectangle for the face
            

            # Define regions of interest (ROI) for both grayscale and colored frames (used for eye detection)
            roi_gray = gray[y:y+w, x:x+w]  # Grayscale ROI for detecting eyes
            roi_color = frame[y:y+h, x:x+w]  # Colored ROI for displaying the rectangles

            # Detect eyes within the face region (ROI) using the eye cascade classifier
            eyes = eye_cascade.detectMultiScale(roi_gray, 1.3, 5)

            # Check if any eyes are detected
            if len(eyes) > 0:
                last_eye_time = time.time()  # Update time if eyes are detected

            # Loop over all detected eyes
            for (ex, ey, ew, eh) in eyes:
                # Draw a rectangle around each eye within the face region
                cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)  # Green rectangle for the eyes

        # Check for inactivity in input (mouse and keyboard) and timeouts
        if is_input_active() == False:  # Function from test.py
            print("Input inactivity detected.")  # No input from devices

        # Calculate the time elapsed since a face and eyes were last detected
        elapsed_face_time = time.time() - last_face_time
        elapsed_eye_time = time.time() - last_eye_time

        print(f"Elapsed face time: {elapsed_face_time:.2f}, Elapsed eye time: {elapsed_eye_time:.2f}, Input active: {is_input_active()}")

        
        # If 30 seconds have passed without detecting a face, print an error message
        if (elapsed_face_time > timeout) and (elapsed_eye_time > timeout) and (is_input_active() == False):
            error_count += 1
            print(f"Error: Lock back in {error_count}")
            animation()  # Only call the animation here
        else:
            print("No error condition met.")


        # Display the video stream with the detected faces and eyes
        cv2.imshow('Anti Reel Machine', frame)

        # Break the loop if the 'q' key is pressed
        if cv2.waitKey(1) == ord('q'):
            break

    # Release the webcam when done
    capture.release()

    # Close all OpenCV windows
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()