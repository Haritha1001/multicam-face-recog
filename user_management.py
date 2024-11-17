import time
import cv2
import face_recognition
import os
import csv
from modules.database_operations import existingDbVal, insertIntoDatabase

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
