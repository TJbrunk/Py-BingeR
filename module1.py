

#---------------------Launches Mobile Browser-----------------------------
from selenium import webdriver
from BingAccount import Mobile, LoadAccounts
import time


def logout(a,browser):
    browser.get("http://www.bing.com/rewards/dashboard")
    time.sleep(2)
    browser.find_element_by_xpath('//*[@id="mbHeader"]/a[2]/img').click()
    time.sleep(2)

    sidebar = browser.find_elements_by_tag_name("a")
    for link in sidebar:
        if link.text.find('Sign out') > -1:
            link.click()
            return


accounts = [Mobile(**a) for a in LoadAccounts("Accounts.txt")]

options = webdriver.ChromeOptions()
options.add_argument('--user-agent=Mozilla/5.0\
                        (iPhone; U; CPU iPhone OS 4_0 like Mac OS X; en-us)\
                        AppleWebKit/532.9 (KHTML, like Gecko)\
                        Version/4.0.5 Mobile/8A293 Safari/6531.22.7')

mobileBrowser = webdriver.Chrome('C:\\chromedriver.exe',chrome_options=options)

for a in accounts:
    a.login("http://login.live.com", mobileBrowser)
    time.sleep(5)
    logout(a, mobileBrowser)

#mobileBrowser.get("http://www.bing.com")






#---------------------Launches Desktop Browser-----------------------------
##from selenium import webdriver
##from selenium.webdriver.common.keys import Keys
##from BingAccount import Desktop
##import time
###
##Browser = webdriver.Chrome('C:\\chromedriver.exe')
###Browser.get("http://www.bing.com")
##accountinfo =  {'email' : 'BrunkBrink@outlook.com',
##                 'password' : '06dd95ee81',
##                 }
##account = Desktop(**accountinfo)
###Browser.get("http://www.google.com")
##account.login("http://login.live.com", Browser)
##account.get_bonus_points(Browser)
###time.sleep(3)
###body = Browser.find_element_by_tag_name('body')
###print body
###time.sleep(3)
###body.send_keys(Keys.CONTROL + 't')
###Browser.quit()