import requests
import json
from datetime import date


def collect_data():
    count = 0
    page_number = 1
    city_count = 0
    today_date = str(date.today())

    voo_promo_arrival_city = []
    voo_promo_arrival_city_departure_city = []

    while True:
        for page in range(page_number, page_number + 1):

            url = f'https://promo123.123milhas.com/api/external/products/category/voo-promo?page={page}&pageSize=36&order=menu_order'
            response = requests.get(url=url)

            page_number += 1

            data = response.json()
            items = data.get('data')

            for i in items:
                arrival_city = i.get('title').lower()[10:-17].replace(' ', '-')
                voo_promo_arrival_city.append(arrival_city)


        count += 1
        print(f'Page #{count}, number of arrival cities: {len(voo_promo_arrival_city)}')
        print(url)

        if len(items) < 36:
            break


    for city in voo_promo_arrival_city:
        url = f'https://promo123.123milhas.com/api/external/products/voos-para-{city}-passagem-aerea'
        response = requests.get(url=url)

        data = response.json()
        pricings = data.get('pricings')


        for i in pricings:
            id = i.get('id')
            price = i.get('price')
            old_price = i.get('old_price'),
            departure_city = i['available_origin'].get('origin'),
            period_name = i['available_period'].get('period_name'),
            period_number = i['available_period'].get('initial_date')[:7]

            voo_promo_arrival_city_departure_city.append(
                {
                    'id': id,
                    'price': price,
                    'old_price': old_price[0],
                    'departure_city': departure_city[0],
                    'period_name': period_name[0],
                    'period_number': period_number,
                    'arrival_city': city,
                    'date': today_date
                }
            )

        city_count +=1
        print(f'{city_count}/{len(voo_promo_arrival_city)} finished, {city}')

    with open('voo_promo_arrival_city_departure_city.json', 'w', encoding="utf-8") as file:
        json.dump(voo_promo_arrival_city_departure_city, file, indent=4, ensure_ascii=False)


def main():
    collect_data()


if __name__ == '__main__':
    main()
    

    
# for google drive purpose only

from google.colab import drive
drive.mount('/content/gdrive')

with open(f'/content/gdrive/My Drive/{date.today()}voo_promo_arrival_city_departure_city.json', 'w') as f:
  f.write('content')


# JSON converter to xml 
# https://tableconvert.com/json-to-excel
