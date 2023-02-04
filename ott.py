from selenium import webdriver
from bs4 import BeautifulSoup

driver = webdriver.Chrome('/Users/jungseokoh/Downloads/chromedriver_mac64/chromedriver')
#암묵적으로 웹 지원 로드를 위해 3초까지 기다려준다.
driver.implicitly_wait(3)
#url에 접근한다.
# driver.get("https://m.kinolights.com/title/3709")
driver.get("https://m.kinolights.com/ranking/netflix")
html = driver.page_source ##페이지의 element 모두 가져오기
soup = BeautifulSoup(html, 'html.parser')

#contents > div.contents-area > div:nth-child(1) > div > div > ul.chart-list-container.active > li:nth-child(1) > a > span.left-content-wrap
#contents > div.contents-area > div:nth-child(1) > div > div > ul.chart-list-container.active > li > a > span
content_names = soup.select("#contents > div.contents-area > div:nth-child(1) > div > div > ul.chart-list-container.active > li > a > span")
for content_name in content_names:
    Name = content_name.select_one('span.title-text')
    if Name is not None:
        print(Name.text)


# data_ott = []
# otts_name = soup.select("#streamingVodList > div > div.price-item-provider > div.provider-info")
# for ott_name in otts_name:
#     OTTs = ott_name.select_one('p').text
#     data_ott.append({'ott':OTTs})
#     print(data_ott)

#contents > div.movie-info-container > div.movie-image-area > div.backdrop > img
#contents > div.movie-info-container > div.movie-header-area > div.poster > img

# 이미지 가져오기
# bg_url : 큰 이미지 경로
# poster_url : 포스터(작은 이미지) 경로
# imgs = soup.select('#contents > div.movie-info-container > div')
# for img in imgs:
#     bg_image = img.select_one('div.backdrop > img')
#     if bg_image is not None:
#         bg_url = bg_image['src']
#         print(bg_url)
#     poster_image = img.select_one('div.poster > img')
#     if poster_image is not None:
#         poster_url = poster_image['src']
#         print(poster_url)

#연도 가져오기
# years = soup.select('#contents > div> div > div > p')
# for year in years:
#     detail = year.select('span')
#     year_content = detail[1].text
#     print(year_content)

#OTT이미지는 어떻게 가져올지

# data_ott_image = []
# otts_image = soup.select("#streamingVodList > div > div.price-item-provider > div.provider-info")
# for ott_image in otts_image:
#     OTTs_image = ott_image.select_one('p')
#     data_ott_image.append({'ott_image':OTTs})
#     print(data_ott_image)

