from selenium.webdriver.common.keys import Keys
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


async def fetch_sale_data():
    driver = webdriver.Chrome()
    driver.get(
        "https://steamdb.info/sales/?min_reviews=500&min_rating=0&min_discount=60&category=401")

    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.ID, "DataTables_Table_0"))
    )

    table_body = element.find_element_by_tag_name("tbody")
    row_list = table_body.find_elements_by_tag_name("tr")

    sale_data = {}

    for row in row_list:
        data_list = []
        app_link = row.find_element_by_class_name(
            'info-icon').get_attribute('href').partition("/?")[0]
        for datum in row.find_elements_by_tag_name("td")[2:]:
            data_list.append(datum.text)
        data_list[0] = data_list[0].partition("\n")[0]
        sale_data[data_list[0]] = {
            "Discount": data_list[1],
            "Price": data_list[2],
            "Rating": data_list[3],
            "Expiration": data_list[4],
            "Sale Start": data_list[5],
            "Published": data_list[6],
            "Steam URL": app_link
        }
    driver.close()
    return sale_data
