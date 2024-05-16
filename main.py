import json
import requests
import pprint
import copy
from tabulate import tabulate

search_track_map = []
search_results = {}
const_seat_types = {
                1: {
                    "type": "AC_B",
                    "fare": "N/A",
                    "seat_counts": 0,
                },
                2: {
                    "type": "AC_S",
                    "fare": "N/A",
                    "seat_counts": 0,
                },
                3: {
                    "type": "SNIGDHA",
                    "fare": "N/A",
                    "seat_counts": 0,
                },
                4: {
                    "type": "F_BERTH",
                    "fare": "N/A",
                    "seat_counts": 0,
                },
                5: {
                    "type": "F_SEAT",
                    "fare": "N/A",
                    "seat_counts": 0,
                },
                6: {
                    "type": "F_CHAIR",
                    "fare": "N/A",
                    "seat_counts": 0,
                },
                7: {
                    "type": "S_CHAIR",
                    "fare": "N/A",
                    "seat_counts": 0,
                },
                8: {
                    "type": "SHOVAN",
                    "fare": "N/A",
                    "seat_counts": 0,
                },
            }
request_count = 0
table_headers_list = ['Station Combination']
# table_header = "Station Combination\t\t\t\t"
for seat in const_seat_types:
    # table_header += f"\t {const_seat_types[seat]['type']}"
    table_headers_list.append(const_seat_types[seat]['type'])


def getStationListByTrainCode(train_id):
    url = 'https://railspaapi.shohoz.com/v1.0/web/train-routes'
    params = {'model': train_id}
    result = requests.post(url, params)
    station_list = []
    if result.status_code == 200:
        result_json = json.loads(result.text)
        for route in result_json['data']['routes']:
            station_list.append(route['city'])
    return station_list

def getSuitableTrainList(from_city, to_city, journey_date):
    url = f"https://railspaapi.shohoz.com/v1.0/web/bookings/search-trips-v2?from_city={from_city}&to_city={to_city}&date_of_journey={journey_date}&seat_class=S_CHAIR"
    result = requests.get(url)
    suitable_train_list = []
    if result.status_code == 200:
        result_json = json.loads(result.text)
        for train in result_json['data']['trains']:
            train_code = train['trip_number'][-4:-1]
            suitable_train_list.append(train_code)
    return suitable_train_list


def processSearch(from_city, to_city, journey_date, suitable_train_codes):
    url = f"https://railspaapi.shohoz.com/v1.0/web/bookings/search-trips-v2?from_city={from_city}&to_city={to_city}&date_of_journey={journey_date}&seat_class=S_CHAIR"
    result = requests.get(url)
    if result.status_code == 200:
        result_json = json.loads(result.text)
        for train in result_json['data']['trains']:
            if train['trip_number'][-4:-1] not in suitable_train_codes:
                continue
            key = train['trip_number']
            search_results[key] = search_results.get(key, {"train_name": key, "available_seats": []})
            seat_types = copy.deepcopy(const_seat_types)
            has_seat = False
            for seat in train['seat_types']:
                total_available_seats = int(seat['seat_counts']['online']) + int(seat['seat_counts']['offline'])
                if total_available_seats > 0:
                    has_seat = True
                    seat_key = seat['key']
                    total_fare = float(seat['fare']) + seat['vat_amount']
                    seat_types[seat_key]['fare'] = total_fare
                    seat_types[seat_key]['seat_counts'] = total_available_seats
            if has_seat:
                search_results[key]['available_seats'].append({"from_city": from_city, "to_city": to_city, "seat_types": seat_types})


def showResults():
    for train_name in search_results:
        print(train_name)
        combo_list = search_results[train_name]['available_seats']
        # print(combo_list)
        if len(combo_list) < 1:
            print("No tickets available")
            continue
        # print(table_header)
        # print("-------------------------------------------------------------------------------------------")
        # for station_combo in combo_list:
        #     result_line = f"{station_combo['from_city']} -> {station_combo['to_city']}\t\t\t\t"
        #     for i in range(1, 9):
        #         result_line += f"\t {station_combo['seat_types'][i]['seat_counts']}"
        #     print(result_line)
        # print('\n')
        table_data = []
        for station_combo in combo_list:
            row_item = [f"{station_combo['from_city']} -> {station_combo['to_city']}"]
            for i in range(1, 9):
                row_item.append(station_combo['seat_types'][i]['seat_counts'])
            table_data.append(row_item)
        print(tabulate(table_data, headers=table_headers_list))
        print("\n")


if __name__ == '__main__':
    from_city = 'Brahmanbaria'
    to_city = 'Dhaka'
    journey_date = '23-May-2024'
    train_codes = getSuitableTrainList(from_city, to_city, journey_date)
    print(train_codes)
    for train_code in train_codes:
        station_list = getStationListByTrainCode(train_code)
        request_count += 1
        start_station_index = station_list.index(from_city)
        end_station_index = station_list.index(to_city)
        print(station_list)
        # print(f"{start_station_index}  {end_station_index}")
        # print('\n')
        for j in range(end_station_index, len(station_list)):
            for i in range(0, start_station_index + 1):
                print(f"{station_list[i]} -> {station_list[j]}")
                search_string = station_list[i] + station_list[j]
                if search_string not in search_track_map:
                    search_track_map.append(search_string)
                    processSearch(station_list[i], station_list[j], journey_date, train_codes)
                    request_count += 1

    showResults()
    print(search_results)
    print(table_headers_list)
    print(request_count + 1)
    # print(const_seat_types)