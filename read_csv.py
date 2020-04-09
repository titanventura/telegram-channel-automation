import csv
from tqdm import tqdm
from base_app.models import UserRecord

input_file = csv.DictReader(open("test.csv"))
records = list(input_file)
for record in tqdm(records):
    try:
        UserRecord.objects.create(name=record['name'],phone=record['phone'],email=record['email'],rollno=record['rollno'])
    except Exception as e:
        print(e)