import cv2
import face_recognition

def compute_encodings(images):
    encoded_list = []
    try:
        for img in images:
            image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(image)[0]
            encoded_list.append(encode)
    except IndexError as e:
        print(e)
        sys.exit(1)
    return encoded_list
