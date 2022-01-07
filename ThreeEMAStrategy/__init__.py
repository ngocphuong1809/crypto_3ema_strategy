from jesse.strategies import Strategy, cached
import jesse.indicators as ta
from jesse import utils


class ThreeEMAStategy(Strategy):

    def hyperparameters(self):
        return [
            {'name': 'slow_EMA_Length', 'type': int, 'default': 55},
            {'name': 'middle_EMA_Length', 'type': int, 'default': 21},
            {'name': 'fast_EMA_Length', 'type': int, 'default': 9},
            {'name': 'trend_MA_Length', 'type': int, 'default': 200},
            {'name': 'atr_Length', 'type': int, 'default': 14},
            {'name': 'tp_ATR_Mult', 'type': int, 'default': 3},
            {'name': 'sl_ATR_Mult', 'type': int, 'default': 2},
            {'name': 'rsi_Length', 'type': int, 'default': 14},
        ]

    @property
    def slow_EMA(self):
        return ta.ema(self.candles, self.hp["slow_EMA_Length"])
    
    @property
    def midd_EMA(self):
        return ta.ema(self.candles, self.hp["middle_EMA_Length"])

    @property
    def fast_EMA(self):
        return ta.ema(self.candles, self.hp["fast_EMA_Length"])

    @property
    def atr(self):
        return ta.atr(self.candles, self.hp["atr_Length"])
    
    @property
    def rsi_Value(self):
        return ta.rsi(self.candles, self.hp["rsi_Length"])

    @property
    def sma200(self):
        return ta.sma(self.candles, self.hp["trend_MA_Length"])
    @property
    def is_Rsi_OB(self):
        if self.rsi_Value >= 80:
            return self.rsi_Value

    @property 
    def is_Rsi_OS(self):
        if self.rsi_Value <=20:
            return self.rsi_Value

    def should_long(self) -> bool:
        return self.midd_EMA > self.slow_EMA

    def should_short(self) -> bool:
        return False

    def should_cancel(self) -> bool:
        return self.fast_EMA <= self.midd_EMA

    def go_long(self):
            take_profit = self.price + self.atr*self.hp["tp_ATR_Mult"]
            stop = self.price - self.atr*self.hp["sl_ATR_Mult"]
            # qty = 10
            qty = utils.size_to_qty(self.balance, self.price)
            self.buy = qty, self.price
            self.stop_loss = qty, stop
            self.take_profit = qty, take_profit

    def update_position(self) ->None:
        if self.is_Rsi_OB:
             # self.liquidate() closes the position with a market order
            self.liquidate()
        elif self.is_Rsi_OS:
            self.liquidate()
        # if self.fast_EMA <= self.midd_EMA:
        #     self.liquidate()
   
    def go_short(self):
        pass
# // STRATEGY
# goLong  = crossover(middEMA, slowEMA) and inDateRange
# closeLong = crossunder(fastEMA, middEMA) and inDateRange   
   
# Simple 3 EMA Strategy with plotted Take Profit and Stop Loss

# Entry condition:
# - Middle EMA cross above the Slow EMA
# - Set take profit and stop loss exit conditions based on ATR Indicator

# Exit condition:
# - Fast EMA cross below the Middle EMA
