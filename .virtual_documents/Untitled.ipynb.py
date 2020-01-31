import requests
import json


def pretty(obj):
    print(json.dumps(obj, indent=2, ensure_ascii=False))


url = 'http://webservice.recruit.co.jp/hotpepper/large_area/v1/'
params = {
    'key': 'fe9c64a5d253d6fa',
    'format': 'json'
}
res = requests.get(url, params=params)
rawData = json.loads(res.text)
prefecturesData = rawData['results']['large_area']

pretty(prefecturesData)


prefectures = []
for prefectureData in prefecturesData:
    prefectures.append({
        'name': prefectureData['name'],
        'code': prefectureData['code']
    })
prefectures


url = 'http://webservice.recruit.co.jp/hotpepper/middle_area/v1/'
params = {
    'key': 'fe9c64a5d253d6fa',
    'format': 'json',
    # 'count': 2,
}
middleAreas = []

for prefecture in prefectures:
    params['large_area'] = prefecture['code']
    res = requests.get(url, params=params)
    rawData = json.loads(res.text)
    middleAreasData = rawData['results']['middle_area']

    for middleAreaData in middleAreasData:
        middleAreas.append({
            'name': middleAreaData['name'],
            'code': middleAreaData['code']
        })

middleAreas


shops = []
for shopData in shopsData:
        shops.append({
        'name': shopData['name'],
        'address': shopData['address'],
        'prefecture': shopData['large_area']['name'],
        'middle_area': shopData['middle_area']['name'],
        'small_area': shopData['small_area']['name'],
        'genre': shopData['genre']['name'],
        'budget': shopData['budget']['name']
    })

pretty(shops)






