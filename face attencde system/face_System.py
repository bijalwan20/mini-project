import pymongo
from datetime import datetime
import streamlit as st
import pickle
import face_recognition
import numpy as np
import cv2

if __name__=="__main__":
    

    
    st.title("Face Recognition Based Attendence System")
    col1,col2=st.columns(2)

    now = datetime.now()
    current_date=now.strftime("%Y-%m-%d")
    
    #DB Create
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db=client['student']
    collection=db['names']


    all=collection.find()
    pp_face_encoding=[]
    namelist=[]
    present={'Name':[],'Time':[]}
    ll=0
    for i in all:
        ll+=1
        if current_date not in i:
            collection.update_one({"name":i['name']},{"$set":{current_date:'A'}})
            st.experimental_rerun()
        

        if i[current_date] =='P':
            current_time=now.strftime("%H hr-%M min")
            present['Name'].append(i['name'])
            present['Time'].append(current_time)

        namelist.append(i['name'])
        pp_face_encoding.append(np.asarray(i['encoding'],dtype=np.float64))

    col1.write("Total number of student in our databse: "+str(ll))
    col1.dataframe(present,1000)

    selected_mode = col2.selectbox(
    	"Select a mode",['Mark Your Attendence','Create New User']
	)

    if selected_mode=='Create New User':
        username=col2.text_input("Enter Your Name")
        userpassword=col2.text_input("Enter Your password")
        pic1=col2.camera_input("Take a pictue")
        if pic1 is not None:
            b=pic1.getvalue()
            cimg=cv2.imdecode(np.frombuffer(b,np.uint8),cv2.IMREAD_COLOR)
            face_location=face_recognition.face_locations(cimg)
            face_encodings=face_recognition.face_encodings(cimg,face_location)
            
            if col2.button("Create User"):
                for face_encoding in face_encodings:
                    collection.insert_one({'name':username,'password':userpassword,'encoding':face_encoding.tolist(),current_date:'A'})
                st.balloons()
                st.warning("User is created !")


    if selected_mode=='Mark Your Attendence':
        pic=col2.camera_input("Take a pictue")
        if pic is not None:
            b=pic.getvalue()
            cimg=cv2.imdecode(np.frombuffer(b,np.uint8),cv2.IMREAD_COLOR)
            face_location=face_recognition.face_locations(cimg)
            face_encodings=face_recognition.face_encodings(cimg,face_location)
            name=""
            flag=False
            for face_encoding in face_encodings:
                matches=face_recognition.compare_faces(pp_face_encoding,face_encoding)
                face_distance=face_recognition.face_distance(pp_face_encoding,face_encoding)
                best_match_index=np.argmin(face_distance)
                print(best_match_index)
                if matches[best_match_index]:
                    name=namelist[best_match_index]
                    flag=True

                print(name)

            if flag:
                collection.update_one({"name":name},{"$set":{current_date:'P'}})
                st.balloons()
                st.warning("Attendence marked")
        
        
