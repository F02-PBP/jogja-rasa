import pandas as pd
from restaurants.models import Restaurant

def run():
    csv_file_path = 'data.csv'
    data = pd.read_csv(csv_file_path)

    for index, row in data.iterrows():
        restaurant = Restaurant.objects.create(
            name=row['Nama Tempat Makan'],
            longitude=row['Longitude'],
            latitude=row['Latitude'],
            description=row['Deskripsi Resto'],
        )
        restaurant.save()

    print('SEMOGA BISAAA')
