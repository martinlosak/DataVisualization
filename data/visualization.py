import csv
import json


# nacita vsetky europske letiska a ulozi do dictionary id:city
def load_eu_airports():
    # Slovakia and neighbours
    country_set = {'Slovakia', 'Czech Republic', 'Austria', 'Poland', 'Hungary', 'Ukraine'}
    # Slovakia and neighbours + West
    # country_set = {'Slovakia', 'Czech Republic', 'Austria', 'Poland', 'Hungary', 'Ukraine', 'Germany', 'Switzerland',
    #                'United Kingdom', 'Italy'}
    eu_airports_id = {}
    with open('airports.csv', 'r', encoding='utf8') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            if 'Europe' in row['tz'] and row['iata']:
                if row['country'] in country_set:
                    # eu_airports_id[row['id']] = row["city"]
                    eu_airports_id.setdefault(row['id'], [row["city"], row["country"]])
    print(eu_airports_id)
    print('EU Airports [id:city]: ' + str(len(eu_airports_id)))
    return eu_airports_id


# vezme dictionary europskych letisk id:city a namapuje lety do tvaru source_id,dest_id
def load_routes(airports):
    i = 0
    with open('routes.csv', 'r', encoding='utf8') as csvfile:
        routes = csv.DictReader(csvfile)

        with open('routes_new.csv', 'w', encoding='utf8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['source_city', 'source_country', 'dest_city', 'dest_country'])  # write header

            # pre vsetky lety
            for row in routes:
                # ak existuju ich letiska, vypis ich do routes_new
                if row['source_id'] in airports and row['dest_id'] in airports:
                    writer.writerow(
                        [airports[row['source_id']][0], airports[row['source_id']][1],
                         airports[row['dest_id']][0], airports[row['dest_id']][1]])
                    i += 1
    print('EU Routes [source_city, source_country, dest_city, dest_country]: ' + str(i))


def create_json():
    unique_list = {}
    with open('routes_new.csv', 'r', encoding='utf8') as f:
        routes = csv.DictReader(f)

        # pre vsetky lety
        for row in routes:
            # ak sa odletove letisko nenachadza este v liste
            if row['source_city'] not in unique_list:
                # vytvor strukturu letisko:[priletove_letiska,...]
                unique_list.setdefault(row['source_city'], []).append(row['dest_city'])
            # ak sa uz nachadza
            else:
                # skontroluj ci prilet letisko je uz v [priletove_letiska,...]
                for source_airport, destination_airports in unique_list.items():
                    if row['source_city'] == source_airport and row['dest_city'] not in destination_airports:
                        unique_list.setdefault(row['source_city'], []).append(row['dest_city'])

    with open('unique_routes_neigh.json', 'w', encoding='utf8', newline='') as f:
        json.dump(unique_list, f, indent=4)
    print('EU Unique routes [source_city:[dest_city,dest_city,..]]: ' + str(len(unique_list)))

a = load_eu_airports()
load_routes(a)
create_json()
