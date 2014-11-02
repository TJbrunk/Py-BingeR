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
def main(argv):
    import bingaccount.BingAccount
    from bingaccount import Desktop, Mobile
    from bingaccount import loadAccount
    import os, getopt


    #selenium is used to automate web tasks
    #it is used in this case to login/logout of bing accounts
    #find daily point offers, and points collected today
    from selenium import webdriver
    import selenium.common.exceptions

    workingDir = os.getcwd() + '\\dependencies'

    inputs = Parse_Inputs(argv, workingDir)


    browserLoaded = False
    i=0
    while True:
        try:
            i+=1
            a = Desktop.Desktop(**loadAccount.loadAccount(i, inputs['accountFile']))
            if a.pcEnabled == 'TRUE':
                if not browserLoaded:
                    #init the desktop browser
                    desktopBrowser = webdriver.Chrome(workingDir +'\chromedriver.exe')
                    desktopBrowser.set_window_size(1280,1024)
                    desktopBrowser.implicitly_wait(10)
                    browserLoaded = True

                #Login and verify the login
                a.login("http://login.live.com", desktopBrowser)

                #Find how many points can be earned for Desktop searches
                a.get_points(desktopBrowser)

                #Calc the number of searches need to get all the points
                a.get_multiplier(desktopBrowser)

                #Get random words for the number of searches to perform
                a.generate_word_list()

                #search all for all the word
                a.search(desktopBrowser)

                #get daily bonus point(s)
                a.get_bonus_points(desktopBrowser)


                #logout
                a.logout(desktopBrowser)
        except IndexError:
            #We get an index error after all the accounts in the file have been run
            print "Finished with PC searches"
            break
        except selenium.common.exceptions.NoSuchElementException:
            print "Selenium encountered and error. Verify the account"
        except StandardError:
            print "Unable to login %s" % a.email

    if browserLoaded:
        #close desktop browser
        desktopBrowser.quit()

    browserLoaded = False

    #begin mobile searches
    i = 0
    while True:
        try:
            i += 1
            a = Mobile.Mobile(**loadAccount.loadAccount(i, inputs['accountFile']))
            if a.mobileEnabled == 'TRUE':
                if not browserLoaded:
                    #init mobile browser
                    options = webdriver.ChromeOptions()
                    options.add_argument('--user-agent=Mozilla/5.0\
                                        (iPhone; U; CPU iPhone OS 4_0 like Mac OS X; en-us)\
                                        AppleWebKit/532.9 (KHTML, like Gecko)\
                                        Version/4.0.5 Mobile/8A293 Safari/6531.22.7')

                    mobileBrowser = webdriver.Chrome(workingDir + '\chromedriver.exe',
                                                    chrome_options=options)
                    mobileBrowser.implicitly_wait(10)
                    browserLoaded = True
                #login to mobile
                a.login("http://login.live.com", mobileBrowser)

                a.get_points(mobileBrowser)
                a.get_multiplier(mobileBrowser)
                a.generate_word_list()

                #run all searches
                a.search(mobileBrowser)

                a.get_bonus_points(mobileBrowser)

    #            a.goal_check(mobileBrowser)

                #logout of account
                a.logout(mobileBrowser)

        except IndexError:
            print "Finished with mobile searches"
            break
        except selenium.common.exceptions.NoSuchElementException:
			print "Selenium encountered and error. Verify the account"
        except StandardError:
            print "Unable to login %s" % a.email

    #close mobile browser
    if browserLoaded:
        mobileBrowser.quit()
    print "ALL Searches Complete"

#===============================================================================

def Parse_Inputs(argv, workingDir):
    import getopt

    def Help():
        print "Usage:"
        print "-h or --help : display this help menu"
        print "-f <account.csv file> or --file <account.csv file> : use to specify\
        an account file other than the default"
        print "-d or --debug : enable vebose output for debugging"
        print "-a <#> or --account <#> : Run Py-BingeR with only the these accounts\
        from the account file"

    accFile = workingDir + '\\accounts.csv'
    debug = False
    account = False

    try:
        opts, args = getopt.getopt(argv, "f:da:", ['file','debug', 'account'])


        for opt, arg in opts:
            if opt in ('-h', '--help'):
                Help()

            if opt in ('-f', '--file'):
               accFile = arg

            if opt in ('-d', '--debug'):
                debug = True
                print "debugging enabled"

            if opt in ('-a', '--account'):
                account = arg

        return {'accountFile':accFile, 'debug':debug, 'account':account}

    except getopt.GetoptError:
        print "argument error"
        Help()
        sys.exit(2)


if __name__ == '__main__':
    import sys
    main(sys.argv[1:])
