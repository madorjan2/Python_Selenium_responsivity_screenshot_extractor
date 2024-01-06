'''
Created By Adorjan Meszaros
23/12/2023

Responsivity Image Extraction Tool - Driver Manager

A collection of functions that create a Selenium Webdriver object and navigate them to the desired webpage.
Only functions that start with visit_ will be called by main.py
Every visit_ functions should have a post_ method that cleans up whatever needs cleaning and quits the Webdriver.
'''

from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By

def create_driver():
    options = ChromeOptions()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=options)
    return driver

def visit_mainpage(driver=None):
    if driver is None:
        driver = create_driver()
    driver.maximize_window()
    driver.get('http://hotel-v3.progmasters.hu/')
    return driver, "mainpage"

def post_mainpage(driver):
    print('Tearing down mainpage')
    driver.quit()

def visit_register_page(driver=None):
    if driver is None:
        driver = create_driver()
    driver.maximize_window()
    driver.get('http://hotel-v3.progmasters.hu/')
    driver.find_element(By.ID, 'dropbar').click()
    driver.find_element(By.XPATH, '//a[text()="Vendég"]').click()
    return driver, "register"

def post_register_page(driver):
    print('Tearing down register')
    driver.quit()