#-------------------------------------------------------------------------------
# Name:        Py-Binger
# Purpose:     Main application to be run to collect Bing Rewards points
#
# Author:      TBrink
#
# Created:     25/09/2014
# Copyright:   (c) TBrink 2014
# Licence:     GPL2
#-------------------------------------------------------------------------------
from BingAccount import Desktop, Mobile

from BingAccount import loadAccount


def main():
    #selenium is used to automate web tasks
    #it is used in this case to login/logout of bing accounts
    #find daily point offers, and points collected today
    from selenium import webdriver


    #load in the account information
   # accounts = [Desktop(**a) for a in LoadAccounts("Accounts.txt")]

    browserLoaded = False

    for i in range(6):
        a = Desktop(**loadAccount(i))
        if a.pcEnabled == 'TRUE':
            if not browserLoaded:
                #init the desktop browser
                desktopBrowser = webdriver.Chrome('C:\\chromedriver.exe')
                desktopBrowser.set_window_size(1280,1024)
                browserLoaded = True
            ##run all desktop searches
            a.login("http://login.live.com", desktopBrowser)
            a.get_points(desktopBrowser)

            #print"Getting multiplier & calculating minimum searches"
            a.get_multiplier(desktopBrowser)

            a.generate_word_list()
            a.search(desktopBrowser)

            #get daily bonus point(s)
            a.get_bonus_points(desktopBrowser)

            #logout
            a.logout(desktopBrowser)

    if browserLoaded:
        #close desktop browser
        desktopBrowser.quit()


    browserLoaded = False

    #load all the accounts a mobile 'objects'
#    accounts = [Mobile(**a) for a in LoadAccounts("Accounts.txt")]

    #begin mobile searches
    for i in range(6):
        a = Mobile(**loadAccount(i))
        if a.mobileEnabled == 'TRUE':
            if not browserLoaded:
                #init mobile browser
                options = webdriver.ChromeOptions()
                options.add_argument('--user-agent=Mozilla/5.0\
                                    (iPhone; U; CPU iPhone OS 4_0 like Mac OS X; en-us)\
                                    AppleWebKit/532.9 (KHTML, like Gecko)\
                                    Version/4.0.5 Mobile/8A293 Safari/6531.22.7')

                mobileBrowser = webdriver.Chrome('C:\\chromedriver.exe',
                                                chrome_options=options)
                browserLoaded = True
            #login to mobile
            a.login("http://login.live.com", mobileBrowser)
            a.get_points(mobileBrowser)
            a.get_multiplier(mobileBrowser)
            a.generate_word_list()

            #run all searches
            a.search(mobileBrowser)

            a.get_bonus_points(mobileBrowser)

            #logout of account
            a.logout(mobileBrowser)

    #close mobile browser
    if browserLoaded:
        mobileBrowser.quit()
    print "Searches Complete"

if __name__ == '__main__':
    main()
