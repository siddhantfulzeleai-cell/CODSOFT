import cv2
from deepface import DeepFace

# Load the database of known faces (a folder containing 'name.jpg' files)
db_path = "path/to/your/faces_database"

# Initialize Video Stream
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret: break

    try:
        # 1. Detection & Recognition in one call
        # We specify 'retinaface' for detection and 'ArcFace' for recognition
        results = DeepFace.find(img_path=frame, 
                                db_path=db_path, 
                                detector_backend='retinaface', 
                                model_name='ArcFace',
                                enforce_detection=False)

        if len(results) > 0:
            for res in results:
                # Extract coordinates and identity
                # Note: DeepFace returns a list of DataFrames
                df = res
                if not df.empty:
                    name = df.iloc[0]['identity'].split('/')[-1].split('.')[0]
                    x, y, w, h = df.iloc[0]['source_x'], df.iloc[0]['source_y'], \
                                 df.iloc[0]['source_w'], df.iloc[0]['source_h']
                    
                    # Draw Bounding Box and Name
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cv2.putText(frame, name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)

    except Exception as e:
        print(f"Error: {e}")

    cv2.imshow('Face Recognition App', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()