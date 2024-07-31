from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import cv2
import face_recognition
import pickle
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, db, storage

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://attendanceprojectfinal-default-rtdb.firebaseio.com/",
    'storageBucket': "attendanceprojectfinal.appspot.com"
})

bucket = storage.bucket()

# Load known encodings
with open('EncodeFile.p', 'rb') as file:
    encodeListKnownWithIds = pickle.load(file)
    encodeListKnown, studentIds = encodeListKnownWithIds

@app.route('/detect', methods=['POST'])
def detect():
    
        file = request.get_data()
        print(f"Received file data of length: {len(file)}")  # Debug print

        if not file:
            print("No image data received")  # Debug print
            return jsonify({"error": "No image data received"}), 400

        npimg = np.frombuffer(file, np.uint8)
        img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

        if img is None or img.size == 0:
            print("Failed to decode image")  # Debug print
            return jsonify({"error": "Failed to decode image"}), 400

        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        faceCurFrame = face_recognition.face_locations(imgS)
        encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

        if faceCurFrame:
            for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
                matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
                faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
                matchIndex = np.argmin(faceDis)
                if matches[matchIndex]:
                    id = studentIds[matchIndex]
                    studentInfo = db.reference(f'Students/{id}').get()
                    blob = bucket.get_blob(f'Images/{id}.png')
                    storedImage = blob.generate_signed_url(datetime.timedelta(seconds=300), method='GET')
                    studentInfo['storedImage'] = storedImage
                    return jsonify(studentInfo)
        
        print("Student not found")  # Debug print
        return jsonify({"error": "Student not found"})
    # except Exception as e:
    #     print(f"Error occurred: {e}")  # Debug print
    #     return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
