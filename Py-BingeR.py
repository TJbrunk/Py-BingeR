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

                for x in range(3):
                    #login to mobile
                    a.login("http://login.live.com", desktopBrowser)
                    loggedin = a.verify_login(desktopBrowser)
                    if loggedin:
                        print "Logged in"
                        a.get_points(desktopBrowser)
                        a.get_multiplier(desktopBrowser)

                        a.generate_word_list()

                        #run all searches
                        a.search(desktopBrowser)

                        a.get_bonus_points(desktopBrowser)

            #            a.goal_check(desktopBrowser)

                        #logout of account
                        a.logout(desktopBrowser)
                        if a.verify_logout(desktopBrowser):
                            pass
                        else:
                            desktopBrowser.quit()
                            browserLoaded = False
                        break
                    else:
                        print "Error Logging in as %s\n\n" % a.email

        except IndexError:
            #We get an index error after all the accounts in the file have been run
            print "Finished with PC searches"
            print '=' * 80
            break
        except selenium.common.exceptions.NoSuchElementException:
            print "Selenium encountered and error. Verify the account\n\n"
            desktopBrowser.quit()
            browserLoaded = False
        except:
            print "general error. proceeding to next account"


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
                for x in range(3):
                    #login to mobile
                    a.login("http://login.live.com", mobileBrowser)
                    loggedin = a.verify_login(mobileBrowser)
                    if loggedin:
                        print "Logged in"
                        a.get_points(mobileBrowser)
                        a.get_multiplier(mobileBrowser)
                        a.generate_word_list()

                        #run all searches
                        a.search(mobileBrowser)

                        a.get_bonus_points(mobileBrowser)

            #            a.goal_check(mobileBrowser)

                        #logout of account
                        a.logout(mobileBrowser)
                        if a.verify_logout(mobileBrowser):
                            pass
                        else:
                            mobileBrowser.quit()
                            browserLoaded = False
                        break
                    else:
                        print "Error logging in as %s\n\n" % a.email

        except IndexError:
            print "Finished with mobile searches"
            print '=' * 80
            break
        except selenium.common.exceptions.NoSuchElementException:
            print "Selenium encountered and error. Verify the account\n\n"
            mobileBrowser.quit()
            browserLoaded = False
        except:
            print "general error. proceeding to next account"


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
        print "-v or --verbose : enable vebose output for debugging"
        print "-a <#> or --account <#> : Run Py-BingeR with only the these accounts\
        from the account file\nNOTE: NOT CURRENTLY IMPLEMENTED"

    accFile = workingDir + '\\accounts.csv'
    verbose = False
    account = False

    try:
        opts, args = getopt.getopt(argv, "f:da:", ['file','debug', 'account'])


        for opt, arg in opts:
            if opt in ('-h', '--help'):
                Help()

            if opt in ('-f', '--file'):
               accFile = arg

            if opt in ('-v', '--verbose'):
                verbose = True
                print "Verbose output enabled"

            if opt in ('-a', '--account'):
                account = arg

        return {'accountFile':accFile, 'verbose':verbose, 'account':account}

    except getopt.GetoptError:
        print "argument error"
        Help()
        sys.exit(2)


if __name__ == '__main__':
    import sys
    main(sys.argv[1:])
