# :bulb: Enerheads quantitative challenge :bulb:

Energy traded on wholesale markets contains a large amount of generation from renewable energy sources (RES). Most volatile of those being wind and solar. Accurate predictions of RES generation is crucial for market agents since they are obligated to trade their production/consumption on spot physical markets (i.e. Nord Pool).

Battery energy storage systems (BESS) play an increasingly important role in providing flexibility to the market when renewable energy forecasts deviate. On the one hand the battery may perform arbitrage in spot market, on the other hand it can provide balancing services to the grid (via products like aFRR, mFRR). Tasks given here allow us to cover two parts of energy trading - predicting system prices and optimizing battery dispatch.

## :electric_plug: Prediction of energy market prices :electric_plug:

You are given meteorological and market data for part of 2025. [Meteorological data file](https://github.com/jkved/enerheads-quant-challenge/blob/main/data/weather_location_Vilnius.csv)(s) contains day-ahead and intraday forecasts for meteorological variables for a single location. The data description is available on [OpenMeteo docs](https://open-meteo.com/en/docs) and the timezone here is in UTC. This will contain some of your predictors values. Day ahead value (with suffix `previous_day1`) is known 24 hours before delivery time, intraday (no suffix column) is around 1 hour before or at delivery time.
Market data (predictors and target values) is given in file [market data file](https://github.com/jkved/enerheads-quant-challenge/blob/main/data/market_data.csv), the data is also publicly available on [Baltic transparency dashboard](https://baltic.transparency-dashboard.eu/). Here index is in UTC timezone and two columns here are considered our target variables:
- `10YLT-1001A0008Q_DA_eurmwh` - this is Nord Pool day-ahead auction cleared prices (EUR/MWh). It is resolved day before delivery day (day-ahead), i.e. today at 10:00 UTC we find out prices for tommorrow CET day (22:00 UTC today -> 22:00 UTC tommorrow). Only weather data with `previous_day1` suffix is available at inference time
- `LT_up_sa_cbmp` or `LT_down_sa_cbmp` - this is mFRR activation prices. Generally only up or down activations take place at the same time so price is duplicated in these columns. It is resolved at delivery time (intraday). All weather data and Nord Pool prices are available at inference time but all other market data is visible with a 30 minute lag, i.e. for an mFRR activation price @ 11:00, all other market data is visible only up to (not including) 10:30.

Complete the following tasks:
1. Create Nord Pool prices forecasting model in day-ahead setting.
2. Create mFRR prices forecasting model in intraday setting
3. Implement certain evaluation metrics for prices:
    1. you wish to accurately guess times when smallest and largest prices of the day take shape.
    2. you wish to know how many instances there are with spreads between smallest and largest prices being bigger than X (say, 200 EUR/MWh).
4. Choose a collection of 2-3 plots to visualize the performance of both models.

## :battery: BESS schedule optimization :battery:

Every 15 minutes a balancing energy activations auction takes place where the price is cleared and Litgrid activates mFRR upwards or downwards (or none at all). You are given data of balancing market mFRR product in [market data file](https://github.com/jkved/enerheads-quant-challenge/blob/main/data/market_data.csv). The columns of interest here are these:
- `LT_mfrr_SA_up_activ` - cleared mFRR upwards activations (in MWh)  
- `LT_mfrr_SA_down_activ` - cleared mFRR downwards activations (in MWh)  
- `LT_up_sa_cbmp` - cleared marginal price of mFRR upwards activations (in EUR/MWh)
- `LT_down_sa_cbmp` - cleared marginal price of mFRR downwards activations (in EUR/MWh)

Given these constraints and assumptions:
1. Battery has 1 MW power and 2 MWh capacity.
2. Battery can perform 2 cycles per day (1 cycle is charging and/or discharging total amount of energy equal to capacity).
3. We are price takers (our bids dont affect the clearing price).
4. We have perfect foresight (we know all prices and activations in advance).
5. Up and down activations are only possible if they have happened for that market time unit (see input data). Also, charge and discharge cannot happen concurrently.
6. Minimal possible bid to place is 1 MW. Hence we are only able to charge 0.25 MWh for a 15 minute interval.

Write a code that finds schedule that generates best profit (discharging revenue - charging costs) for a given interval of hours:
1. Implement given constraints, parameters and decision variables using pyomo library in a `SingleMarketSolver` class of [BESS_knapsack_problem.ipynb](https://github.com/jkved/enerheads-quant-challenge/blob/main/BESS_knapsack_problem.ipynb) file
2. Write a method that creates instances of template class `SingleMarketSolver` and calculates generated profit for entire dataset. Hint - you may want to run a single optimization task for one day and carry constraints for the other day.
3. What is the optimal schedule optimization horizon? (i.e 24 hours, 25, 25.5?).
4. Calculate 95% confidence interval for profit per MWh (EUR/MWh).
5. Small depth of cycle is said to be a good metric to maintain BESS state of health. How would you suggest to calculate it?

If you feel like you need further elaboration on the nature of the task - look up (BESS) knapsack problem and linear programming.

## :email: Result submission :email:

Give us a link to your cloned repository. Present your findings in a jupyter notebooks, we'd also love to take a gander at the byproducts of your work - feel free to show training codes.