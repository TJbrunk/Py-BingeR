import csv
def loadAccount(account, file='accounts.csv'):
    """Loads all Bing account objects from text file"""
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

print loadAccount(3, "accounts.csv")
