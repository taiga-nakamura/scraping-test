import requests
import json


def pretty(obj):
    print(json.dumps(obj, indent=2, ensure_ascii=False))


def fetch(target, paramsOption={}):
    baseUrl = 'http://webservice.recruit.co.jp/hotpepper/'
    apiVersion = 'v1'
    defaultParams = {
        'key': 'fe9c64a5d253d6fa',
        'format': 'json'
    }
    url = f'{baseUrl}{target}/{apiVersion}'
    params = dict(defaultParams, **paramsOption)
    response = requests.get(url, params=params)
    return json.loads(response.text)


def getLargeAreas():
    data = fetch('large_area')
    areas = []

    for datum in data['results']['large_area']:
        areas.append({
            'name': datum['name'],
            'code': datum['code']
        })

    return areas


cache_middleArea = []


def getMiddleAreas():
    global cache_middleArea

    if 0 < len(cache_middleArea):
        print('Used cache_middleArea')
        return cache_middleArea

    largeAreas = getLargeAreas()
    middleAreas = [] 

    for largeArea in largeAreas:
        data = fetch('middle_area', {'large_area': largeArea['code']})

        for datum in data['results']['middle_area']:
            middleAreas.append({
                'name': datum['name'],
                'code': datum['code'],
                'large_area': datum['large_area']
            })

    cache_middleArea = middleAreas
    return middleAreas


def getSmallAreas():
    middleAreas = getMiddleAreas()
    smallAreas = []

    for middleArea in middleAreas:
        data = fetch('small_area', {'middle_area': middleArea['code']})

        for datum in data['results']['small_area']:
            smallAreas.append({
                'name': datum['name'],
                'code': datum['code'],
                'middle_area': datum['middle_area'],
                'large_area': datum['large_area']
            })

    return smallAreas

# areaList = getSmallAreas()
pretty(len(areaList))


data = fetch('gourmet', {
#     'large_area': 'Z011',
    'middle_area': 'Y005',
#     'small_area': 'X005',
    'count': 1
})
pretty(data)


count = 10
offset = 101
for i in range(5):
    data = fetch('gourmet', {
    #     'large_area': 'Z011',
        'middle_area': 'Y007',
    #     'small_area': 'X005',
        'type': 'lite',
        'count': count,
        'start': offset
    })
    results_available = data['results']['results_available']
    num_shops = len(data['results']['shop'])
    print(f'i:{i}, results_available:{results_available}, num_shop:{num_shops}, offset:{offset}')
    offset += count
    if 0 < num_shops: continue


data = getMiddleAreas()
pretty(data)


def formatRestaurantData(data):
    return {
        'name': data['name'],
        'address': data['address'],
        'large_area': data['large_area']['name'],
        'middle_area': data['middle_area']['name'],
        'small_area': data['small_area']['name'],
        'genre': data['genre']['name'],
        'budget': data['budget']['name']
    }


def getRestaurants():
    middleAreas = getMiddleAreas()
    restaurants = []
    count = 1

    for middleArea in middleAreas:
        offset = 2831
        while True:
            data = fetch('gourmet', {
                'middle_area': middleArea['code'],
                'order': 3,  # 小エリアコード順
                'count': count,
                'start': offset
            })

            restaurantsData = data['results']['shop']

            print(f"available:{data['results']['results_available']}, offset:{offset}, num_shop:{len(restaurantsData)}")
            if len(restaurantsData) == 0: break

            for data in restaurantsData:
                restaurants.append(formatRestaurantData(data))

            offset += count
        break

    return restaurants


getRestaurants()



