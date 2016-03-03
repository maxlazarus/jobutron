'''
Created on Jan 11, 2015

@author: max@theprogrammingclub.com
'''

def install_dependencies():
    import platform
    from subprocess import call
    if platform.system() == 'Windows':
        call (['python', '-m', 'pip', 'install', '-U', 'selenium']) #WINDOWS
    else:
        call (['sudo', 'pip', 'install', '-U', 'selenium']) #LINUX, OSX
    from selenium import webdriver, common  # @NoMove @Reimport @UnusedImport

try:
    from selenium import webdriver, common  # @NoMove @UnusedImport
except:
    try:
        install_dependencies()
    except:
        execfile('get-pip.py')
        install_dependencies()

import os
from os import path
from os import sep
from subprocess import call
import re
import codecs
import getpass
import time

top_level_domain = r'https://www.ubcengcore.com'
login_path = r'/secure/shibboleth.htm'
postings_path = r'/myAccount/co-op/postings.htm'
upload_path = r'/myAccount/co-op/myDocuments.htm'
image_folder_path = r'../browser_images/'

def clear_images():
    '''clears all the files in the image_folder_path location'''
    folder = path.dirname(__file__) + (image_folder_path)
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            os.unlink(file_path)
        except Exception, e:
            print e

def login(browser):
    '''opens top_level_domain and attempts a login, prompting for user & pass'''
    print 'Starting login attempt'
    try:
        browser.get(top_level_domain + login_path)

        username = str(raw_input('Enter your username: '))
        
        with open('username.txt', 'r+') as f:
            if username == '':
                username = f.read()
                print 'Using saved username: ' + username
            else:
                f.seek(0)
                f.write(username)
        browser.find_element_by_id('j_username').send_keys(username)
        
        password = getpass.getpass('Enter your password: ')
        
        browser.find_element_by_id('password').send_keys(password)
        browser.save_screenshot(image_folder_path + 'login_attempt.png')
        continue_xpath = '//*[@id="col2"]/form/fieldset/input'
        browser.find_element_by_xpath(continue_xpath).click()
        print 'Login form clicked'
    except Exception, e:
        print 'Couldn\'t do it: %s' % e #login failed      
        browser.save_screenshot(image_folder_path + 'login_error.png')
    return browser
           
def disconnect(browser):
    print 'Disconnecting...'
    browser.close()
    browser.quit()


def get_browser():
    '''clears images and returns a new PhantomJS Selenium webdriver object'''
    try:
        browser = webdriver.PhantomJS()
    except:
        browser = webdriver.PhantomJS('./phantomjs')
    browser.implicitly_wait(3)
    browser.delete_all_cookies()
    clear_images()
    print 'Browser opened'
    return browser

def to_postings(browser):
    browser.get(top_level_domain + postings_path)
    print 'Navigated to postings page'
    return browser

def to_job(browser, numerical_id):
    job_search_xpath = '//*[@id="searchByPostingNumberForm"]/input[2]'
    search_button_xpath = '//*[@id="searchByPostingNumberForm"]/a'
    browser.find_element_by_xpath(job_search_xpath).send_keys(str(numerical_id))
    browser.find_element_by_xpath(search_button_xpath).click()
    print 'Navigated to job ' + str(numerical_id)
    return browser

def get_jobs_list(browser, page):
    '''grabs the first page of jobs - may be broken'''
    print 'Finding job list page ' + str(page)  
    try:
        browser.get(top_level_domain + postings_path)
        browser.save_screenshot(image_folder_path + 'get_jobs_list attempt.png')
        page_1_xpath = '//*[@id="dashboard"]/div[3]/div[1]/div[2]/div/div/a[2]'
        page_other_xpath = '//*[@id="postingsTablePlaceholder"]/div/div/div/ul/li[' + str(page + 1) + ']/a'
        page_xpath = None
        if page == 1:
            page_xpath = page_1_xpath
        else:
            browser.find_element_by_xpath(page_1_xpath).click()
            time.sleep(10)
            page_xpath = page_other_xpath
        browser.find_element_by_xpath(page_xpath).click()
        print 'Found jobs list'
        browser.save_screenshot(image_folder_path + 'post-jobs list page ' + str(page) + '.png')
    except common.exceptions.NoSuchElementException, e:
        raise ScriptFlowException

def save_content_as(content, filename):
    '''saves text content to disk'''
    print 'Creating ' + filename
    f = codecs.open(filename, 'w', 'utf-8')
    for line in content:      
        f.write(line)
    f.close()

def relog_in(browser):
    '''try to click on "Keep me logged in"'''
    try:
        logged_in_xpath = '//*[@id="keepMeLoggedInModal"]/div[3]/a[1]'
        browser.find_element_by_xpath(logged_in_xpath).click()
        print 'Clicked on warning to remain logged in'
    except common.exceptions.ElementNotVisibleException, e:
        print e
    except common.exceptions.NoSuchElementException, e:
        print e
    return browser;

def to_upload(browser):
    upload_button_xpath = '//*[@id="mainContentDiv"]/div[2]/div/a[1]'
    print browser.current_url
    browser.get(top_level_domain + upload_path)
    time.sleep(3)
    print browser.current_url
    browser.save_screenshot(image_folder_path + 'cover upload.png')
    browser.find_element_by_xpath(upload_button_xpath).click()
    print 'Navigated to upload page'
    return browser

def upload_cover(browser, numerical_id):
    name_xpath = '//*[@id="fileUploadForm"]/div[1]/div[2]/input'
    type_xpath = '//*[@id="fileUploadForm"]/div[2]/div[2]/select/option[2]'
    choose_file_xpath = '//*[@id="fileUploadForm"]/div[2]/div[2]/select'
    finish_upload_button_xpath = '//*[@id="mainContentDiv"]/div[2]/div/div/div/div/div/a[1]'

    filepath = path.abspath(path.join(path.dirname(__file__), '..', 'res/' + str(numerical_id) + '.docx'))
    browser.find_element_by_xpath(name_xpath).send_keys(str(numerical_id))
    browser.find_element_by_xpath(type_xpath).click()
    try:
        browser.find_element_by_xpath(choose_file_xpath).send_keys(filepath)
    except Exception, e:
        browser.save_screenshot(image_folder_path, 'cover upload.png')
        raise e
    print 'Uploaded cover ' + str(numerical_id)
    return browser

if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option('-g', '--get', action='store_true', dest='mode')
    parser.add_option('-u', '--upload', action='store_false', dest='mode')
    (options, args) = parser.parse_args()
    print 'Welcome to jobutron by max.prokopenko@gmail.com'
    b = get_browser()
    b = login(b)

    if(options.mode == True): #save jobs specified in -g
        for arg in args:
            b = to_postings(b)
            b = to_job(b, arg)
            save_content_as(b.page_source, "../jobs/" + str(arg) + ".html")

    if(options.mode == False): #upload jobs (non-functional)
        for arg in args:
            b = to_upload(b)
            b = upload_cover(b, arg)

    disconnect(b)
    call(["../bin/Release/jobulator.exe"])
    quit()