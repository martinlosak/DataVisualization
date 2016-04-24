import csv
import json


# nacita vsetky europske letiska a ulozi do dictionary id:city
def load_eu_airports():
    eu_airports_id = {}
    with open('airports.csv', 'r', encoding='utf8') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            if 'Europe' in row['tz'] and row['iata']:
                eu_airports_id[row['id']] = row["city"]

    print('EU Airports [id:city]: ' + str(len(eu_airports_id)))
    return eu_airports_id


# vezme dictionary europskych letisk id:city a namapuje lety do tvaru source_id,dest_id
def load_routes(airports):
    i = 0
    with open('routes.csv', 'r', encoding='utf8') as csvfile:
        reader = csv.DictReader(csvfile)

        with open('routes_new.csv', 'w', encoding='utf8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['source', 'dest'])  # write header

            for row in reader:
                if row['source_id'] in airports and row['dest_id'] in airports:
                    writer.writerow([airports[row['source_id']], airports[row['dest_id']]])
                    i += 1
    print('EU Routes [source_id:dest_id]: ' + str(i))


def create_json():
    unique_list = {}
    with open('routes_new.csv', 'r', encoding='utf8') as f:
        routes = csv.DictReader(f)

        # pre vsetky lety
        for row in routes:
            # ak sa odletove letisko nenachadza este v liste
            if row['source'] not in unique_list:
                # vytvor strukturu letisko:[priletove_letiska,...]
                unique_list.setdefault(row['source'], []).append(row['dest'])
            # ak sa uz nachadza
            else:
                # skontroluj ci prilet letisko je uz v [priletove_letiska,...]
                for source_airport, destination_airports in unique_list.items():
                    if row['source'] == source_airport and row['dest'] not in destination_airports:
                        unique_list.setdefault(row['source'], []).append(row['dest'])

    with open('unique_routes.json', 'w', encoding='utf8', newline='') as f:
        json.dump(unique_list, f, indent=4)
    print('EU Unique routes [source_city:[dest_city,dest_city,..]]: ' + str(len(unique_list)))


a = load_eu_airports()
load_routes(a)
create_json()
