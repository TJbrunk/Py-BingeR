import csv


#*****************************LOAD ACCOUNTS FUNCTION****************************


def loadAccount(account, f):
    """Loads the specified Bing account object from csv file"""
 #   account += 1
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
                'workingDir',
                ]
    #open the accounts file, get the desired account (row) and zip the values
    #to the settings as a dict
    with open(f, 'rb') as csvfile:
        values = [a for a in csv.reader(csvfile)][account]
 #       values.append(folder)
        kwargs = dict(zip(keys,values))
        return kwargs