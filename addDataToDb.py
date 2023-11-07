import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey.json")
# initializong rtdb url for connection 
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://facerec-cec69-default-rtdb.firebaseio.com/"
})

# it will create directory in firebase rt db
ref = db.reference('students')
data = {
    "456765":{
        "name": "Arpit Sharma",
        "major": "Robotics L",
        "starting_year": 2015,
        "total_attendance": 8,
        "standings": "G",
        "year": 4,
        "last_attendance_time": "2023-11-11 00:54:34"
    },
    "567299":{
        "name":"Rahul Singh",
        "major": "Robotics A",
        "starting_year": 2016,
        "total_attendance": 2,
        "standings": "B",
        "year": 3,
        "last_attendance_time": "2023-11-11 00:52:34"
    },
    "973475":{
        "name":"Karan Gupta",
        "major": "Robotics",
        "starting_year": 2017,
        "total_attendance": 4,
        "standings": "O",
        "year": 2,
        "last_attendance_time": "2023-11-11 00:51:34"
    }
}

for key,value in data.items():
    ref.child(key).set(value)