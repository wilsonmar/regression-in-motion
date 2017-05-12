#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Example of Polynomial Regression

This program demonstrates the use of pandas and statsmodel for polynomial regression.
The actual example is to fit the growth of the federal budget over 50 years.
"""

import os.path
import math
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt

from statsmodels.sandbox.regression.predstd \
    import wls_prediction_std

data = pd.read_csv("us-federal-debt.csv", sep=",\s*", engine='python')

def tidy_data(data):
    """Create a tidy data frame that we can use for liner regression.
    
    The data frame will have the following columns:
        debt -- the original debt column
        x0   -- constant column of all 1s
        x1   -- original x data
        x2   -- x^2
        x3   -- x^3
    
    Arguments:
        data -- DataFrame containing 'Year' and 'Debt' columns
    """
        
    df = pd.DataFrame(index=data.index)
    df['debt'] = data['Debt']
    df['x0'] = 1
    df['x1'] = data['Year'] - min(data['Year']) + 1.0
    df['x2'] = df['x1'] * df['x1']
    df['x3'] = df['x2'] * df['x1']
    return df

tidy_data = tidy_data(data)

def visualize_data(data):
    """Create a line plot of the debt vs. year.
    
    Arguments:
        data      -- a tidy DataFrame, with columns stock_ret and xvar
    """
    ax = data.plot(kind='line', x='x1', y='debt',
                   title='US National Debt')
    ax.set_xlabel('Year')
    ax.set_ylabel('Debt')

visualize_data(tidy_data)
plt.savefig(os.path.join("..", 'line-plot.png'))

def do_linear_regression(data):
    """Perform a linear regression for stock_ret based on bench_ret and const of the DataFrame.
    
    Arguments:
        data      -- a tidy DataFrame, with response column debt, and predictor columns xi
    """
    index = [ col for col in data.columns.values if col != "debt" ]
    model = sm.OLS(data['debt'], 
                   data[index],
                   missing='drop')
    fit = model.fit()
    return fit

fit = do_linear_regression(tidy_data)
print(fit.summary())

def visualize_linear_regression(data, fit, show_std=False):
    """Create a line plot and linear model of the response variable ('debt') vs. predictor variable ('x1').
    
    Arguments:
        data      -- a tidy DataFrame, with response column debt, and predictor columns xi
        fit       -- a linear regression result
        show_std  -- whether to show upper and lower bands around answer (default False)
    """
    ax = data.plot(kind='line', x='x1', y='debt',
                   title=('US National Debt'))
    x = pd.np.linspace(min(data['x1']), max(data['x1']))
    X_new = pd.DataFrame()
    X_new['x0'] = [1] * len(x)
    X_new['x1'] = x
    X_new['x2'] = X_new['x1'] * X_new['x1']
    X_new['x3'] = X_new['x2'] * X_new['x1']
    preds = fit.predict(X_new)
    plt.plot(x, preds, 'r--')

    if show_std:
        _, lower, upper = wls_prediction_std(fit, X_new)
        plt.plot(x, lower, 'r:', 
                 x, upper, 'r:')
    ax.set_xlabel('Year')
    ax.set_ylabel('Debt')

visualize_linear_regression(tidy_data, fit)
plt.savefig(os.path.join("..", 'nonlinear-plot-without-errors.png'))

visualize_linear_regression(tidy_data, fit, show_std=True)
plt.savefig(os.path.join("..", 'nonlinear-plot-with-errors.png'))

