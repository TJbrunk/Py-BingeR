import BingAccount, random, time, os

#**********************************DESKTOP CHILDCLASS***************************
class Desktop(BingAccount.BingAccount):
    """Desktop settings subclass of main Bing Accounts class"""
    def __init__(self,email, password, **kwargs):

        self.pcEnabled = kwargs['pcEnabled']
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


        super(Desktop, self).__init__(email, password)

    #---------------------------------------------------------------------------

    def logout(self, browser):
        """Logs out of outlook account"""
        finalPoints = self.get_account_points(browser)
        self.save_points(finalPoints)
        print "%s earned %d points with desktop searches"\
            %(self.email, finalPoints - self._startingPoints_)
        self.goal_check(browser)
        browser.get('http://www.bing.com')
        time.sleep(3)
        browser.find_element_by_id('id_l').click()
        time.sleep(5)
        browser.find_element_by_partial_link_text('Sign out').click()


    #---------------------------------------------------------------------------

    def get_multiplier(self, browser):
        """calls the Bing Account get_multiplier function, while passing
        the appropriate search string for the desktop class"""
        super(Desktop, self).get_multiplier(browser, "PC search-")

    #---------------------------------------------------------------------------

    def get_points(self, browser):
        super(Desktop, self).get_points(browser, "PC search-")
