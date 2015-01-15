'''
Created on Jan 14, 2015

@author: max@theprogrammingclub.com
'''
def enter_username_and_password(browser):
    username = "YOUR_USERNAME"
    password = "YOUR_PASSWORD"
    browser.find_element_by_id("j_username").send_keys(username)
    browser.find_element_by_id("password").send_keys(password)
    browser.find_element_by_name("action").click()