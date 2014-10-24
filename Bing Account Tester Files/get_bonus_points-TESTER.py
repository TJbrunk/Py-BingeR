from BingAccount import Desktop, Mobile, loadAccount
from selenium import webdriver

##account = Desktop(**loadAccount(1))
##
##browser = webdriver.Chrome('C:\\chromedriver.exe')
##browser.set_window_size(1280,1024)
##
##account.login("http://login.live.com", browser)
##account.get_bonus_points(browser)
##
##browser.quit()

account = Mobile(**loadAccount(1))

options = webdriver.ChromeOptions()
options.add_argument('--user-agent=Mozilla/5.0\
                        (iPhone; U; CPU iPhone OS 4_0 like Mac OS X; en-us)\
                        AppleWebKit/532.9 (KHTML, like Gecko)\
                        Version/4.0.5 Mobile/8A293 Safari/6531.22.7')

browser = webdriver.Chrome('C:\\chromedriver.exe',chrome_options=options)

account.login("http://login.live.com", browser)

account.get_bonus_points(browser)






account.logout

browser.quit()