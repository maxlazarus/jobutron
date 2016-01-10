'''
Created on Jan 11, 2015

@author: max@theprogrammingclub.com
'''

def install_dependencies():
    import platform
    from subprocess import call
    if platform.system() == "Windows":
        call (["python", "-m", "pip", "install", "-U", "selenium"]) #WINDOWS
    else:
        call (["sudo", "pip", "install", "-U", "selenium"]) #LINUX, OSX
    from selenium import webdriver, common  # @NoMove @Reimport @UnusedImport

try:
    from selenium import webdriver, common  # @NoMove @UnusedImport
except:
    try:
        install_dependencies()
    except:
        execfile("get-pip.py")
        install_dependencies()
        
import selenium.webdriver.common.action_chains as ac
from os import path
from os import sep as slash
import re
import codecs

#x = json.load(f) f= json.dump(x)

top_level_domain = r"https://www.ubcengcore.com"
login = r"/secure/shibboleth.htm"
postings = r"/myAccount/co-op/postings.htm"
upload = r"/myAccount/myDocuments.htm"
image_folder = r"../browser_images/"

def login_to_site(browser, limit):
    print "Connecting..."
    for i in range(0, limit + 1):
        if i == limit:
            disconnect(browser)
            break
        print "Login attempt " + str(i + 1)
        try:
            browser.get(top_level_domain + login)
            username = str(raw_input("Enter your username: "))
            password = str(raw_input("Enter your password: "))
            browser.find_element_by_id("j_username").send_keys(username)
            browser.find_element_by_id("password").send_keys(password)
            browser.save_screenshot(image_folder + "login_attempt " + str(i + 1) + ".png")
            browser.find_element_by_name("action").click()
            print "Login form clicked"
            break
        except Exception, e:
            print "Couldn't do it: %s" % e #login failed      
            browser.save_screenshot(image_folder + "login_error.png")
           
def disconnect(browser):
    print "Disconnecting"
    browser.close()
    browser.quit()
    
def get_jobs_list(browser):
    max_attempts = 5
    for i in range(0, max_attempts):
        print "Finding job list, attempt " + str(i + 1)
        try:
            browser.get(top_level_domain + postings)
            browser.save_screenshot(image_folder + "get_jobs_list attempt " + str(i + 1) +".png")
            browser.find_element_by_xpath("//*[@id='dashboard']/div[3]/div[1]/div[2]/div/div/a[2]").click()
            print "Found master jobs list"
            break   
        except common.exceptions.NoSuchElementException, e:
            print "Couldn't do it: %s" % e #element not found yet
        i += 1

def save_current_page_as(browser, filename):
    content = browser.page_source
    print "Creating " + filename
    f = codecs.open(filename, 'w', "utf-8")
    for line in content:
        f.write(line)
    f.close()

def scrape_HTML(browser):
    '''
    <a href="?action=displayPosting&amp;postingId=61949&amp;npfGroup=">
                                        Associate Developer (Software Quality Assurance)
                                    </a>'''
    content = browser.page_source

    regex = re.compile("postingId=[0-9]\d*")
    matches = regex.findall(content)
    print matches
    
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
            save_current_page_as(browser, filename)
            browser.back()   
            
def upload_cover_letter(browser, job_id):
    print "Uploading cover letter " + job_id;
    browser.get(top_level_domain + upload)
    browser.save_screenshot(image_folder + "upload_error.png")

    #!!!!!!!!!!!!!!!!!!!!!!
    #does not work at all!!
    #!!!!!!!!!!!!!!!!!!!!!!
    a = browser.find_element_by_class_name("mediumTestButton")
    
    actions = ac.ActionChains(browser)
    actions.move_to_element(a)
    actions.click(a)
    actions.perform()

print "Welcome to jobutron by max.prokopenko@gmail.com"

try:
    browser = webdriver.PhantomJS()
except:
    browser = webdriver.PhantomJS("./phantomjs")

browser.delete_all_cookies()

login_to_site(browser, 5)
browser.save_screenshot(image_folder + "post_login.png")

job_id = "53444"
#upload_cover_letter(browser, job_id)

get_jobs_list(browser)

browser.save_screenshot(image_folder + "jobs_list.png")

scrape_HTML(browser)

disconnect(browser)

quit()
