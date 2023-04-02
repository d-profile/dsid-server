# Digital Student Identity

## Run app 

```sh
python3 -m virtualenv env
source env/bin/activate
pip install -r requirements.txt
python3 main.py
```

Endpoint: http://localhost:8000
Swagger doc: http://localhost:8000/docs

## Business flow

Create Student (school) -> Get Students (school) -> Submit (student) -> Update (student) -> Verify (school) -> Get Student (student) -> Update (student)

1. Admin Web click create students (import csv file) (/school/create-students)
2. Mobile app register (/student/submit)
3. Mobile app view (/student/student)
4. Admin web verify (/school/verify)
4. Admin web view (/school/students)