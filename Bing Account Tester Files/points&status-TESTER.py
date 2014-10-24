from BingAccount import Desktop, Mobile, loadAccount
from selenium import webdriver

def get_points_status(a, browser):
    browser.get("http://www.bing.com/rewards/dashboard")
    status = browser.find_element_by_class_name('level-right').text.split('\n')[0]
    points = browser.find_element_by_class_name('credits').text

    return [str(status), int(points)]


def progress_credits(a, browser):
    browser.get("http://www.bing.com/rewards/dashboard")
   # try:
    progress = browser.find_element_by_class_name('progress-credits').text.split(' of ')
    if int(progress[1]) - int(progress[0]) >= 0:
        print "You got free internet money"
   # except:
   #     print "no goal set"



account = Desktop(**loadAccount(0))

browser = webdriver.Chrome('C:\\chromedriver.exe')
browser.set_window_size(1280,1024)

account.login("http://login.live.com", browser)
#print get_points_status(account, browser)
progress_credits(account, browser)


##account = Mobile(**loadAccount(1))
##
##options = webdriver.ChromeOptions()
##options.add_argument('--user-agent=Mozilla/5.0\
##                        (iPhone; U; CPU iPhone OS 4_0 like Mac OS X; en-us)\
##                        AppleWebKit/532.9 (KHTML, like Gecko)\
##                        Version/4.0.5 Mobile/8A293 Safari/6531.22.7')
##
##browser = webdriver.Chrome('C:\\chromedriver.exe',chrome_options=options)
##
##account.login("http://login.live.com", browser)
##
##account.browser)
##





account.logout

browser.quit()