import csv
from disdata.models import Pincode
from django.contrib.gis.geos import Point

Pincode.objects.all().delete()
CSV_PATH = 'IN.csv'
with open(CSV_PATH, newline='') as csvfile:
    spamreader = csv.reader(csvfile)
    next(spamreader)
    set_of_pin=set()
    for row in spamreader:
        # print(row)
        # break
        if row[1] not in set_of_pin:
            set_of_pin.add(row[1])
            Pincode.objects.create(pincode=row[1],area=row[2][:40],state=row[3][:40],state_code=int(row[4]),province=row[5][:40],province2=row[6][:40],accuracy=int(row[9]),located_at=Point(float(row[8]),float(row[7])))
