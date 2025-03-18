import cv2
import dlib
import numpy as np


# Load face detector and landmark predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")  # Download from dlib.net/files

def calculate_facial_ratios(image_path):
    try:
        # Load the image
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("Image not found or invalid format")
        
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)

        if not faces:
            print("No faces detected.")
            return

        for face in faces:
            landmarks = predictor(gray, face)

            # Key Measurements
            forehead_chin = landmarks.part(8).y - landmarks.part(27).y
            nose_chin = landmarks.part(33).y - landmarks.part(8).y
            lip_chin = landmarks.part(62).y - landmarks.part(8).y
            face_width = landmarks.part(16).x - landmarks.part(0).x
            eye_distance = landmarks.part(42).x - landmarks.part(39).x

            # Phi Ratios
            phi_ratios = {
                "Face Height/Width": forehead_chin / face_width,
                "Nose-Chin/Lip-Chin": nose_chin / lip_chin,
                "Eye Distance/Face Width": eye_distance / face_width
            }

            # Display Results
            print("\n=== Facial Analysis Report ===")
            for ratio, value in phi_ratios.items():
                deviation = abs(value - 1.618)
                status = "✔ Close to Golden Ratio" if deviation < 0.15 else "⚠ Needs Improvement"
                print(f"{ratio}: {value:.3f} - {status}")

            # Show Image
            cv2.imshow("Facial Analysis", image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

    except Exception as e:
        print(f"Error: {str(e)}")

# Run function
calculate_facial_ratios(r"C:\Users\hp\Downloads\test_face.jpg")  # Update with your image path
print(dlib.__version__)
