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
import time, random, os.path
from datetime import datetime
#import random, Desktop, Mobile

class BingAccount(object):

    def __init__(self, email, password):
        self.email = email
        self.password = password

    #---------------------------------------------------------------------------

    def login(self, URL, browser):
        """Attempts to log in to Outlook account up to three times"""

        print "+"*15 + self.email + "+"*15

        print "%d second start delay" %(self._startDelay_)

        time.sleep(self._startDelay_)

        browser.get(URL)
        time.sleep(5)

        emailField = browser.find_element_by_name('login')
        emailField.send_keys(self.email)
        passwordField = browser.find_element_by_name('passwd')
        passwordField.send_keys(self.password)
        passwordField.submit()
        time.sleep(2)

    #---------------------------------------------------------------------------

    def generate_word_list(self):
        """Generates a random list of words from the words.txt file"""
        f = open(self._dir_ + '\\words.txt')
        words = f.readlines()
        for i in range(self._minSearches_):
            self._wordList_.append(words[random.randint(0,109561)].rstrip())
        f.close()

    #---------------------------------------------------------------------------

    def search(self, browser):
        """Performs Minimum number of defined searches"""
        print "Starting %d searches" % (self._minSearches_)
        for i in range(self._minSearches_):
            browser.get("http://www.bing.com")
 #      	    time.sleep(3)
    	    searchField = browser.find_element_by_name('q')
    	    searchField.send_keys(self._wordList_[i] + Keys.RETURN)
            #print"searching for: " + self._wordList_[i]
            print i,
            waitTime = random.randint(self.searchWaitShort, self.searchWaitLong)
            #print "Waiting %d seconds" %(waitTime)
    	    time.sleep(waitTime)
        print ""

    #------------------------------------------------------------------------------

    def get_points(self, browser, searchString):
        """Gets the available points for the account"""

        #Go to bing Fly Out page: (Details about point accumluated today:
        browser.get('http://www.bing.com/rewardsapp/bepflyoutpage')
        time.sleep(3)
        ##print "Calculating points available to redeem"
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

    def get_multiplier(self, browser, searchString):
        """Gets the search multiplier for the account.
        i.e. 1 point per 2 searches up to 15 points per day and calculates
        the minimum number of searches to perform"""

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
        print "All points have been collected"
        self._minSearches_ = self._extraSearches_

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

    #---------------------------------------------------------------------------

    def get_account_points(self, browser):
        """Finds and returns the number of points the account currently has"""
        browser.get('http://www.bing.com/rewards/dashboard')
        time.sleep(2)
        try:
            points = int(browser.find_element_by_id("id_rc").text)
        except:
            points = -1
        return points

    #---------------------------------------------------------------------------

    def save_points (self, points):
        """Saves the points for the given account to the points.txt file"""
        pointsFile = self._dir_ + "\\points.txt"
	if not os.path.exists(pointsFile):
	    #create file header here
	    print "Points file not found"

	#get the current date and time
        dt = datetime.now()
        #open the file and in prep for appending the new point values
        with open(pointsFile, 'a') as file:
            line =("%s \t %s \t %d \t %d \n")\
	        %(dt, self.email, self._startingPoints_,  points)
            #Write the date/time - account - starting points - points to the file
            file.write(line)

    #---------------------------------------------------------------------------

    def goal_check(self, browser):
        """Checks if the goal for the account has been met"""

        browser.get("http://www.bing.com/rewardsapp/bepflyoutpage")
        time.sleep(3)

        offers = browser.find_elements_by_class_name('offertitle')
        for offer in offers:
            #Find the offer that is the Account Goal
            if offer.text.find("Your goal") >-1:
                goal, points = offer.text.split("-")
                points, goal = points.split(' of ')
                points, goal = int(points), int(goal)

                if points >= goal:
                    print '\n' + '%' * 40
                    print "%s has reached its goal"%(self.email)
                    print '%' * 40 + '\n'
                elif points < goal:
                    remaining = goal - points
                    print "still need %d points to reach goal" % remaining
                else:
                    print "no goal found"
                break
        return

    #---------------------------------------------------------------------------

    def verify_login(self, browser):
        """Returns True if the account logged in successfully"""
        browser.get("http://account.live.com")
        time.sleep(2)

        try:
            summary = browser.find_element_by_class_name("summaryhead")
            self._startingPoints_ = self.get_account_points(browser)
            print "%d points currently" % self._startingPoints_
            return True
        except:
            return False

    #---------------------------------------------------------------------------

    def verify_logout(self, browser):
        """Returns True if the account logged out successfully"""
        browser.get("http://account.live.com")
        time.sleep(1)
        div = "+"*15
        try:
            browser.find_element_by_class_name("loginhead").text.find("Sign in")
            print div + "%s logged out" %self.email + div + "\n\n\n"
            return True
        except:
            print "Error logging out. Restarting the browser"
            print div + self.email + div +"\n\n\n"
            return False