from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from BingAccount import Desktop, Mobile
import time

account =  {'email' : 'BrunkBrink@outlook.com',
     'password' : '7875c9443a',
     'pcEnabled':True,
     'mobileEnabled': True,}

browser = webdriver.Chrome('C:\\chromedriver.exe')
a = Desktop(**account)

a.login("http://login.live.com", browser)
a.get_points(browser)
#print "%d desktop points remaining" % a.pointsRemaining
a.get_multiplier(browser)
print "%d searches for minimum desktop points (plus offset)" %a.minSearches
a.logout(browser)

browser.quit()


options = webdriver.ChromeOptions()
options.add_argument('--user-agent=Mozilla/5.0\
                        (iPhone; U; CPU iPhone OS 4_0 like Mac OS X; en-us)\
                        AppleWebKit/532.9 (KHTML, like Gecko)\
                        Version/4.0.5 Mobile/8A293 Safari/6531.22.7')

browser = webdriver.Chrome('C:\\chromedriver.exe',chrome_options=options)

a = Mobile(**account)
a.login("http://login.live.com", browser)
a.get_points(browser)
#print "%d mobile points remaining" %a.pointsRemaining
a.get_multiplier(browser)
print "%d searches for minimum mobile points (plus offset)" %a.minSearches
a.logout(browser)
browser.quit()
