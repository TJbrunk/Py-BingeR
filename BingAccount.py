#-------------------------------------------------------------------------------
# Name:        Bing Account Class
# Purpose:
#
# Author:      TBrink
#
# Created:     25/09/2014
# Copyright:   (c) TBrink 2014
# Licence:     GPL2
#-------------------------------------------------------------------------------

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random #import randint

class BingAccount(object):

    def __init__(self, email, password):
        self.email = email
        self.password = password

    #---------------------------------------------------------------------------

    def login(self, URL, browser):
        """Log's in to Outlook account"""
        print "Start delay %d seconds. \t" %(self._startDelay_),
        time.sleep(self._startDelay_)
        browser.get(URL)
        time.sleep(5)
        print "Logging in as " + self.email
        emailField = browser.find_element_by_name('login')
        emailField.send_keys(self.email)
        passwordField = browser.find_element_by_name('passwd')
        passwordField.send_keys(self.password)
        passwordField.submit()
        #reset the browser
        browser.get('http://www.bing.com')
        time.sleep(3)

        self._startingPoints_ = self.get_account_points(browser)
        print "%s currently has %d points" %(self.email, self._startingPoints_)

    #---------------------------------------------------------------------------

    def generate_word_list(self):
        """Generates a random list of words from the words.txt file"""
        f = open('words.txt')
        words = f.readlines()
        for i in range(self._minSearches_):
            self._wordList_.append(words[random.randint(0,109581)].rstrip())
        f.close()

    #---------------------------------------------------------------------------

    def search(self, browser):
        """Performs Minimum number of defined searches"""
        print "Starting %d searches" % (self._minSearches_)
        for i in range(self._minSearches_):
            browser.get("http://www.bing.com")
       	    time.sleep(3)
    	    searchField = browser.find_element_by_name('q')
    	    searchField.send_keys(self._wordList_[i] + Keys.RETURN)
            #print"searching for: " + self._wordList_[i]
            print i,
            waitTime = random.randint(self.searchWaitShort, self.searchWaitLong)
            #print "Waiting %d seconds" %(waitTime)
    	    time.sleep(waitTime)

    #------------------------------------------------------------------------------

    def get_points(self, browser):
        """Gets the available points for the account"""

        if self.__class__.__name__ == "Desktop":
            searchString = "PC search-"
        elif self.__class__.__name__ == "Mobile":
            searchString = "Mobile search-"
        else:
            print "Can't determine class type"
            return

        #Go to bing Fly Out page: (Details about point accumluated today:
        browser.get('http://www.bing.com/rewardsapp/bepflyoutpage')
        time.sleep(7)
        #print "Calculating points available to redeem"
        #All offers on the flyout page are of class = offertitle
        offers = browser.find_elements_by_class_name('offertitle')

        #should be minumum of 3 offers: 1-Daily bonuses, 2-PC searches, 3-Mobile searches
        for offer in offers:
            #loop through all the offers and find the #of PC searches done today

            if offer.text.find(searchString) > -1:
                #get the current points earned, and the maximum points
                current, maximum = offer.text.split('-')[1].split('of')
                current, maximum = int(current), int(maximum)
                print "%s %d of %d" %(searchString, current, maximum)
                self._pointsRemaining_ = (maximum - current)
                return
        print "Unable to determine %s points remaining" % searchString
        return

    #--------------------------------------------------------------------------

    def get_multiplier(self, browser):
        """Gets the search multiplier for the account.
        i.e. 1 point per 2 searches up to 15 points per day and calculates
        the minimum number of searches to perform"""

        if self.__class__.__name__ == "Desktop":
            searchString = "PC search-"
        elif self.__class__.__name__ == "Mobile":
            searchString = "Mobile search-"
        else:
            print "Can't determine class type in get_multiplier"
            return

        #print "Calculating minimum number of searches to perform"
        offerwrapper = browser.find_elements_by_class_name('offerwrapper')
        for offer in offerwrapper:
            if offer.find_element_by_class_name('offertitle').text.find(searchString) > -1:
                multipliers = offer.find_elements_by_tag_name('span')
                for m in multipliers:
                    if m.text.find('Earn 1 credit per ') > -1:
                        text = m.text.split()
                        nums = []
                        for t in range(len(text)):
                            try:
                                nums.append(int(text[t]))
                            except:
                                pass

                        self._minSearches_ = self._pointsRemaining_*nums[1]+self._extraSearches_
                        print "%d credit per %d searches"\
                              %(nums[0], nums[1])
                        #found what we need - return to caller
                        return None

    #---------------------------------------------------------------------------

    def get_bonus_points(self, browser):
        """Claim the daily bonus point(s)"""
        #go to the account dashboard and wait for it to load
        browser.get("http://www.bing.com/rewardsapp/bepflyoutpage")
        time.sleep(.5)

        points = False
        #get all the offer titles
        offers = browser.find_elements_by_class_name('offertitle')
        for offer in offers:
            #if the offer is to Earn points, click it
            if offer.text.find("Earn ") >-1:
                print offer.text
                offer.click()
                points = True
                break
        #if we clicked an offer, call the get_bonus_points method
        #again to check if there are any other offers to claim
        if points:
            self.get_bonus_points(browser)

    def get_account_points(self, browser):
        """Finds and returns the number of points the account currently has"""
        browser.get('http://www.bing.com')
        time.sleep(3)
        return int(browser.find_element_by_id("ir_rc").text)
        # browser.get('http://www.bing.com/rewards/dashboard')
        # time.sleep(3)
        # self._startingPoints_ = int(browser.find_element_by_class_name("credits").text)
        # print "%s currently has %d points" %(self.email, self._startingPoints_)


#*********************************MOBILE CHILDCLASS*****************************
class Mobile(BingAccount):
    """Mobile settings subclass of main Bing Accounts class"""
    def __init__(self, email, password, **kwargs):

        self.mobileEnabled = kwargs['mobileEnabled']
        self.searchWaitLong = int(kwargs['searchWaitLong'])
        self.searchWaitShort = int(kwargs['searchWaitShort'])
        self.minSearchesLow = int(kwargs['minSearchesLow'])
        self.minSearchesHigh = int(kwargs['minSearchesHigh'])
        self.startDelayLow = int(kwargs['startDelayLow'])
        self.startDelayHigh = int(kwargs['startDelayHigh'])

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
        browser.get("http://www.bing.com/rewards/dashboard")
        time.sleep(2)
        browser.find_element_by_xpath('//*[@id="mbHeader"]/a[2]/img').click()
        time.sleep(2)

        sidebar = browser.find_elements_by_tag_name("a")
        for link in sidebar:
            if link.text.find('Sign out') > -1:
                print "Logging out %s\n\n\n" % self.email
                link.click()
                return


#**********************************DESKTOP CHILDCLASS***************************
class Desktop(BingAccount):
    """Desktop settings subclass of main Bing Accounts class"""
    def __init__(self,email, password, **kwargs):

        self.pcEnabled = kwargs['pcEnabled']
        self.searchWaitLong = int(kwargs['searchWaitLong'])
        self.searchWaitShort = int(kwargs['searchWaitShort'])
        self.minSearchesLow = int(kwargs['minSearchesLow'])
        self.minSearchesHigh = int(kwargs['minSearchesHigh'])
        self.startDelayLow = int(kwargs['startDelayLow'])
        self.startDelayHigh = int(kwargs['startDelayHigh'])

        self._extraSearches_ = random.randint(self.minSearchesLow,
                                              self.minSearchesHigh)
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
        browser.get('http://www.bing.com')
        time.sleep(3)
        print "Logging out %s \n\n\n" % self.email
        browser.find_element_by_id('id_l').click()
        time.sleep(5)
        browser.find_element_by_partial_link_text('Sign out').click()
        time.sleep(5)

#*****************************LOAD ACCOUNTS FUNCTION****************************

def loadAccount(account, file='accounts.csv'):
    """Loads all Bing account objects from text file"""
    import csv
    account += 1
    #List of Keys for account objects
    keys = ['email',
                'password',
                'pcEnabled',
                'mobileEnabled',
                'searchWaitShort',
                'searchWaitLong',
                'minSearchesLow',
                'minSearchesHigh',
                'startDelayLow',
                'startDelayHigh',
                ]
    #open the accounts file, get the desired account (row) and zip the values
    #to the settings as a dict
    with open(file, 'rb') as csvfile:
        values = [a for a in csv.reader(csvfile)][account]
        return dict(zip(keys,values))