import pandas as pd
import os
import time
from datetime import datetime

from time import mktime
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import style
style.use('dark_background')

import re


# NOTE:Description of how the code works (when it isn't self evident).
# FIXME:This works, sort of, but it could be done better. (usually code written in a hurry that needs rewriting).
# BUG:There is a problem here.
# TODO:No problem, but additional code needs to be written, usually when you are skipping something.
# REF: Reference link.
# REVIEW: need review.


path = "./intraQuarter"

def Key_Stats(gather="Total Debt/Equity (mrq)"):

    # uodate the path
    statspath = path + '/_KeyStats'

    # save all the folder name as a list
    stock_list = [x[0] for x in os.walk(statspath)]

    # print(type(stock_list))

    # # peak the stock list
    # print(stock_list[0:5])

    # NOTE: set up the data frame for our dataset
    df = pd.DataFrame(columns = ['Date',
                                'Unix',
                                'Ticker',
                                'DE ratio', 
                                'Price', 
                                'stock_p_change', 
                                'SP500', 
                                'sp500_p_change',
                                'Difference',
                                'Status'])

    # sp500 data frame
    sp500_df = pd.read_csv("SP500.csv")

    # for store the name of the ticker
    ticker_list = []


    # NOTE:read all the stock brands
    for each_dir in stock_list[1:25]:
        
        # print all the dir inside each dir (get all the file names)
        each_file = os.listdir(each_dir)

        ticker = each_dir.split('\\')[1]

        # store all the ticker
        ticker_list.append(ticker)

        # starting point
        starting_stock_value = False
        starting_sp500_value = False


        # print(each_dir)
        # print(ticker)

        # time.sleep(15)

        # NOTE:if there is a file exist
        if len(each_file) > 0:

            for file in each_file:

                # strip the time from the file name
                data_stamp = datetime.strptime(file, '%Y%m%d%H%M%S.html')

                # create a time label
                unix_time = time.mktime(data_stamp.timetuple())

                
                # setup the full path for each file
                full_file_path = each_dir + '/' + file

                
                # open and read each individual html file
                source = open(full_file_path,'r').read()

                #print(source)

                try:
                    # NOTE: get the DE ratio
                    # split the source file in half and pick the second half
                    # split the second half and pick the first element
                    try:
                        value = float(source.split(gather+':</td><td class="yfnc_tabledata1">')[1].split('</td>')[0])
                    except Exception as e:
                        # source changed format
                        value = float(source.split(gather+':</td>\n<td class="yfnc_tabledata1">')[1].split('</td>')[0])
                        # print(str(e), ticker, file)

                    # NOTE: get the sp500 value based on the current unix time
                    try:
                        # format the data time style
                        sp500_date = datetime.fromtimestamp(unix_time).strftime('%Y-%m-%d')

                        # get the corresponding rows
                        row = sp500_df[sp500_df["Date"] == sp500_date]

                        # get the adjusted close value in that specific date
                        sp500_value = float(row['Adj Close'])


                    except:
                        # format the data time style go back 3 days
                        sp500_date = datetime.fromtimestamp(unix_time-259200).strftime('%Y-%m-%d')

                        # get the corresponding rows
                        row = sp500_df[sp500_df["Date"] == sp500_date]

                        # get the adjusted close value in that specific date
                        sp500_value = float(row['Adj Close'])

                        
                    # NOTE: get the stock price at that date
                    try:
                        stock_price = float(source.split('</small><big><b>')[1].split('</b></big>')[0])
                        # print(stock_price)

                    except Exception as e:
                        # FIXME: <span id="yfs_l10_abc">43.05</span>
                        try:
                            stock_price = (source.split('</small><big><b>')[1].split('</b></big>')[0])
                            stock_price = re.search(r'(\d{1,8}\.\d{1, 8})', stock_price)
                            stock_price = float(stock_price.group(1))

                            # print(stock_price)
                            # time.sleep(15)
                        except Exception as e:
                            # FIXME: <span class="time_rtq_ticker"><span id="yfs_l84_a">43.04</span></span>
                            # stock_price = (source.split('<span class="time_rtq_ticker">')[1].split('</span>')[0])
                            # stock_price = re.search(r'(\d{1,8}\.\d{1, 8})', stock_price)
                            # stock_price = float(stock_price.group(1))
                            pass
                            

                    # record the previous value
                    if not starting_stock_value:
                        starting_stock_value = stock_price

                    if not starting_sp500_value:
                        starting_sp500_value = sp500_value

                    # NOTE: percentage of change
                    stock_p_change = ((stock_price - starting_stock_value) / starting_stock_value) * 100
                    sp500_p_change = ((sp500_value - starting_sp500_value) / starting_sp500_value) * 100


                    difference = stock_p_change - sp500_p_change

                    if difference > 0:
                        status = 1
                    else:
                        status = 0

                    # print(value)
                    # print the ticker and stock price
                    # print('Stock price: ', stock_price, 'Ticker: ', ticker)
                    # print('##########################')

                    # NOTE: update the data frame
                    df = df.append({'Date':data_stamp, 
                                    'Unix':unix_time, 
                                    'Ticker':ticker, 
                                    'DE ratio':value, 
                                    'Price':stock_price, 
                                    'stock_p_change':stock_p_change, 
                                    'SP500': sp500_value, 
                                    'sp500_p_change':sp500_p_change,
                                    'Difference':difference,
                                    'Status': status}, ignore_index=True)

                    # # print the information
                    # print(full_file_path)
                    # print(data_stamp)
                    # print(ticker + ': ', value)

                except Exception as e:
                    # if there is no value just pass
                    pass


    # NOTE: Plot different tickers
    for each_ticker in ticker_list:
        
        plot_df = df[df['Ticker'] == each_ticker]
        plot_df = plot_df.set_index(['Date'])

        try:
            if plot_df['Status'][-1] == 0:
                color = 'r'
            else:
                color = 'g'

            plot_df['Difference'].plot(label = each_ticker, color = color)
            plt.legend()
        except Exception as e:
            print(str(e))

    plt.show()

    # NOTE: save the file in csv
    # # file name to save         
    # save = gather.replace(' ','').replace(')','').replace('(','').replace('/','') + str('.csv')

    # print(save)

    # # save the data frame
    # df.to_csv(save)

    # # time.sleep(15)         

            
# REVIEW: Main function
Key_Stats()