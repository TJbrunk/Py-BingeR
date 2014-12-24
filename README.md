Python Bing Rewards bot
Py-BingeR
=========

Python code to collect Bing points by performing desktop and mobile searches


Getting Started
==========
Delete the example account in the accounts file, then add all of your accounts to the file; leaving the header row.
You can add as many or few accounts as you want.
RUn Main.py, and Py-BingeR will go through all of the accounts collecting PC and Mobile search points as defined in the accounts file.
Py-BingeR will also collect daily offer bonus points for each account




accounts.csv settings:
==========
The accounts.csv file holds all the account information and search parameters for each of your accounts. It's easiest to edit the file in Excel, but be sure to only save it as a csv.

1st column: Full email address ie example@outlook.com

2nd column: Password for the account. (Enter it the exact way you'd enter it on the website)

3rd column: Enter "TRUE" (all caps no quotes) if you want Py-BingeR to perform PC searches 

4th column: Enter "TRUE" (all caps no quotes) if you want Py-BingeR to perform Mobile searches
	NOTE: If you enter anything besides TRUE in columns 3 or 4 those searches won't be performed

5th column: The minimum time (in seconds) that Py-BingeR will wait between bing searches

6th column: The maximum time (in seconds) that Py-BingeR will wait between bing searches

NOTE: Py-BingeR automatically calculates the minimum number of searches an account needs to perform based on the maximum number of points the account can earn in a day, and how many searches need to be done to earn 1 point

7th column: The minimum number of searches Py-BingeR will perform, beyond the searches needed to earn all the available points

8th column: The maximum number of searches Py-BingeR will perform, beyond the searches needed to earn all the available points

9th column: Minimum time (in seconds) that Py-BingeR will wait before logging into the bing account

10th column: Maximum time (in seconds) that Py-BingeR will wait before logging into the bing account