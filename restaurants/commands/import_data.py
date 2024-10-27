from django.core.management.base import BaseCommand
import csv
from restaurants.models import Restaurant
from django.db import transaction

class Command(BaseCommand):
    help = 'Import restaurants data from CSV file'

    def handle(self, *args, **kwargs):
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
                        self.stdout.write(
                            self.style.SUCCESS(f"Sukses: {row['Nama Tempat Makan']}")
                        )
                    except Exception as e:
                        self.stdout.write(
                            self.style.ERROR(f"Error {row['Nama Tempat Makan']}: {str(e)}")
                        )
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Import selesai. Total restaurants: {Restaurant.objects.count()}"
                    )
                )