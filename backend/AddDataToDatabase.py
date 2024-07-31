import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://attendanceprojectfinal-default-rtdb.firebaseio.com/"
})

ref = db.reference('Students')

data = {
    "6732":
        {
            "name": "Poojith",
            "major": "CSD",
            "total_attendance": 7,
            "year": 3,
            "standing": "B",
            "starting_year": 2021,
            "last_attendance_time": "2024-6-6 00:54:34"
            
        },
    "6740":
        {
            "name": "Naga Sai",
            "major": "CSD",
            "total_attendance": 12,
            "year": 3,
            "standing": "B",
            "starting_year": 2021,
            "last_attendance_time": "2024-6-6 00:54:34"
            
        },
    "6752":
        {
            "name": "Uday",
            "major": "CSD",
            "total_attendance": 7,
            "year": 3,
            "standing": "B",
            "starting_year": 2021,
            "last_attendance_time": "2024-6-6 00:54:34"
            
        }
}

for key, value in data.items():
    ref.child(key).set(value)