import BingAccount, random, time, os

#*********************************MOBILE CHILDCLASS*****************************
class Mobile(BingAccount.BingAccount):
    """Mobile settings subclass of main Bing Accounts class"""
    def __init__(self, email, password, **kwargs):

        self.mobileEnabled = kwargs['mobileEnabled']
        self.searchWaitLong = int(kwargs['searchWaitLong'])
        self.searchWaitShort = int(kwargs['searchWaitShort'])
        self.minSearchesLow = int(kwargs['minSearchesLow'])
        self.minSearchesHigh = int(kwargs['minSearchesHigh'])
        self.startDelayLow = int(kwargs['startDelayLow'])
        self.startDelayHigh = int(kwargs['startDelayHigh'])

        self._dir_ = os.getcwd() + '\\dependencies'

                #if Low < High pick random # for extra searches
        if self.minSearchesLow < self.minSearchesHigh:
            self._extraSearches_ = random.randint(self.minSearchesLow,
                                              self.minSearchesHigh)

        #if High < Low pick random # of less searches to perform
        else:
            self._extraSearches_ = random.randint(self.minSearchesHigh,
                                                self.minSearchesLow) * -1

        self._minSearches_ = 30
        self._startDelay_ = random.randint(self.startDelayLow,
                                        self.startDelayHigh)
        self._wordList_ = []
        self._pointsRemaining_ = 1
        self._startingPoints_ = 0

        super(Mobile, self).__init__(email, password)

    #---------------------------------------------------------------------------

    def logout(self, browser):
        """Logs out of a mobile bing account"""
        browser.get("http://www.bing.com")
        time.sleep(1)
        finalPoints = self.get_account_points(browser)
        self.save_points(finalPoints)
        print "%d points earned"\
            %(finalPoints - self._startingPoints_)

        self.goal_check(browser)

        browser.get("http://www.bing.com/rewards/dashboard")
        browser.find_element_by_xpath('//*[@id="mbHeader"]/a[2]/img').click()
        time.sleep(2)

        for i in range(4):
            try:
                AccountMenu = browser.find_element_by_xpath('//*[@id="Account"]').click()
                time.sleep(2)
                browser.find_element_by_xpath('//*[@id="Account_menu"]/a[5]/li').click()
                break
            except selenium.common.exceptions.ElementNotVisibleException:
                i += 1


    #---------------------------------------------------------------------------

    def get_multiplier(self, browser):
        """calls the Bing Account get_multiplier function, while passing
        the appropriate search string for the mobile class"""
        super(Mobile, self).get_multiplier(browser, "Mobile search-")

    #---------------------------------------------------------------------------

    def get_points(self, browser):
        super(Mobile, self).get_points(browser, "Mobile search-")

    def login(self, url, browser):
        super(Mobile, self).login(url, browser)
        time.sleep(0.5)
        browser.get("http://www.bing.com")
        time.sleep(0.5)