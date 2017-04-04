#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Example of Linear Regression

This program demonstrates the use of statsmodel linear regression.
The actual example is to compute alpha and beta for AAPL stock,
relative to the S&P500 average.
"""

import os.path
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt

from statsmodels.sandbox.regression.predstd \
    import wls_prediction_std

# The Quandl package makes it easy to access market data
# It is available from https://pypi.python.org/pypi/Quandl
import quandl 

def get_data_from_quandl(qticker, 
                         start_date="2016-01-01", end_date="2016-12-31", 
                         cache=False):
    """Download data from Quandl service.
    
    Arguments:
        qticker    -- ticker in Quandl format, e.g., "WIKI/AAPL"
        start_date -- first date to retrieve (default "2016-01-01")
        end_date   -- last date to retrieve (default "2016-12-31")
        cache      -- True if local cache should be used (default False)
    """
    base, ticker = qticker.split("/")
    fname = os.path.join("..", "data", "cache", ticker + ".csv")
    if cache and os.path.isfile(fname):
        data = pd.read_csv(fname, index_col=0)
        return data
    data = quandl.get(qticker,
                      start_date=start_date, end_date=end_date)
    data.to_csv(fname)
    return data

aapl = get_data_from_quandl("WIKI/AAPL", cache=True)
sp500 = get_data_from_quandl("YAHOO/INDEX_GSPC", cache=True)

def visualize_raw_data(stock, benchmark, stock_name, benchmark_name):
    """Create a line chart of the stock and the benchmark.
    
    Arguments:
        stock     -- DataFrame of the stock of interest, must have 'Adj. Close' column
        benchmark -- DataFrame of the benchmark index, must have 'Adjusted Close' column
    """
    df = pd.merge(aapl[['Adj. Close']], sp500[['Adjusted Close']], left_index=True, right_index=True)
    df.rename(columns={'Adj. Close': stock_name, 'Adjusted Close': benchmark_name}, inplace=True)
    ax = df.plot(kind='line', secondary_y=[benchmark_name], title='Raw Data')
    ax.set_xlabel('Date')
    ax.set_ylabel(stock_name)
    ax.right_ax.set_ylabel(benchmark_name)

visualize_raw_data(aapl, sp500, 'AAPL', 'S&P 500')
plt.savefig(os.path.join("..", 'img', 'raw-data-plot.png'))


def tidy_data(stock, benchmark):
    """Create a tidy data frame that we can use for liner regression.
    
    The data frame will have the following columns:
        stock_ret -- 1 day return of the stock of interest (y, or dependent variable)
        bench_ret -- 1 day return of the benchmark index (x, or independent variable)
        const     -- constant column of all ones
    
    Arguments:
        stock     -- DataFrame of the stock of interest, must have 'Adj. Close' column
        benchmark -- DataFrame of the benchmark index, must have 'Adjusted Close' column
    
    Note: The 'Adj.' vs. 'Adjusted' convention preserves the Quandl naming convention
    for WIKI stock database, vs. YAHOO index database
    """
    def compute_returns(s):
        """Compute 1-day returns of a time series of non-negative values.
        
        Arguments:
            s -- a Series of raw data
        """
        today, yesterday = s, s.shift(1)
        return (today - yesterday) / yesterday
        
    df = pd.DataFrame(index=stock.index)    
    df['stock_ret'] = compute_returns(stock['Adj. Close'])
    df['bench_ret'] = compute_returns(benchmark['Adjusted Close'])
    df['const'] = 1
    return df

tidy_data = tidy_data(aapl, sp500)
tidy_data.to_csv(os.path.join("..", "data", "aapl-sp500.csv"))

def visualize_data(data, stock, benchmark, axis_low=-0.1, axis_high=0.1):
    """Create a scatter plot of the stock returns vs. the benchmark returns.
    
    Arguments:
        data      -- a tidy DataFrame, with columns stock_ret and bench_ret
        stock     -- name of the stock
        benchmark -- name of the benchmark index
        axis_low  -- lowest value for x and y axes (defult -0.1)
        axis_high -- highest value for x and y axes (defult 0.1)
    """
    ax = data.plot(kind='scatter', x='bench_ret', y='stock_ret',
                   title='1-Day Returns',
                   xlim=(axis_low, axis_high), ylim=(axis_low, axis_high))
    ax.set_xlabel(benchmark)
    ax.set_ylabel(stock)
    ax.set_aspect(1)

visualize_data(tidy_data, 'AAPL', 'S&P 500', axis_low=-0.075, axis_high=0.075)
plt.savefig(os.path.join("..", 'img', 'scatter-plot.png'))

def do_linear_regression(data):
    """Perform a linear regression for stock_ret based on bench_ret and const of the DataFrame.
    
    Arguments:
        data      -- a tidy DataFrame, with columns stock_ret, bench_ret, and const
    """
    model = sm.OLS(data['stock_ret'], 
                   data[['bench_ret', 'const']],
                   missing='drop')
    fit = model.fit()
    return fit

fit = do_linear_regression(tidy_data)

def visualize_linear_regression(data, fit, stock, benchmark, axis_low=-0.1, axis_high=0.1, show_std=False):
    """Create a scatter plot and linear model of the stock returns vs. the benchmark returns.
    
    Arguments:
        data      -- a tidy DataFrame, with columns stock_ret, bench_ret, and const
        fit       -- a linear regression result
        stock     -- name of the stock
        benchmark -- name of the benchmark index
        axis_low  -- lowest value for x and y axes (defult -0.1)
        axis_high -- highest value for x and y axes (defult 0.1)
        show_std  -- whether to show upper and lower bands around answer (default False)
    """
    ax = data.plot(kind='scatter', x='bench_ret', y='stock_ret',
                   title='1-Day Returns',
                   xlim=(axis_low, axis_high), ylim=(axis_low, axis_high))
    X_new = pd.DataFrame({'bench_ret': [axis_low, axis_high]})
    X_new['const'] = 1
    preds = fit.predict(X_new)
    plt.plot(X_new['bench_ret'], preds, 'r-')
    if show_std:
        _, lower, upper = wls_prediction_std(fit, X_new)
        plt.plot(X_new['bench_ret'], lower, 'r--', 
                 X_new['bench_ret'], upper, 'r--')
    ax.set_xlabel(benchmark)
    ax.set_ylabel(stock)
    ax.set_aspect(1)


visualize_linear_regression(tidy_data, fit, 'AAPL', 'S&P 500', axis_low=-0.075, axis_high=0.075)
plt.savefig(os.path.join("..", 'img', 'lr-plot-without-errors.png'))

visualize_linear_regression(tidy_data, fit, 'AAPL', 'S&P 500', axis_low=-0.075, axis_high=0.075, show_std=True)
plt.savefig(os.path.join("..", 'img', 'lr-plot-with-errors.png'))
