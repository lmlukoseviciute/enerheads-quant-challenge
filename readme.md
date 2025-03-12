# :bulb: Enerheads quantitative challenge :bulb:

Energy traded on wholesale markets contains rapidly growing amount of generation from renewable energy sources (RES). Most volatile of those being wind and solar. Accurate predictions of RES generation is crucial for market agents since they are obligated to trade their production/consumption on spot physical markets (i.e. Nord Pool). The error of total prod/cons when settling is considered imbalance and is penalized by having market agents pay some price for each MWh of imbalance. This price in most cases is worse than the spot market price. 

Battery energy storage systems (BESS) play an increasingly important role in minimizing said imbalance and/or providing flexibility to the market. On the one hand the battery may perform arbitrage in spot market, on the other hand it can provide balancing services to the grid (via products like aFRR, mFRR). All because it is a controlled generation asset. Tasks given here allow us to cover two parts of energy trading - predicting system imbalances and optimizing battery operation.

## :electric_plug: Imbalance and activations prediction model :electric_plug:

You are given meteorological and market data for part of 2025 Q1. [Meteorological data file](https://github.com/jkved/enerheads-quant-challenge/blob/main/data/openmeteo_location0.csv)(s) contains day-ahead and intraday forecasts for meteorological variables for a single location. The data description is available on [OpenMeteo docs](https://open-meteo.com/en/docs) and the timezone here is in UTC. This will contain most of your predictors values. Day ahead value (with suffix '_day1') is known 24 hours before delivery time, intraday (no suffix column) is around 1 hour before delivery time.
Market data (predictors and target values) is given in file [market data file](https://github.com/jkved/enerheads-quant-challenge/blob/main/data/spot_balancing_2025Q1.csv), the data is also publicly available on [Baltic transparency dashboard](https://baltic.transparency-dashboard.eu/). Here index is in EET timezone and columns of interest are these:
- 'LT_mfrr_SA_up_activ' - mFRR upwards activations (in MW). Upwards means the system is in energy shortage and additional generation is activated or consumption turned off. In other words, battery can discharge in this timestep.
- 'LT_mfrr_SA_down_activ' - mFRR downwards activations (in MW). Downwards is the vice versa of upwards. In other words, battery can charge in this timestep.
- 'LT_imb_MW' - imbalance of LT system (in MW) before any activations from Litgrid.
- '10YLT-1001A0008Q_DA_eurmwh' - this is Nord Pool day-ahead auction cleared price (EUR/MWh). Consider it to be part of predictors since it is known in advanced.

Activations are Litgrid activated energy used to balance the system (to counter the imbalance). Train an imbalance and mFRR activations prediction models:
1. Calculate deltas for meteorological values.
2. Train and evaluate a prediction model for imbalance and mFRR activations. Which can you forecast more accurately? Can we use imbalance as a predictor for activations?
3. Assume we know actual values of activations 30 minutes after, for example, at 12:00 we know value of 11:15. what autoregressive timeseries forecasting method is good for forecasting? How does it compare to your previous model?
4. What tendencies do you see in imbalance volumes? For example, imbalance is positive for some hours, or happens almost certainly under some weather conditions? 

## :battery: BESS schedule optimization :battery:

Every 15 minutes a balancing energy activations auction takes place where the price is cleared and Litgrid activates mFRR upwards or downwards (or none at all). You are given data of balancing market mFRR product in [market data file](https://github.com/jkved/enerheads-quant-challenge/blob/main/data/spot_balancing_2025Q1.csv). The columns of interest here are these:
- 'LT_mfrr_SA_up_activ' - mFRR upwards activations (in MW)  
- 'LT_mfrr_SA_down_activ' - mFRR downwards activations (in MW)  
- 'LT_up_sa_cbmp' - marginal price of mFRR upwards activations (in EUR/MWh)
- 'LT_down_sa_cbmp' - marginal price of mFRR downwards activations (in EUR/MWh)
If you feel like you need further elaboration on the nature of the task - look up knapsack problem and linear programming.

Given these constraints and assumptions:
1. Battery has 1 MW power and 2 MWh capacity.
2. Battery can perform 2 cycles per day (1 cycle is charging and/or discharging total amount of energy equal to capacity).
3. We are price takers (our bids dont affect the clearing price).
4. We have perfect foresight (we know all prices and activations in advance).
5. Up and down activations are only possible if they have happened for that market time unit (see input data). Also, charge and discharge cannot happen concurrently.
6. Minimal possible bid to place is 1 MW. Hence we are only able to charge 0.25 MWh for a 15 minute interval.

Write a code that finds schedule that generates best profit (discharging revenue - charging costs) for a given interval of hours:
1. Implement given constraints using pyomo library in a `SingleMarketSolver` class of .py file
2. Write a method that creates instances of template class `SingleMarketSolver` and calculates generated profit for entire dataset. Hint - you may want to run a single optimization task for one day and carry constraints for the other day.
3. What is the optimal schedule optimization horizon? (i.e 24 hours, 25, 25.5?).
4. Calculate 95% confidence interval for profit per MWh (EUR/MWh).
5. Small depth of cycle is said to be a good metric to maintain BESS state of health. How would you suggest to calculate it?

Please do the this task on a given template file [BESS_knapsack_problem.py](https://github.com/jkved/enerheads-quant-challenge/blob/main/BESS_knapsack_problem.ipynb)  so it is easier to compare the results. 

## :email: Result submission :email:

Send us a .zip or give us a link to your cloned repository. Present your findings in a jupyter notebooks, we'd also love to take a gander at the byproducts of your work - feel free to show training codes, etc. For 2nd task - save output dataframe to .csv.