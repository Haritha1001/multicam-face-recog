import cv2
import face_recognition
import numpy as np
from datetime import datetime

def camera(id, name1, cameraID, allAvailableDBEncodings, fileNameList, attendanceTableName, DbIDs):
    video_capture = cv2.VideoCapture(cameraID)
    table=attendanceTableName
    while video_capture.isOpened():
        success, frame = video_capture.read()
        imgSmall = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        imgSmall = cv2.cvtColor(imgSmall, cv2.COLOR_BGR2RGB)
        location = face_recognition.face_locations(imgSmall)
        encodeCurrFrame = face_recognition.face_encodings(imgSmall, location)
        for i, j in zip(encodeCurrFrame, location):
            matches = face_recognition.compare_faces(allAvailableDBEncodings, i)
            faceDist = face_recognition.face_distance(allAvailableDBEncodings, i)
            matchIndex = np.argmin(faceDist)
            if matches[matchIndex]:
                exp = "[^0-9-]+"
                name = re.findall(exp, fileNameList[matchIndex].upper())[0]
                id = str(DbIDs[matchIndex])
                y1, x2, y2, x1 = j
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, name, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                markAttendance(id, name, table)
        cv2.imshow(f"{name1}-{cameraID}", frame)
        if cv2.waitKey(1) == 27:
            break
    video_capture.release()
    cv2.destroyAllWindows()
