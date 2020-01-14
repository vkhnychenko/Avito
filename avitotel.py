# -*- coding: utf-8 -*-
from time import sleep

from selenium import webdriver
from PIL import Image
from pytesseract import image_to_string
from selenium.webdriver.firefox.options import Options

class Bot:
    def __init__(self,html):
        options = Options()
        options.headless = True
        self.html = html
        self.driver = webdriver.Firefox(options=options)
        self.navigate(self.html)
        self.driver.close()

    def take_screenshot(self):
        self.driver.save_screenshot('avito_screenshot.png')

    def tel_recon(self):
        image = Image.open('tel.gif')
        numb = image_to_string(image)
        return numb

    def crop(self, location, size):
        image = Image.open('avito_screenshot.png')
        x = location['x']
        y = location['y']
        width = size['width']
        height = size['height']

        image.crop((x, y, x + width, y + height)).save('tel.gif')
        self.tel_recon()


    def navigate(self,html):
        self.driver.get(html)

        button = self.driver.find_element_by_xpath('//a[@class="button item-phone-button js-item-phone-button button-origin button-origin-blue button-origin_full-width button-origin_large-extra item-phone-button_hide-phone item-phone-button_card js-item-phone-button_card"]')
        button.click()

        sleep(3)

        self.take_screenshot()

        image = self.driver.find_element_by_xpath('//div[@class="item-phone-big-number js-item-phone-big-number"]//*')
        location = image.location       #dict {'x':123456, 'y':123456}
        size = image.size               #dict {'width':256, 'height':568}

        self.crop(location, size)

