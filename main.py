# pip install selenium pandas openpyxl fake_useragent matplotlib
from selenium import webdriver
from selenium.common import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
import pathes
import pandas as pd
import time

useragent = UserAgent()
options = webdriver.ChromeOptions()
options.add_argument(f"user-agent={useragent.random}")
browser = webdriver.Chrome(options=options)


def element_click(path: str) -> bool:
    try:
        browser.find_element(By.XPATH, path).click()
        return True
    except:
        return False


def get_element(path: str):
    try:
        el = browser.find_element(By.XPATH, path)
        return el
    except NoSuchElementException:
        return False


def find_elements_about_car(mark):
    _, tag_title, tag_sales = mark.find_elements(By.TAG_NAME, "td")
    try:
        href = pathes.URL + tag_title.find_element(By.TAG_NAME, "a").get_attribute("href")
    except NoSuchElementException:
        href = ""
    title, url, sales = tag_title.text, href, tag_sales.text
    return title, sales, url


def write_in_dict(data, car_name=None, sales=None, url=""):
    data["Бренд"].append(car_name)
    try:
        data["Объем продаж"].append(int(sales.replace(" ", "")))
    except ValueError:
        data["Объем продаж"].append(None)
    data["Ссылка"].append(url)


def get_general_statistic():
    data_cars = {i.text: [] for i in browser.find_elements(By.XPATH, pathes.TITLES_TABLE)[1:]}
    data_cars["Ссылка"] = []
    stop = False
    index = 2
    mark = get_element(pathes.CAR_TABLE + f"/tr[{index}]")  # /html/body/div[1]/div[5]/div[1]/div[1]/div[4]/div[1]/table/tbody/tr[2]/td[2]/a
    while stop is False:
        if mark is False:
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
        mark = get_element(pathes.CAR_TABLE + f"/tr[{index}]")
        if mark:
            car_name, sales, url = find_elements_about_car(mark)
            write_in_dict(data_cars, car_name=car_name, sales=sales, url=url)
            index += 1
        else:
            stop = True
    df = pd.DataFrame(data_cars)
    df.to_excel("data_cars.xlsx", index=False)


def main():
    browser.get(pathes.URL)
    browser.maximize_window()
    time.sleep(2)
    get_general_statistic()
    browser.quit()
    print("Done")


if __name__ == "__main__":
    main()
