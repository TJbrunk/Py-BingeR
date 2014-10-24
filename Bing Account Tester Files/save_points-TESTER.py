import csv
def save_points (self, points):
    """Saves the points for the given account to the csv file"""
    #open the account file and read in all the accounts
    with open("accounts.csv", 'r') as file:
      accounts = [a for a in csv.reader(file)]
    #find the account from the file that matches the current account
    for a in range(len(accounts)):
        #match by email address
        if accounts[a][0] == self.email:
            #replace the points column with the new points
            accounts[a][10]= points
            #stop when we get the matching account
            break
    #open the account for writing
    with open("accounts.csv", 'wb') as file:
        f = csv.writer(file)
        #Write all of the accounts back to the file
        f.writerows(accounts)


save_points('asdfqwer9@outlook.com', 999)