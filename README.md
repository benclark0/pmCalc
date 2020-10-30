# pmCalc
Script for calculating the possible move of stocks based on their options calls and puts. 

The possible move of a stock is a value based on the options calls and puts for a given stock one week in advance of close.

This script grabs stock data using the wallstreet python 3 library. It then grabs options data for 7 days in the future. It calculates expected move of the stock, then the possible move. That data is printed in the std out and also added to a file, currently hard coded at stock_em_pm_calculated.csv that will be created (or overwritten) in the working directory.  

# TODO
Create a simple CLI for users to request individual stocks on command, or provide a list of stocks.
Decrease API calls. This is very roughly coded and does way too many API calls.
Validate math for finding the closest viable strike to the stock price. If the closest strike is within a percent (currently 30 percent) of the price of the stock, that strike should be used. We'd then get that strike's bid and ask and take their mean.  Otherwise, we take the mean of bid and ask from the closest strike, determine whether or not the price is higher or lower than the closest strike and take the mean of bid and ask for that strike. if price is higher, get mean of bid and ask of strike 1 higher than closest, and if lower, get the mean and bid of strike 1 lower than closest. 
Fix date.
Create more methods.
Create unit tests for current methods. Create unit tests for new methods.
Add future calculation requests from investors. 
