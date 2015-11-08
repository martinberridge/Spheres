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

# HIST_FILE = 'C:\Users\mhna\Documents\Python\RiskLab\sa\HistPrices.csv'
# VOL_FILE =  'C:\Users\mhna\Documents\Python\RiskLab\sa\VolParameters.csv'
HIST_FILE = '~/Downloads/HistPrices.csv'
VOL_FILE = '~/Downloads/VolParameters.csv'

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


class EquityMarketData(object):

    def __init__(self):
        self.hist_file = HIST_FILE
        self.hist_prices = None

    def get_spot(self,ticker):
        if self.hist_prices is None:
           self.hist_prices = pd.read_csv(self.hist_file, parse_dates =True, dayfirst = True, index_col = 'Index')

        last_date = max(self.hist_prices.index)

        self.spot = float(self.hist_prices.ix[last_date, ticker])

        return self.spot

class OptionMarketData(object):

    def __init__(self):
        self.vol_file = VOL_FILE
        self.vol_params = None

    def get_vol(self, ticker, spot,strike = 1.0, tenor = 1.0, strike_type = 'pct'):
        if  self.vol_params is None :
           self.vol_params = pd.read_csv(self.vol_file, index_col = 'Underlyer')

        atm_vol = self.vol_params.ix[ticker].ATMVol
        skew = self.vol_params.ix[ticker].Skew

        if strike_type != 'pct':
            strike == strike/float(spot)

        if strike <= 1:
            convexity = self.vol_params.ix[ticker].PutConvexity
        else:
            convexity = self.vol_params.ix[ticker].CallConvexity

        flatBelow = self.vol_params.ix[ticker].FlatVolsBelow
        flatAbove = self.vol_params.ix[ticker].FlatVolsAbove
        cap = self.vol_params.ix[ticker].CappedAt
        floor = self.vol_params.ix[ticker].FlooredAt

        strike_vol = min(cap, max(floor, atm_vol + (1- max(flatBelow, min(flatAbove,strike)))/0.1 * skew /math.sqrt(tenor) + ((1-max(flatBelow, min(flatAbove, strike)))/0.1)**2 * convexity / tenor))
        return strike_vol


class RatesMarket(object):

    def get_spot(self):
        return 0.025

class OptionsMarket(object):

    def __init__(self,ticker, market_data):
        self.ticker = ticker
        self.market_data = market_data
        self._tweak = 0.0

    def tweak(self):
        return self._tweak

    def get_vol(self, strike = 1, tenor = 1, strike_type = 'pct'):
        return self.market_data.get_vol(self.ticker,spot,strike,tenor,strike_type) + self.tweak()



class EquityMarket(object):

    def __init__(self,ticker, market_data):
        self.ticker = ticker
        self.market_data = market_data
        self._tweak = 0.0

    def tweak(self):
        return self._tweak

    def get_spot(self):
        return self.market_data.get_spot(self.ticker) + self.tweak()


class Underlyer():
    def __init__(self, value):
        self.name = value
        self.vol_file = VOL_FILE
        self.vol_params = None
        self.equity_market_data = EquityMarketData()
        self.option_market_data = OptionMarketData()
        self.spot = None
        self.vol = None

    def getSpot(self):
        if self.spot is None:
           self.spot = self.equity_market_data.get_spot(self.name)
        return self.spot

    def setSpot(self, value):
        self.spot = value

    def getVol(self, strike = 1, tenor = 1, strike_type = 'pct'):

        if self.vol is None:
           self.vol = self.option_market_data.get_vol(self.name,self.equity_market_data.get_spot(self.name),strike, tenor, strike_type)
        return self.vol

    # def getHistPrices(self, valueDate, numObservations = 1, dayfirst = True, hist_file = HIST_FILE):
    #     hist_prices = pd.read_csv(hist_file, parse_dates =True, dayfirst = True, index_col = 'Index')
    #     end_date = parse(valueDate, dayfirst = dayfirst)
    #     #print end_date.month
    #     end_date_n = findClosestDate(end_date,hist_prices.index)
    #     if end_date_n != end_date:
    #         print 'WARNING: Specified date is not a good day. Using ' + str(end_date_n)
    #     #print end_date_n.month
    #     ul_hist = hist_prices.ix[:end_date_n][self.name]
    #     ul_hist_prices = ul_hist[-numObservations:]
    #     if end_date_n - timedelta(numObservations) < min(hist_prices.index):
    #         print 'WARNING: Period start date is outside the range of available dates. \nDisplaying max available data.'
    #
    #     return ul_hist_prices





# class Instrument():
#     def __init__(self, value, inst_type):
#         self.name = value
#         self.type = inst_type
#
#     def PV(self):
#         #calculate PV
#         return 0
#
#     def setPrice(self, price):
#         self.PV = price
#         return self.PV
#
# class Stocks(Instrument):
#     def __init__(self, value):
#         self.name = value
#
#     def PV(self):
#         stock_ul = Underlyer(self.name)
#         self.PV = stock_ul.getSpot()
#         return self.PV
#
# class Options(Instrument):
#     def __init__(self):
#         print 'Option'


#class EuropeanOption(Options):

class EuropeanOption(object):
    def __init__(self, equity_market, options_market,rates_market, opt_type, opt_strike, opt_maturity):

        self.equity_market = equity_market
        self.options_market = options_market
        self.rates_market = rates_market

        if opt_type.upper() == 'CALL':
            self.opt_type = ql.Option.Call
        elif opt_type.upper() == 'PUT':
            self.opt_type = ql.Option.Put
        else:
            print opt_type +' is an incorrect option type'

        self.strike = opt_strike
        self.maturity = opt_maturity
        self.name = equity_market.ticker+opt_type+str(opt_strike)+str(opt_maturity)

    def PV(self, SpotOverRide = None, VolOverRide = None, VolOverRideType = 'shock'):

        if SpotOverRide != None:
            current_spot = SpotOverRide
        else:
            current_spot = self.equity_market.get_spot()

        spot = ql.SimpleQuote(current_spot)
        maturity_date = parse(self.maturity)
        day = maturity_date.day
        month = maturity_date.month
        year = maturity_date.year
        val_date = ql.Date(datetime.now().day,datetime.now().month,datetime.now().year)
        expiry = ql.Date(day, month,year)

        if VolOverRide != None:
            if VolOverRideType.upper() == 'SHOCK':
                strike_vol = self.options_market.get_vol(self.strike,tenor = (expiry - val_date), strike_type = 'abs')+VolOverRide
            else:
                strike_vol = VolOverRide

        else:
            strike_vol = self.options_market.get_vol(self.strike,tenor = (expiry - val_date), strike_type = 'abs')

        sigma = ql.SimpleQuote(strike_vol)
        r = ql.SimpleQuote(self.rates_market.get_spot())

        option = ql.EuropeanOption(ql.PlainVanillaPayoff(self.opt_type,self.strike),ql.EuropeanExercise(expiry))

        riskFreeCurve = ql.FlatForward(0,ql.TARGET(),ql.QuoteHandle(r),ql.Actual360())
        volatility = ql.BlackConstantVol(0,ql.TARGET(), ql.QuoteHandle(sigma),ql.Actual360())
        process = ql.BlackScholesProcess(ql.QuoteHandle(spot),ql.YieldTermStructureHandle(riskFreeCurve),ql.BlackVolTermStructureHandle(volatility))
        engine = ql.AnalyticEuropeanEngine(process)

        option.setPricingEngine(engine)
        return option.NPV()


emd = EquityMarketData()
omd = OptionMarketData()
em = EquityMarket("XOM",emd)
om = OptionsMarket("XOM",omd)
rm = RatesMarket()

spot = em.get_spot()
print spot
print om.get_vol(spot)

option1 = EuropeanOption(em,om,rm,'put',72,'25/12/2015')

print option1.PV()

print option1.PV(SpotOverRide=70, VolOverRide = 0.40)

spotRange = np.linspace(-.10,.10,5)
volRange = np.linspace(-0.05,0.05,3)

optionPV = []
for j in volRange:
    spotLadder = []
    spot  = em.get_spot()
    for i in spotRange:
        spotLadder.append(option1.PV(SpotOverRide = spot*(1+i), VolOverRide = j))
    optionPV.append(spotLadder)


print optionPV

