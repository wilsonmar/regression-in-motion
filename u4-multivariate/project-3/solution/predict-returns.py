#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Example of Multivariate Linear Regression

This program demonstrates the use of pandas and statsmodel for multivariate regression.
The actual example is to predict the 1-day returns of Walmart (WMT) by using previous
days 1-day returns and the current day's 1-day return of the S&P500.
"""

import os.path
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# The Quandl package makes it easy to access market data
# It is available from https://pypi.python.org/pypi/Quandl
import quandl 

def get_data_from_quandl(qticker, 
                         start_date="2016-01-01", end_date="2016-12-31", 
                         cache=False):
    """Download data from Quandl service.
    
    Arguments:
        qticker    -- ticker in Quandl format, e.g., "WIKI/WMT"
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

wmt = get_data_from_quandl("WIKI/WMT", cache=True)
sp500 = get_data_from_quandl("YAHOO/INDEX_GSPC", cache=True)

def tidy_data(stock, benchmark):
    """Create a tidy data frame that we can use for liner regression.
    
    The data frame will have the following columns:
        stock_ret    -- 1 day return of the stock of interest (y, or dependent variable)
        bench_ret    -- 1 day return of the benchmark index (x, or independent variable)
        stock_ret_01 -- 1 day return of the benchmark index 1 day ago
        stock_ret_02 -- 1 day return of the benchmark index 2 days ago
        ...
        stock_ret_10 -- 1 day return of the benchmark index 10 days ago
        const        -- constant column of all ones
    
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
    df['stock_ret_01'] = df['stock_ret'].shift(1)
    df['stock_ret_02'] = df['stock_ret'].shift(2)
    df['stock_ret_03'] = df['stock_ret'].shift(3)
    df['stock_ret_04'] = df['stock_ret'].shift(4)
    df['stock_ret_05'] = df['stock_ret'].shift(5)
    df['stock_ret_06'] = df['stock_ret'].shift(6)
    df['stock_ret_07'] = df['stock_ret'].shift(7)
    df['stock_ret_08'] = df['stock_ret'].shift(8)
    df['stock_ret_09'] = df['stock_ret'].shift(9)
    df['stock_ret_10'] = df['stock_ret'].shift(10)
    df['const'] = 1
    return df

tidy_data = tidy_data(wmt, sp500)
tidy_data.to_csv(os.path.join("..", "data", "wmt-sp500.csv"))

def find_correlations(data):
    """Find the correlations of the dependent column against each of the independent columns.

    Arguments:
        data     -- a tidy DataFrame, with independent column stock_ret
    """
    index = [ col for col in data.columns.values if col != "stock_ret" ]
    s = pd.Series(index=index)
    for col in index:
        s[col] = data['stock_ret'].corr(data[col])
    return s

correlations = find_correlations(tidy_data)

def visualize_correlogram(correlations, stock):
    """Create a correlogram plot for each independent variable
    
    Arguments:
        correlogram -- a Series, with entries for each independent variable
        stock       -- Name of stock for the correlogram
    """

    xs = range(1, len(correlations) + 1)
    ys = correlations.values
    fig = plt.figure()
    plt.vlines(x=xs, ymin=[0], ymax=ys)
    plt.plot([0,len(xs)], [0, 0], 'k:')
    fig.suptitle('1-Day Return Correlograms')
    plt.xlabel('Independent Variable')
    plt.ylabel('Correlation')
    plt.xticks(xs, correlations.axes[0].tolist(), rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.25)


visualize_correlogram(correlations, 'WMT')
plt.savefig(os.path.join("..", 'img', 'correlogram.png'))


def visualize_data(data, stock, benchmark, axis_low=-0.1, axis_high=0.1, x='bench_ret'):
    """Create a scatter plot of the stock returns vs. the benchmark returns.
    
    Arguments:
        data      -- a tidy DataFrame, with columns stock_ret and xvar
        stock     -- name of the stock
        benchmark -- name of the benchmark index
        axis_low  -- lowest value for x and y axes (default -0.1)
        axis_high -- highest value for x and y axes (default 0.1)
        x         -- name of independent column (default 'bench_ret')
    """
    ax = data.plot(kind='scatter', x=x, y='stock_ret',
                   title='1-Day Returns',
                   xlim=(axis_low, axis_high), ylim=(axis_low, axis_high))
    ax.set_xlabel(benchmark)
    ax.set_ylabel(stock)
    ax.set_aspect(1)

visualize_data(tidy_data, 'WMT', 'WMT (1 day ago)', axis_low=-0.075, axis_high=0.075, x='stock_ret_01')
plt.savefig(os.path.join("..", 'img', 'scatter-plot.png'))


def do_linear_regression(data):
    """Perform a linear regression for stock_ret based on bench_ret and const of the DataFrame.
    
    Arguments:
        data      -- a tidy DataFrame, with columns stock_ret, bench_ret, and const
    """
    index = [ col for col in data.columns.values if col != "stock_ret" ]
    model = sm.OLS(data['stock_ret'], 
                   data[index],
                   missing='drop')
    fit = model.fit()
    return fit

fit = do_linear_regression(tidy_data)
print(fit.summary())

tidy_data2 = tidy_data[['stock_ret', 'bench_ret', 'stock_ret_01', 'const']]
fit2 = do_linear_regression(tidy_data2)
print(fit2.summary())

def visualize_3d_fit(data, fit, stock, benchmark, x1='bench_ret', x2='stock_ret_01'):
    """Create a scatter plot of the stock returns vs. the benchmark returns.
    
    Arguments:
        data      -- a tidy DataFrame, with columns stock_ret, x1 and x2
        fit       -- a linear regression model
        stock     -- name of the stock
        benchmark -- name of the benchmark index
        x1        -- name of independent column #1 (default 'bench_ret')
        x2        -- name of independent column #2 (default 'bench_ret')
    """
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(data['stock_ret'], data[x1], data[x2])
    xmin, xmax = ax.get_xlim()
    ymin, ymax = ax.get_ylim()
    xs = pd.np.arange(xmin, xmax, 0.01)
    ys = pd.np.arange(ymin, ymax, 0.01)
    xs, ys = pd.np.meshgrid(xs, ys)
    vfn = pd.np.vectorize(lambda x, y: x*fit.params[x1] + y*fit.params[x2] + fit.params['const'])
    zs = vfn(xs, ys)
    ax.plot_surface(xs, ys, zs, color='r', alpha=0.2)
    fig.suptitle('1-Day Returns of ' + stock)
    ax.set_xlabel(benchmark)
    ax.set_ylabel(stock + ' (previous)')
    ax.set_zlabel(stock)

visualize_3d_fit(tidy_data2, fit2, "WMT", "S&P 500", x1='bench_ret', x2='stock_ret_01')
plt.savefig(os.path.join("..", 'img', 'scatter-plot-3d.png'))

def visualize_single_parameter(data, fit, stock, benchmark, x='bench_ret'):
    """Create a scatter plot and linear model of the stock returns vs. a single parameter.
    
    Arguments:
        data      -- a tidy DataFrame, with columns stock_ret, bench_ret, and const
        fit       -- a linear regression result
        stock     -- name of the stock
        benchmark -- name of the benchmark index
        x         -- name of independent column to display (default 'bench_ret')
    """
    ax = data.plot(kind='scatter', x=x, y='stock_ret',
                   title='1-Day Returns')
    index = [ col for col in data.columns.values if col != "stock_ret" ]
    X_new = pd.DataFrame({})
    for col in index:
        mid = (data[col].min() + data[col].max()) / 2.0
        X_new[col] = [mid, mid]
    X_new[x] = ax.get_xlim()

    preds = fit.predict(X_new)
    plt.plot(X_new[x], preds, 'r-')
    ax.set_xlabel(benchmark)
    ax.set_ylabel(stock)

visualize_single_parameter(tidy_data2, fit2, "WMT", "S&P 500", x='bench_ret')
plt.savefig(os.path.join("..", 'img', 'lr-single-bench-rest-avg.png'))

visualize_single_parameter(tidy_data2, fit2, "WMT", "WMT (previous)", x='stock_ret_01')
plt.savefig(os.path.join("..", 'img', 'lr-single-yesterday-rest-avg.png'))

def visualize_single_isolated_parameter(data, fit, stock, benchmark, x='bench_ret'):
    """Create a scatter plot and linear model of the stock returns vs. a single parameter
    after accounting for the others.
    
    Arguments:
        data      -- a tidy DataFrame, with columns stock_ret, bench_ret, and const
        fit       -- a linear regression result
        stock     -- name of the stock
        benchmark -- name of the benchmark index
        x         -- name of independent column to display (default 'bench_ret')
    """
    index = [ col for col in data.columns.values if col != "stock_ret" ]

    X_new = pd.DataFrame({})
    for col in index:
        X_new[col] = data[col]
    X_new[x] = 0
    X_new['stock_ret'] = data['stock_ret'] - fit.predict(X_new)
    X_new[x] = data[x]
    ax = X_new.plot(kind='scatter', x=x, y='stock_ret',
                    title='1-Day Returns')

    X_new = pd.DataFrame({})
    for col in index:
        X_new[col] = [0, 0]
    X_new[x] = ax.get_xlim()
    preds = fit.predict(X_new)
    plt.plot(X_new[x], preds, 'r-')

    ax.set_xlabel(benchmark)
    ax.set_ylabel(stock)

visualize_single_isolated_parameter(tidy_data2, fit2, "WMT", "S&P 500", x='bench_ret')
plt.savefig(os.path.join("..", 'img', 'lr-isolated-bench-rest-avg.png'))

visualize_single_isolated_parameter(tidy_data2, fit2, "WMT", "WMT (previous)", x='stock_ret_01')
plt.savefig(os.path.join("..", 'img', 'lr-isolated-yesterday-rest-avg.png'))
