import os
import django
import uuid
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jogja_rasa.settings')  
django.setup()

from restaurants.models import Restaurant

def find_invalid_uuids():
    invalid_uuids = []
    with connection.cursor() as cursor:
        cursor.execute("SELECT id FROM restaurants_restaurant")
        rows = cursor.fetchall()
        for row in rows:
            try:
                uuid.UUID(str(row[0]))
            except ValueError:
                print(f"Invalid UUID found: {row[0]}")
                invalid_uuids.append(row[0])
    return invalid_uuids

def delete_invalid_uuids(invalid_uuids):
    with connection.cursor() as cursor:
        for invalid_uuid in invalid_uuids:
            cursor.execute("DELETE FROM restaurants_restaurant WHERE id = %s", [invalid_uuid])
            print(f"Deleted restaurant with invalid UUID: {invalid_uuid}")

if __name__ == "__main__":
    invalid_uuids = find_invalid_uuids()
    delete_invalid_uuids(invalid_uuids)