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
import re
import codecs
import getpass

#x = json.load(f) f= json.dump(x)

top_level_domain = r'https://www.ubcengcore.com'
login_path = r'/secure/shibboleth.htm'
postings_path = r'/myAccount/co-op/postings.htm'
upload = r'/myAccount/myDocuments.htm'
image_folder_path = r'../browser_images/'

def clear_images():
    folder = path.dirname(__file__).join(image_folder_path)
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            os.unlink(file_path)
        except Exception, e:
            print e

def login(browser):
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

import time

#num of jobs in this string?
#"//*[@id='postingsTablePlaceholder']/div/div/span[1]"

#get page i of results
#

def get_browser():
#clears images and returns a new PhantomJS Selenium webdriver object
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
        #sort by expiring soonest first
        #browser.find_element_by_xpath('//*[@id="postingsTable"]/thead/tr/th[6]/a/i').click()
        print 'Found jobs list'
        browser.save_screenshot(image_folder_path + 'post-jobs list page ' + str(page) + '.png')
    except common.exceptions.NoSuchElementException, e:
        raise ScriptFlowException

def save_content_as(content, filename):
#saves text content to disk
    print 'Creating ' + filename
    f = codecs.open(filename, 'w', 'utf-8')
    for line in content:      
        f.write(line)
    f.close()

def keepLoggedIn(browser):
#try to click on 'Keep me logged in'
    try:
        logged_in_xpath = '//*[@id="keepMeLoggedInModal"]/div[3]/a[1]'
        browser.find_element_by_xpath(logged_in_xpath).click()
        print 'Clicked on warning to remain logged in'
    except common.exceptions.ElementNotVisibleException, e:
        print e
    except common.exceptions.NoSuchElementException, e:
        print e
    return browser;

def scrape_HTML(browser):

    content = browser.page_source

    find_posting_id_regex = re.compile('postingId=[0-9]\d*')
    find_number_regex = re.compile('[0-9]\d*')
    matches = find_posting_id_regex.findall(content)
    
    for match in matches:
        numerical_id = find_number_regex.findall(match)[0].encode('ascii')

        filepath = path.abspath(path.join(path.dirname(__file__), '..', 'jobs'))
        filename = filepath + sep + numerical_id + '.html'

        #if file does not exist yet  
        if path.isfile(filename) is not True:
            print 'Accessing job ' + numerical_id

            #click on next job
            try:
                job_xpath = '//*[@id="posting' + numerical_id + '"]/td[2]/strong/a'
                browser.find_element_by_xpath(job_xpath).click()
            except common.exceptions.NoSuchElementException, e:
                job_xpath = '//*[@id="posting' + numerical_id + '"]/td[2]/a[1]'
                browser.find_element_by_xpath(job_xpath).click()

            save_content_as(browser.page_source, filename)
            browser.save_screenshot(image_folder_path + 'access attempt for job ' + numerical_id + '.png')
            

            #back to job search results
            try:
                return_xpath = '//*[@id="mainContentDiv"]/div[2]/div/div/div/div[2]/div/div[2]/div[3]/div/ul/li[1]/a'
                browser.find_element_by_xpath(return_xpath).click()
            except common.exceptions.NoSuchElementException, e:
                raise ScriptFlowException

            
def upload_cover_letter(browser, job_id): 
#! Unimplemented    
    print 'Uploading cover letter ' + job_id;
    browser.get(top_level_domain + upload)

def main():
    from optparse import OptionParser
    parser = OptionParser()
    '''
    parser.add_option("-f", "--file", dest="filename",
                      help="write report to FILE", metavar="FILE")
    parser.add_option("-q", "--quiet",
                      action="store_false", dest="verbose", default=True,
                      help="don't print status messages to stdout")
    '''
    (options, args) = parser.parse_args()
    print 'Welcome to jobutron by max.prokopenko@gmail.com'
    b = get_browser()
    b = login(b)
    for arg in args:
        b = to_postings(b)
        b = to_job(b, arg)
        save_content_as(b.page_source, "../jobs/" + str(arg) + ".html")
    disconnect(b)
    quit()

if __name__ == '__main__':
    main()