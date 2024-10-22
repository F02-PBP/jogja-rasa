import csv
from restaurants.models import Restaurant
from django.db import transaction

def run():
    csv_file_path = 'data.csv'
    
    with transaction.atomic():
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    Restaurant.objects.create(
                        name=row['Nama Tempat Makan'],
                        longitude=float(row['Longitude']) if row['Longitude'] else 0,
                        latitude=float(row['Latitude']) if row['Latitude'] else 0,
                        description=row['Deskripsi Resto']
                    )
                    print(f"Sukses: {row['Nama Tempat Makan']}")
                except Exception as e:
                    print(f"Error {row['Nama Tempat Makan']}: {str(e)}")

    print(f"Import selesai. Total restaurants: {Restaurant.objects.count()}")