# -*- coding: utf-8 -*-
"""
@author: mhna
"""

import pandas as pd
import numpy as np
from dateutil.parser import parse
from datetime import  datetime
import math
import graphfunctions as gf
import QuantLib as ql

import dag
import visualize

# HIST_FILE = 'C:\Users\mhna\Documents\Python\RiskLab\sa\HistPrices.csv'
# VOL_FILE =  'C:\Users\mhna\Documents\Python\RiskLab\sa\VolParameters.csv'
HIST_FILE = '~/Downloads/HistPrices.csv'
VOL_FILE = '~/Downloads/VolParameters.csv'

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


class RatesMarket(dag.DomainObj):

     @dag.DagMethod
     def spot(self):
        return 0.025

class OptionsMarket(dag.DomainObj):

    def __init__(self,ticker, market_data):
        super(OptionsMarket,self).__init__()
        self.ticker = ticker
        self.market_data = market_data

    @dag.DagMethod
    def market_tweak(self):
        return 0

    def my_id(self):
        return self.ticker + "_" + str(self.id)

    @dag.DagMethod
    def vol(self, spot, strike = 1, tenor = 1, strike_type = 'pct'):
        tweaked_vol = self.market_data.get_vol(self.ticker,spot,strike,tenor,strike_type) + self.market_tweak()
        return tweaked_vol

class EquityMarket(dag.DomainObj):

    def __init__(self,ticker, market_data):

        super(EquityMarket,self).__init__()

        self.ticker = ticker
        self.market_data = market_data

    def my_id(self):
        return self.ticker + "_" + str(self.id)

    @dag.DagMethod
    def market_tweak(self):
        return 0

    @dag.DagMethod
    def spot(self):
        return self.market_data.get_spot(self.ticker) + self.market_tweak()

class EuropeanOption(dag.DomainObj):

    def __init__(self, underlying, opt_type, opt_strike, opt_maturity):

        super(EuropeanOption,self).__init__()

        if opt_type.upper() == 'CALL':
            self.opt_type = ql.Option.Call
        elif opt_type.upper() == 'PUT':
            self.opt_type = ql.Option.Put
        else:
            print opt_type +' is an incorrect option type'

        self.strike = opt_strike
        self.name = underlying+opt_type+str(opt_strike)+str(opt_maturity)

        maturity_date = parse(opt_maturity)
        day = maturity_date.day
        month = maturity_date.month
        year = maturity_date.year
        self.expiry = ql.Date(day, month,year)

    def my_id(self):
        return self.name + "_" + str(self.id)

    @dag.DagMethod
    def rates_market(self):
        return None

    @dag.DagMethod
    def equity_market(self):
        return None

    @dag.DagMethod
    def options_market(self):
        return None

    @dag.DagMethod
    def value_date(self):
        return ql.Date(datetime.now().day,datetime.now().month,datetime.now().year)

    @dag.DagMethod
    def PV(self):
        current_spot = self.equity_market().spot()
        spot = ql.SimpleQuote(current_spot)

        strike_vol = self.options_market().vol(self.strike,current_spot,tenor = (self.expiry - self.value_date() ), strike_type = 'abs')
        sigma = ql.SimpleQuote(strike_vol)

        r = ql.SimpleQuote(self.rates_market().spot())


        riskFreeCurve = ql.FlatForward(0,ql.TARGET(),ql.QuoteHandle(r),ql.Actual360())
        volatility = ql.BlackConstantVol(0,ql.TARGET(), ql.QuoteHandle(sigma),ql.Actual360())
        process = ql.BlackScholesProcess(ql.QuoteHandle(spot),
                                         ql.YieldTermStructureHandle(riskFreeCurve),
                                         ql.BlackVolTermStructureHandle(volatility))

        engine = ql.AnalyticEuropeanEngine(process)

        option = ql.EuropeanOption(ql.PlainVanillaPayoff(self.opt_type,self.strike),ql.EuropeanExercise(self.expiry))
        option.setPricingEngine(engine)
        PV = option.NPV()
        return PV



def main():
    emd = EquityMarketData()
    omd = OptionMarketData()
    em = EquityMarket("XOM",emd)
    om = OptionsMarket("XOM",omd)
    rm = RatesMarket()

    option1 = EuropeanOption("XOM",'put',72,'25/12/2015')
    option1.equity_market.set_value(em)
    option1.options_market.set_value(om)
    option1.rates_market.set_value(rm)
    option1.value_date.set_value(ql.Date(9,11,2015))

    print option1.PV()


    spotRange = np.linspace(-.10,.10,5)
    volRange = np.linspace(-0.05,0.05,3)

    optionPV = []
    spot  = em.spot()

    # tweak by overriding spot/vol tweak values
    for j in volRange:
        spotLadder = []
        for i in spotRange:
            em.market_tweak.set_value(spot * i)
            om.market_tweak.set_value(j)
            spotLadder.append( option1.PV() )
        optionPV.append(spotLadder)

    print optionPV

    #clean up
    optionPV = []

    #tweak the markets using context/tweaks - reprice options dependent on these markets
    for j in volRange:
        spotLadder = []

        for i in spotRange:
            with gf.context():
                gf.tweak( em.market_tweak,(spot * i) )
                gf.tweak( om.market_tweak, j )
                spotLadder.append( option1.PV())

        optionPV.append(spotLadder)

    print optionPV

    #spot ladder using layers

    layers = []

    for bump in spotRange :
        l = gf.layer()
        with l:
           gf.tweak(em.market_tweak,bump)
        layers.append(l)

    bumps = iter(spotRange)
    for alayer in layers:
        with alayer:
           print "pv spot 1+%s: %s" % (next(bumps), option1.PV())



if __name__ == "__main__" :
    main()
