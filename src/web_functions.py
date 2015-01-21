'''
Created on Jan 11, 2015

@author: max@theprogrammingclub.com
'''

try:
    from selenium import webdriver, common  # @NoMove @UnusedImport
except:
    from subprocess import call
    call (["sudo", "pip", "install", "-U", "selenium"])
    from selenium import webdriver, common  # @NoMove @Reimport @UnusedImport
import selenium.webdriver.common.action_chains as ac
from os import path
from os import sep as slash
import re
import codecs

#x = json.load(f) f= json.dump(x)

tld = r"https://www.ubcengcore.com"
login = r"/secure/shibboleth.htm"
postings = r"/myAccount/postings.htm"
upload = r"/myAccount/myDocuments.htm"

def login_to_site(browser, limit):
    print "Connecting..."
    i = 1
    loop = True
    while loop == True:
        print "Login attempt " + str(i)
        i += 1
        try:
            browser.get(tld + login)
            username = str(raw_input("Enter your username: "))
            password = str(raw_input("Enter your password: "))
            browser.find_element_by_id("j_username").send_keys(username)
            browser.find_element_by_id("password").send_keys(password)
            browser.find_element_by_name("action").click()
            loop = False
        except Exception, e:
            print "Couldn't do it: %s" % e #login failed      
            browser.save_screenshot("login_error.png")
            loop = True
            if i > limit:
                disconnect(browser)
           
def disconnect(browser):
    print "Disconnecting"
    browser.close()
    browser.quit()
    
def get_jobs_list(browser):
    i = 1
    while True:
        print "Finding job list, attempt " + str(i)
        i += 1
        try:
            browser.save_screenshot("job_attempt.png")
            browser.get(tld + postings)
            browser.find_element_by_id("fs5").submit()
            break
        except common.exceptions.NoSuchElementException, e:
            print "Couldn't do it: %s" % e #element not found yet

def scrape_HTML(content) :
    regex = re.compile("postingViewForm[0-9]\d*")
    matches = regex.findall(content)
    
    basepath = path.dirname(__file__)
    filepath = path.abspath(path.join(basepath, "..", "jobs"))
    
    for form_id in matches:
        regex = re.compile("\d+$") 
        numerical_id = regex.findall(form_id)[0]
        numerical_id = numerical_id.encode("ascii")
        
        filename = filepath + slash + numerical_id + '.html'
        
        if path.isfile(filename) is not True: # file does not exist yet    
            form = browser.find_element_by_id(form_id)
            form.submit()
            content = browser.page_source
            #browser.save_screenshot("last.png")
            
            print "Creating " + filename
            f = codecs.open(filename, 'w', "utf-8")
            for line in content:
                f.write(line)
            f.close()
        
            browser.back()        
            
def upload_cover_letter(browser, job_id):
    print "Uploading cover letter " + job_id;
    browser.get(tld + upload)
    browser.save_screenshot("upload_error.png")

    #!!!!!!!!!!!!!!!!!!!!!!
    #does not work at all!!
    #!!!!!!!!!!!!!!!!!!!!!!
    a = browser.find_element_by_class_name("mediumTestButton")
    
    actions = ac.ActionChains(browser)
    actions.move_to_element(a)
    actions.click(a)
    actions.perform()
    browser.save_screenshot("last1.png")
    
print "Welcome to jobulator by max@theprogrammingclub.com"

try:
    browser = webdriver.PhantomJS()
except:
    browser = webdriver.PhantomJS("./phantomjs")

browser.delete_all_cookies()

login_to_site(browser, 5)

job_id = "53444"
#upload_cover_letter(browser, job_id)

get_jobs_list(browser)
content = browser.page_source
scrape_HTML(content)

disconnect(browser)

quit()
