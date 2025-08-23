import logging

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


async def pars_link_for_auto_pars():
    links = []
    options = Options()
    options.add_argument("--headless")  # Фоновый режим
    options.add_argument("--disable_gpu")
    driver = webdriver.Chrome(options=options)
    try:
        driver.get("https://www.xbox.com/en-US/promotions/sales/sales-and-specials?xr=shellnav")

        # Ищем все кнопки с "SHOP MORE"
        buttons = driver.find_elements(By.XPATH, '//a[.//span[contains(text(), "SHOP MORE")]]')

        links = [button.get_attribute("href") for button in buttons if button.get_attribute("href")]
        links = [link.replace("xbox.com/", "xbox.com/en-US/") for link in links]
        driver.quit()
    except Exception as e:
        driver.quit()
        logging.error(f"Ошибка ссылок для автопарса {e}")

    return links




if __name__ == '__main__':
    pars_link_for_auto_pars()
