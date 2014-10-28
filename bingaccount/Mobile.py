import BingAccount, random, time

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

        self._dir_ = kwargs['workingDir']

        self._extraSearches_ = random.randint(self.minSearchesLow,
                                              self.minSearchesHigh)
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
        finalPoints = self.get_account_points(browser)
        self.save_points(finalPoints)
        print "%d points earned with mobile searches"\
            %(finalPoints - self._startingPoints_)
		browser.get("http://www.bing.com/rewards/dashboard")
        browser.find_element_by_xpath('//*[@id="mbHeader"]/a[2]/img').click()
        time.sleep(2)

        sidebar = browser.find_elements_by_tag_name("a")
        for link in sidebar:
            if link.text.find('Sign out') > -1:
                print "Logging out %s\n\n\n" % self.email
                link.click()
                return
        browser.get("http://www.google.com")
        time.sleep(3)

    #---------------------------------------------------------------------------

    def get_multiplier(self, browser):
        """calls the Bing Account get_multiplier function, while passing
        the appropriate search string for the mobile class"""
        super(Mobile, self).get_multiplier(browser, "Mobile search-")

    #---------------------------------------------------------------------------

    def get_points(self, browser):
        super(Mobile, self).get_points(browser, "Mobile search-")
