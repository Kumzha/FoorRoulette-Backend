import requests
import json
from schemas import Restaurant

def formatBoltDeliveryTime(min: int, max: int) -> str:
    min_minutes = int(min/60)
    max_minutes = int(max/60)
    return f"{min_minutes}-{max_minutes} min"


def getBoltRestaurants(lat: float, lng: float) -> list[Restaurant]:

    headers = {
        'accept': '*/*',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'origin': 'https://food.bolt.eu',
        'priority': 'u=1, i',
        'referer': 'https://food.bolt.eu/',
        '^sec-ch-ua': '^\\^Not/A)Brand^\\^;v=^\\^8^\\^, ^\\^Chromium^\\^;v=^\\^126^\\^, ^\\^Google',
        'sec-ch-ua-mobile': '?0',
        '^sec-ch-ua-platform': '^\\^Windows^\\^^',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    }


    #TODO need to gather city id info
    params = (
        ('delivery_lat', lat),
        ('delivery_lng', lng),
        ('city_id', '9'),
        ('version', 'FW.1.70'),
        ('language', 'en-US'),
        ('session_id', '0'),
        ('device_name', 'web'),
        ('device_os_version', 'web'),
        ('deviceId', '0'),
        ('deviceType', 'web'),
    )
    
    # Do the request and make it readable, iteratable
    response = requests.get('https://deliveryuser.live.boltsvc.net/deliveryClient/public/getHomeCategories', headers=headers, params=params)
    response_object = response.json()
    response_string = json.dumps(response_object, indent = 4)

    restaurant_list = []

    
    file_path = 'textfiles/bolt_providers.txt'
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(response_string) 

    # print(response_object['data']['providers'][0]['rating_info']["rating_value"])

    # City not found error response: {'code': 5812, 'message': 'CITY_NOT_FOUND', 'error_hint': 'City not found for (0; 0)'}
    try:
    #TODO delivery price must be checked if outside Europe(euro)
        for provider in response_object['data']['providers']:

            if provider['is_available'] == True:

                if provider['rating_info'] is None or provider['rating_info']["rating_value"] is None:
                    #TODO can play around with this
                    provider_rating = 3 
                else:
                    provider_rating = provider['rating_info']["rating_value"]

                restaurant = Restaurant(
                                bolt = True, 
                                url="https://food.bolt.eu/lt-LT/9-vilnius/p/" + str(provider['provider_id']),
                                name=provider['name']['value'],
                                # rating=provider['rating_info']["rating_value"],
                                address=provider['address'],
                                estimated_delivery_time=formatBoltDeliveryTime(provider['min_delivery_eta'],provider['max_delivery_eta']),
                                image=provider['images']['provider_list_v1']['aspect_ratio_map']['original']['3x'],
                                rating=provider_rating,
                                #TODO implement tags/categories
                                tags=provider['tags'],
                                delivery_price=provider['delivery_price']['price_str']
                                )
                
                restaurant_list.append(restaurant)
    except:
        return restaurant_list

    # Writes all reduced info into a file

    # restaurant_dicts = [restaurant.dict() for restaurant in restaurant_list]
    # restaurant_string = json.dumps(restaurant_dicts, indent = 4)
    # file_path = 'textfiles/bolt_providers.txt'
    # with open(file_path, 'w', encoding='utf-8') as file:
    #     file.write(restaurant_string)

    return restaurant_list



# getBoltRestaurants("Pavasario gatve 30")

