import logging

import selenium
from selenium import webdriver

# logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
def do_screen(url):
    opt = webdriver.ChromeOptions()
    opt.add_argument('--ignore-ssl-errors=yes')
    opt.add_argument('--ignore-certificate-errors')
    opt.add_argument('--disable-dev-shm-usage')
    opt.add_argument('--no-sandbox')
    driver = webdriver.Remote(
        command_executor='http://selenium:4444',
        options=opt
    )
    try:
        driver.maximize_window()
        driver.get(url)
        file=driver.get_screenshot_as_png()
        # driver.save_screenshot(r'trash/teses.png') #TODO REMOVE
        driver.close()
        driver.quit()
        log.info('Site screened')
        return file
    except Exception as e:
        driver.close()
        driver.quit()
        raise ValueError(f'Ошибка, может быть ссылка неверная? {e}')

# if __name__ == '__main__':
#     do_screen('https://www.google.com')