#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      TBrink
#
# Created:     25/09/2014
# Copyright:   (c) TBrink 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from BingAccount import Desktop
#import jsonpickle
#import yaml



acc2 = Desktop(email = 'TYLER@gmail.com',
                    password = "PASSWORD",
                    pcEnabled = False,
                    mobileEnabled = False,
                    )
print type(acc2)
##acc2.append(BingAccount(email = 'LEVI@gmail.com',
##                    password = "Pwd",
##                    desktop = False,
##                    mobile = False,
##                    DwaitLong = 10,
##                    DwaitShort = 20,
##                    DnumSearches = 200,
##                    MwaitLong = 10,
##                    MwaitShort = 20,
##                    MnumSearches = 200,
##                    ))
##for a in acc2:
##    a.saveAccount()
#    print a.desktop, a.mobile
print acc2.__class__.__name__

#loadAccount()
##print acc2.email
##print acc2.password
##print acc2.desktop.waitLong
#print acc2.MwaitLong
