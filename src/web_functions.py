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
            
            with open("username.txt", 'r+') as f:
                if username == "":
                    username = f.read()
                    print "Using saved username: " + username
                else:
                    f.seek(0)
                    f.write(username)

            browser.find_element_by_id("j_username").send_keys(username)
            password = str(raw_input("Enter your password: "))

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

#num of jobs in this string?
#"//*[@id='postingsTablePlaceholder']/div/div/span[1]"

#get page i of results
#"//*[@id='postingsTablePlaceholder']/div/div/div/ul/li[" + str(i) + "]/a"

def get_jobs_list(browser, max_attempts):

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

def save_content_as(content, filename):

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

    basepath = path.dirname(__file__)
    filepath = path.abspath(path.join(basepath, "..", "jobs"))

    find_posting_id_regex = re.compile("postingId=[0-9]\d*")
    find_number_regex = re.compile("[0-9]\d*")
    matches = find_posting_id_regex.findall(content)
    
    for match in matches:
        numerical_id = find_number_regex.findall(match)[0].encode("ascii")
        filename = filepath + slash + numerical_id + '.html'

        #if file does not exist yet  
        if path.isfile(filename) is not True:
            print "Accessing job " + numerical_id

            #click on next job
            try:
                job_xpath = "//*[@id='posting" + numerical_id + "']/td[2]/strong/a"
                browser.find_element_by_xpath(job_xpath).click()
            except common.exceptions.NoSuchElementException, e:
                job_xpath = "//*[@id='posting" + numerical_id + "']/td[2]/a[1]"
                browser.find_element_by_xpath(job_xpath).click()

            save_content_as(browser.page_source, filename)
            browser.save_screenshot(image_folder + "access attempt for job " + numerical_id + ".png")
            
            #try to click on "Keep me logged in"
            try:
                logged_in_xpath = "//*[@id='keepMeLoggedInModal']/div[3]/a[1]"
                browser.find_element_by_xpath(logged_in_xpath).click()
                print "Clicked on warning to remain logged in"
            except common.exceptions.ElementNotVisibleException, e:
                pass

            #back to job search results
            return_xpath = "//*[@id='mainContentDiv']/div[2]/div/div/div/div[2]/div/div[2]/div[3]/div/ul/li[1]/a"
            browser.find_element_by_xpath(return_xpath).click()
    '''
    
    
    for form_id in matches:
        regex = re.compile("\d+$") 
        numerical_id = regex.findall(form_id)[0]
        numerical_id = numerical_id.encode("ascii")
        
        filename = filepath + slash + numerical_id + '.html'
        
        if path.isfile(filename) is not True: # file does not exist yet    
            form = browser.find_element_by_id(form_id)
            form.submit()     
            save_content_as(browser.page_source, filename)
            browser.back()   
    '''
            
def upload_cover_letter(browser, job_id): #! Unimplemented
    
    print "Uploading cover letter " + job_id;
    browser.get(top_level_domain + upload)

print "Welcome to jobutron by max.prokopenko@gmail.com"

try:
    browser = webdriver.PhantomJS()
except:
    browser = webdriver.PhantomJS("./phantomjs")

browser.delete_all_cookies()

max_attempts = 5;

login_to_site(browser, max_attempts)
get_jobs_list(browser, max_attempts)
scrape_HTML(browser)
disconnect(browser)

quit()