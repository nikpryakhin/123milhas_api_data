import requests
import csv
from datetime import date


def collect_data():
    count = 0
    page_number = 1
    city_count = 0
    today_date = str(date.today())

    voo_promo_arrival_city = []
    voo_promo_arrival_city_departure_city = []

    # list of arrival cities
    while True:

        # Handle the number of pages
        for page in range(page_number, page_number + 1):

            url = f'https://promo123.123milhas.com/api/external/products/category/voo-promo?page={page}&pageSize=36&order=menu_order'
            response = requests.get(url=url)

            page_number += 1

            data = response.json()
            items = data.get('data')

            for i in items:
                arrival_city = i.get('title').lower()[10:-17].replace(' ', '-')
                voo_promo_arrival_city.append(arrival_city)


        # show number of pages
        count += 1
        print(f'Page #{count}, number of arrival cities: {len(voo_promo_arrival_city)}')
        print(url)

        if len(items) < 36:
            break

    # for each city of arrival, we extract all data about the cities of departure
    for city in voo_promo_arrival_city:
        url = f'https://promo123.123milhas.com/api/external/products/voos-para-{city}-passagem-aerea'
        response = requests.get(url=url)

        data = response.json()
        pricings = data.get('pricings')

        # each city has its own data in json format
        for i in pricings:
            id = i.get('id')
            price = i.get('price')
            old_price = i.get('old_price'),
            departure_city = i['available_origin'].get('origin'),
            period_name = i['available_period'].get('period_name'),
            period_number = i['available_period'].get('initial_date')[:7]
            link_arrival_city = f'https://123milhas.com/promo123/produto/voos-para-{city}-passagem-aerea'

            voo_promo_arrival_city_departure_city.append(
                {
                    'id': id,
                    'price': price,
                    'old_price': old_price[0],
                    'departure_city': departure_city[0],
                    'arrival_city': city,
                    'period_name': period_name[0],
                    'period_number': period_number,
                    'link_arrival_city': link_arrival_city,
                    'parse_date': today_date
                }
            )

        # data storage process
        city_count +=1
        print(f'{city_count}/{len(voo_promo_arrival_city)} finished, {city}')


    # csv header
    fieldnames = ['id', 'price', 'old_price', 'departure_city', 'arrival_city', 'period_name', 'period_number', 'link_arrival_city', 'parse_date']

    # save file in csv format
    with open(f'{today_date}_voo_promo_data.csv', 'w', encoding="utf-8", newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(voo_promo_arrival_city_departure_city)


def main():
    collect_data()


if __name__ == '__main__':
    main()
