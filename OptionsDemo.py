# -*- coding: utf-8 -*-
"""
@author: mhna
"""

import pandas as pd
import numpy as np
from dateutil.parser import parse
from datetime import timedelta, datetime
import math
import QuantLib as ql


def findClosestDate(end_date, date_index, before = 1):
    if end_date in date_index:
        print end_date
    elif (end_date > max(date_index)) or (end_date < min(date_index)):
        print 'WARNING: End date outside the historic data range'
    elif before == 1:
        for i in range(-1,-10,-1):
            if end_date in date_index: break
            end_date = end_date - timedelta(1)
    else:
        for i in range(1,10,1):
            if end_date in date_index: break
            end_date = end_date + timedelta(1)

    return end_date



class Underlyer():
    def __init__(self, value):
        self.name = value

    def getSpot(self, hist_file = 'C:\Users\mhna\Documents\Python\RiskLab\sa\HistPrices.csv'):
        hist_prices = pd.read_csv(hist_file, parse_dates =True, dayfirst = True, index_col = 'Index')
        last_date = max(hist_prices.index)
        self.spot = hist_prices.ix[last_date, self.name]

        return self.spot

    def setSpot(self, value):
        self.spot = value

    def getVol(self, strike = 1, tenor = 1, strike_type = 'pct', hist_file = 'C:\Users\mhna\Documents\Python\RiskLab\sa\VolParameters.csv'):
        vol_params = pd.read_csv(hist_file, index_col = 'Underlyer')
        atm_vol = vol_params.ix[self.name].ATMVol
        skew = vol_params.ix[self.name].Skew

        if strike_type == 'pct':
            strike == strike
        else:
            strike == strike/self.getSpot()

        if strike <= 1:
            convexity = vol_params.ix[self.name].PutConvexity
        else:
            convexity = vol_params.ix[self.name].CallConvexity

        flatBelow = vol_params.ix[self.name].FlatVolsBelow
        flatAbove = vol_params.ix[self.name].FlatVolsAbove
        cap = vol_params.ix[self.name].CappedAt
        floor = vol_params.ix[self.name].FlooredAt

        strike_vol = min(cap, max(floor, atm_vol + (1- max(flatBelow, min(flatAbove,strike)))/0.1 * skew /math.sqrt(tenor) + ((1-max(flatBelow, min(flatAbove, strike)))/0.1)**2 * convexity / tenor))
        return strike_vol


    def getHistPrices(self, valueDate, numObservations = 1, dayfirst = True, hist_file = 'C:\Users\mhna\Documents\Python\RiskLab\sa\HistPrices.csv'):
        hist_prices = pd.read_csv(hist_file, parse_dates =True, dayfirst = True, index_col = 'Index')
        end_date = parse(valueDate, dayfirst = dayfirst)
        #print end_date.month
        end_date_n = findClosestDate(end_date,hist_prices.index)
        if end_date_n != end_date:
            print 'WARNING: Specified date is not a good day. Using ' + str(end_date_n)
        #print end_date_n.month
        ul_hist = hist_prices.ix[:end_date_n][self.name]
        ul_hist_prices = ul_hist[-numObservations:]
        if end_date_n - timedelta(numObservations) < min(hist_prices.index):
            print 'WARNING: Period start date is outside the range of available dates. \nDisplaying max available data.'

        return ul_hist_prices



class Instrument():
    def __init__(self, value, inst_type):
        self.name = value
        self.type = inst_type

    def PV(self):
        #calculate PV
        return 0

    def setPrice(self, price):
        self.PV = price
        return self.PV

class Stocks(Instrument):
    def __init__(self, value):
        self.name = value

    def PV(self):
        stock_ul = Underlyer(self.name)
        self.PV = stock_ul.getSpot()
        return self.PV

class Options(Instrument):
    def __init__(self):
        print 'Option'




class EuropeanOption(Options):
    def __init__(self, underlyer, opt_type, opt_strike, opt_maturity):
        self.underlyer = underlyer
        if opt_type.upper() == 'CALL':
            self.opt_type = ql.Option.Call
        elif opt_type.upper() == 'PUT':
            self.opt_type = ql.Option.Put
        else:
            print opt_type +' is an incorrect option type'

        self.strike = opt_strike
        self.maturity = opt_maturity
        self.name = underlyer+opt_type+str(opt_strike)+str(opt_maturity)

    def PV(self, SpotOverRide = None, VolOverRide = None, VolOverRideType = 'shock'):
        ul = Underlyer(self.underlyer)

        if SpotOverRide != None:
            current_spot = SpotOverRide
        else:
            current_spot = ul.getSpot()

        spot = ql.SimpleQuote(current_spot)
        maturity_date = parse(self.maturity)
        day = maturity_date.day
        month = maturity_date.month
        year = maturity_date.year
        val_date = ql.Date(datetime.now().day,datetime.now().month,datetime.now().year)
        expiry = ql.Date(day, month,year)

        if VolOverRide != None:
            if VolOverRideType.upper() == 'SHOCK':
                strike_vol = ul.getVol(self.strike,tenor = (expiry - val_date), strike_type = 'abs')+VolOverRide
            else:
                strike_vol = VolOverRide
        else:
            strike_vol = ul.getVol(self.strike,tenor = (expiry - val_date), strike_type = 'abs')

        sigma = ql.SimpleQuote(strike_vol)
        r = ql.SimpleQuote(0.025)

        option = ql.EuropeanOption(ql.PlainVanillaPayoff(self.opt_type,self.strike),ql.EuropeanExercise(expiry))

        riskFreeCurve = ql.FlatForward(0,ql.TARGET(),ql.QuoteHandle(r),ql.Actual360())
        volatility = ql.BlackConstantVol(0,ql.TARGET(), ql.QuoteHandle(sigma),ql.Actual360())
        process = ql.BlackScholesProcess(ql.QuoteHandle(spot),ql.YieldTermStructureHandle(riskFreeCurve),ql.BlackVolTermStructureHandle(volatility))
        engine = ql.AnalyticEuropeanEngine(process)

        option.setPricingEngine(engine)
        return option.NPV()


option1 = EuropeanOption('XOM','put',72,'25/12/2015')

print option1.PV()

print option1.PV(SpotOverRide=70, VolOverRide = 0.40)

spotRange = np.linspace(-.10,.10,5)
volRange = np.linspace(-0.05,0.05,3)

optionPV = []
for j in volRange:
    spotLadder = []
    for i in spotRange:
        spot = Underlyer(option1.underlyer).getSpot()
        spotLadder.append(option1.PV(SpotOverRide = spot*(1+i), VolOverRide = j))
    optionPV.append(spotLadder)

print optionPV

