import cv2
import numpy as np
import re
from datetime import datetime

def markAttendance(id,name,tableName):
    a = {"BranchA":"mysqlBranchA","BranchB":"mysqlBranchB"}
    if tableName == "BranchA":
        globals()[f"{a[tableName]}db"] = mysql.connector.connect(
            host="localhost",
            user="root",
            database="aTest",
            password="ashwin2801",
            buffered=True
        )
        globals()[f"{a[tableName]}cursor"] = mysqlBranchAdb.cursor()
        query = "select distinct id from BranchA where date = curdate()"
        mysqlBranchAcursor.execute(query, )
        aa = mysqlBranchAcursor.fetchall()
        newlist = []
        for i in aa:
            newlist.append(i[0])
        if binarysearch(newlist, id) == False:
            query1 = "select branch_id,employee_id,employee_name from employee where employee_id=%s and branch_id=1"
            mysqlBranchAcursor.execute(query1, [id])
            result1 = mysqlBranchAcursor.fetchall()
            timenow = datetime.now()
            queryinside1 = "select id from BranchA where id=%s and date=%s and branch_id=1;"
            mysqlBranchAcursor.execute(queryinside1, [result1[0][1],timenow.strftime("%Y-%m/%d")])
            if (len(mysqlBranchAcursor.fetchall()) != 1):
                queryinside11 = "insert into BranchA(branch_id,id,name,date,time) values(%s,%s,%s,%s,%s);"

                mysqlBranchAcursor.execute(queryinside11, [result1[0][0], result1[0][1], result1[0][2],timenow.strftime("%Y-%m/%d"),timenow.strftime("%H:%M:%S")])
                mysqlBranchAdb.commit()
    elif tableName == "BranchB":
        globals()[f"{a[tableName]}db"] = mysql.connector.connect(
            host="localhost",
            user="root",
            database="aTest",
            password="ashwin2801",
            buffered=True
        )
        globals()[f"{a[tableName]}cursor"] = mysqlBranchBdb.cursor()
        query = "select distinct id from BranchB where date = curdate()"
        mysqlBranchBcursor.execute(query, )
        aa = mysqlBranchBcursor.fetchall()
        newlist = []
        for i in aa:
            newlist.append(i[0])
        if binarysearch(newlist, id) == False:
            query1 = "select branch_id,employee_id,employee_name from employee where employee_id=%s and branch_id=2"
            mysqlBranchBcursor.execute(query1, [id])
            result2 = mysqlBranchBcursor.fetchall()
            queryinside2 = "select id from BranchB where id=%s and date=%s and branch_id=2;"
            timenow = datetime.now()
            mysqlBranchBcursor.execute(queryinside2, [result2[0][1],timenow.strftime("%Y-%m-%d")])
            if (len(mysqlBranchBcursor.fetchall()) != 1):
                queryinside22 = "insert into BranchB(branch_id,id,name,date,time) values(%s,%s,%s,%s,%s);"
                mysqlBranchBcursor.execute(queryinside22, [result2[0][0], result2[0][1], result2[0][2], timenow.strftime("%Y-%m-%d"),
                                                          timenow.strftime("%H:%M:%S")])
                mysqlBranchBdb.commit()
              

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
