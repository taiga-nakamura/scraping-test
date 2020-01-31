from selenium import webdriver
import pandas

browser = webdriver.Chrome()
browser.get('https://scraping-for-beginner.herokuapp.com/ranking/')


touristSpots = []
elms_touristSpot = browser.find_elements_by_class_name('u_areaListRankingBox')
elms_touristSpot[0].text


for elm_touristSpot in elms_touristSpot:
    pointCategories = ['fun', 'crowd', 'view', 'access']
    touristSpot = {
        'name': elm_touristSpot.find_element_by_css_selector('.u_title h2').text.split('\n')[1],
        'total': elm_touristSpot.find_element_by_css_selector('.u_rankBox .evaluateNumber').text
    }
    elms_points = elm_touristSpot.find_elements_by_css_selector('.u_categoryTipsItem .evaluateNumber')

    for index, elm_points in enumerate(elms_points):
        category = pointCategories[index]
        touristSpot[category] = elm_points.text

    touristSpots.append(touristSpot)

print(touristSpots)






