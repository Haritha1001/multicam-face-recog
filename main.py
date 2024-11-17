import pymongo
import os
import cv2
import face_recognition
import re
import numpy as np
import mysql.connector
import time
import csv
from multiprocessing import Process
from datetime import datetime
def getID(name):
    exp = "^[0-9]*"
    for i in range(0,len(name)):
        text = name[i]
        res = re.findall(exp, text)
        b = int(res[0])
        availableID.append(b)
    return availableID
def mergesort(arr):
    if len(arr) <= 1:
        return
    left = arr[:len(arr) // 2]
    right = arr[len(arr) // 2:]
    mergesort(left)
    mergesort(right)
    i = j = k = 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            arr[k] = left[i]
            i += 1
        else:
            arr[k] = right[j]
            j += 1
        k += 1
    while i < len(left):
        arr[k] = left[i]
        i += 1
        k += 1
    while j < len(right):
        arr[k] = right[j]
        j += 1
        k += 1
def binarysearch(arr, element):
    start = 0
    end = len(arr)-1
    mid = int(start+(end-start)/2)
    while start <= end:
        if arr[mid] == element:
            return True
        elif element < arr[mid]:
            end = mid - 1
        else:
            start = mid + 1
        mid = int(start+(end-start)/2)
    return False
def encoding_extraction_from_name_CAM(n):
    available = mycol.find({"branchID":n}, {"_id": 0, "userID": 0,"branchID":0})
    nameList = []
    for i in available:
        nameList.append(list(i.keys()))
    finalList = []
    for j in nameList:
        finalList.append(str(j[0]))
    return finalList
def getNumberofCamera(n):
    query = "select camera_id from branch where branch_id=%s"
    l = []
    mycursor.execute(query,[n])
    result = mycursor.fetchall()
    for i in result:
        l.append(i[0])
    return l
def all_available_database_encodings_CAM(n):
    newListDBencoding = []
    filenamealone = encoding_extraction_from_name_CAM(n)
    available = mycol.find({"branchID":n},{"_id":0,"userID":0,"branchID":0})
    for i,j in zip(available,filenamealone):
        newListDBencoding.append(i.get(j))
    return newListDBencoding
def existingDbVal():
    dbVal = []
    available = mycol.find({}, {"userID": 1})
    for iterate in available:
        dbVal.append(iterate.get("userID"))
    mergesort(dbVal)
    return dbVal
def computeEncodings(images):
    encodedList = []
    try:
        for img in images:
            image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(image)[0]
            encodedList.append(encode)
    except IndexError as e:
        print(e)
        sys.exit(1)
    return encodedList
def convert_to_lofd(l):
    newList = []
    existing = keyID
    count = 0
    for key in l.keys():
        if binarysearch(existingDB,existing[count]) == False:
            aNewDict = {}
            aNewDict.update({"userID": keyID[count]})
            query = "select branch_id from employee where employee_id=%s"
            mycursor.execute(query,[keyID[count]])
            result = mycursor.fetchall()
            aNewDict.update({"branchID":int(result[0][0])})
            aNewDict[key] = list(encodedListKnown[count])
            newList.insert(count, aNewDict)
            count += 1
        else:
            count += 1
    return newList
def getBranchCount():
    query = "select branch_id from branch"
    mycursor.execute(query,)
    result = mycursor.fetchall()
    return result
def insertIntoDatabase(listOfDict):
    if len(listOfDict) != 0:
        mycol.insert_many(listOfDict)
    else:
        print("Empty dictionary")
def encoding_extraction_from_name():
    available = mycol.find({}, {"_id": 0, "userID": 0,"branchID":0})
    nameList = []
    for i in available:
        nameList.append(list(i.keys()))
    finalList = []
    for j in nameList:
        finalList.append(str(j[0]))
    return finalList
def all_available_database_encodings():
    newListDBencoding = []
    filenamealone = encoding_extraction_from_name()
    available = mycol.find({},{"_id":0,"userID":0})
    for i,j in zip(available,filenamealone):
        newListDBencoding.append(i.get(j))
    return newListDBencoding
def getBranchName(n):
    query = "select branch_details from branch where branch_id=%s"
    mycursor.execute(query,[n])
    result = mycursor.fetchall()
    return result[0][0]
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
def signup():
    time.sleep(2)
    video_capture = cv2.VideoCapture(2)
    i=0
    while True:
        success,frame=video_capture.read()
        if i%2==0 and i<20 :
            if i==10:
                image=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
                location = face_recognition.face_locations(image)
                if location:
                    encodings=face_recognition.face_encodings(image)[0]
                    break
                else:
                    i = 0
        elif i%2!=0 and i<20:
            pass
        else:
            break
        i=i+1
    Nl=[]
    Newid=int(input("Enter id : "))
    Checkid=existingDbVal()
    mergesort(Checkid)
    if binarysearch(Checkid,Newid)==False:
        Newname=str(input("Enter your name : "))
        branch = int(input("Enter your Branch ID : "))
        Nd={}
        Nd.update({"userID":Newid})
        Nd['branchID'] = branch
        Nd[f'{Newid}-{Newname}']=list(encodings)
        Nl.append(Nd)
        insertIntoDatabase(Nl)
    else:
        print("Entered id is already entered")
def deleteFromMongo():
    while(1):
        choice = int(input("1. CSV File\n2. ID\n3. Exit\nchoice : "))
        if choice == 1:
            while True:
                ask_path=input("Path of file: ")
                if os.path.exists(ask_path):
                    file=open(ask_path)
                    csvreader=csv.reader(file)
                    rows=[]
                    for row in csvreader:
                        rows.append(row)
                    for i in row:
                        query={"userID":int(i)}
                        mycol.delete_one(query)
                    break
                else:
                    print("path doesn't exist")
        elif choice == 2:
            id = int(input("Enter ID : "))
            query = {"userID":id}
            mycol.delete_one(query)
        elif choice == 3:
            break
        else:
            print("Enter Valid Choice!!")
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
if _name_ == "_main_":
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["project"]
    mycol = mydb["val"]
    mysqldb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        database = "aTest",
        password = "ashwin2801",
        buffered = True
    )
    mycursor = mysqldb.cursor()
    while(1):
        userchoice=int(input("\n1.Add User\n"
        "2.Remove User \n3.Exit \n Choice : "))
        if userchoice == 1:
            signup()
        elif userchoice == 2:
            deleteFromMongo()
        elif userchoice == 3:
            break
    path = "input"
    images = []
    fileNameAlone = []
    testDict = {}
    encodedListKnown = []
    availableID = []
    fileNameWithExtension = os.listdir(path)
    for i in fileNameWithExtension:
        if len(fileNameWithExtension) == 0:
            break
        curImage = cv2.imread(f'{path}/{i}')
        images.append(curImage)
        fileNameAlone.append(os.path.splitext(i)[0])
    for i in os.listdir(path):
        os.remove(f"{path}/{i}")
    keyID = getID(fileNameAlone)
    existingDB = existingDbVal()
    encodedListKnown = computeEncodings(images)
    for k, i in zip(fileNameAlone, encodedListKnown):
        testDict[k] = list(i)
    a = convert_to_lofd(testDict)
    insertIntoDatabase(a)
    noofBranch = getBranchCount()
    for i in noofBranch:
        camCount = getNumberofCamera(int(i[0]))
        allAvailableDBEncodingsCAM = all_available_database_encodings_CAM(int(i[0]))
        fileNameList = encoding_extraction_from_name_CAM(int(i[0]))
        dbIDs = getID(fileNameList)
        windowName = getBranchName(i[0])
        for j in camCount:
            p1 = Process(target=camera,args=[int(j), windowName,int(j) ,allAvailableDBEncodingsCAM, fileNameList,windowName, dbIDs]).start()
        dbIDs.clear()
