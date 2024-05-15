# %%
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs
import pandas as pd
import time

# Chrome WebDriver 다운로드 및 관리
service = Service(ChromeDriverManager().install())


# %%
main_url = "https://www.coupang.com"


def load_source(url):
    # Selenium 웹 드라이버 설정
    options = Options()
    options.add_experimental_option("detach", True)
    # options.add_argument('--headless')  # 브라우저를 표시하지 않고 실행

    # Chrome WebDriver 시작
    driver = webdriver.Chrome(service=service, options=options)

    # 페이지 열기
    driver.get(main_url + url)

    # 페이지 소스 가져오기
    page_source = driver.page_source

    # 웹 드라이버 종료
    driver.quit()

    html = page_source
    soup = bs(html, "html.parser")
    return soup


# %%
first_url = "/np/campaigns/82/components/194176"
soup = load_source(first_url)


# %%
print(soup)


# %%
# 페이지 링크 수집
page_link = []
page_link.append(first_url)
for i in range(2, 4):
    page_link.append(
        f"/np/campaigns/82/components/194176?page={i}"
     )

# %%
# 상품 정보 수집X
products = []
for link in page_link:
    time.sleep(1)
    soup = load_source(link)
    products_list = soup.find_all(class_="baby-product renew-badge")
    for product_info in products_list:
        product = {}
        product["img_src"] = "https:" + product_info.img.get("src")
        product["link_addr"] = main_url + product_info.find(class_="baby-product-link").get(
            "href"
        )
        product["product_name"] = product_info.find(class_="name").text.strip()
        product["product_price"] = product_info.find(class_="price-value").text.strip()
        products.append(product)

# %%
# 데이터프레임으로 변환
df = pd.DataFrame(products)

# %%
# CSV 파일로 저장
df.to_csv("coupang_product.csv", index=False)

# %%
