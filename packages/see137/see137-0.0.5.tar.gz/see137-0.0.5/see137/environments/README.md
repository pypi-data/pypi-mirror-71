# Trial Management


How we'll be managing reinforcement learning trials as well as conventional backtesting. I had the chance to look at the metatrader backtesting api and fell in love with it's simplicity.

It looks like the following:

```py
from metatrader.mt4 import initizalize
from metatrader.backtest import BackTest

# point mt4 install folder
initizalize('C:\\Program Files\\FXCM MetaTrader 4')

# specify backtest period by datetime format
from_date = datetime(2014, 9, 1)
to_date = datetime(2015, 1, 1)

ea_name = 'Moving Average'

# create ea param by dict.
param = {
         'Lots': {'value': 0.1},
         'MaximumRisk': {'value': 0.02},
         'DecreaseFactor': {'value': 3.0},
         'MovingPeriod': {'value': 12},
         'MovingShift': {'value': 6}
         }
# create backtest object
backtest = BackTest(ea_name, param, 'USDJPY', 'M5', from_date, to_date)

# run backtest
ret = backtest.run()

# you can get result from result object
# for example you can print gross profit
print(ret.gross_profit)
```


Then I remembered tensortrade's environment:

```py
from tensortrade.environments import TradingEnvironment

environment = TradingEnvironment(exchange=exchange,
                                 action_scheme=action_scheme,
                                 reward_scheme=reward_scheme,
                                 feature_pipeline=feature_pipeline)
```


## Trial Management for Linkkt

Our trial management should be exactly that simple, yet should allow us to have many moving parts. Much like what we've seen in other backtesting systems. Here are some examples:

### Backtesting

```py
import maya
from see137.trial import (
    BacktestEnvironment, 
    TimeConfiguration, 
    AssetConfiguration, 
    PortfolioConfiguration,
    StrategyConfiguration
)


start = Dict()
start.time = "2011-02-07"
start.timezone = 'US/Eastern'



end = Dict() 
end.time = "2020-04-01",
end.timezone:'US/Eastern'

step_settings = Dict()
step_settings.hours = 3
step_settings.milliseconds = 0
step_settings.minutes = 0

time_settings = TimeConfiguration(
    start=start,
    end=end,
    step_size= step_settings
)


asset_settings = AssetConfiguration(
    setname="example_set_name"
)

user_settings = PortfolioConfiguration(
    base_instrument="USD",
    exchange="coinbase",
    initial_balance=10000000.0
)

strategy_settings = StrategyConfiguration(
    strategy=ExampleStrategy,
    assistance=False, # Determine if we want to use creme-ml to get probability of upward and downward movement
    run_method="split" # Run on each asset equally
)



backtest = BacktestEnvironment(
    name="SimpleBacktest"
    portfolio_scheme=user_settings,
    time_scheme=time_settings,
    asset_scheme=asset_settings,
    strategy_scheme=strategy_settings,
)

backtest_id = backtest.id


backtest.run()


backtest.performance()
backtest.status()
backtest.resources()

backtest = BacktestEnvironment.by_id(backtest_id)
backtest.performance()
backtest.status()
backtest.resources()
```



All settings should have a `by_id` command as well. One that would allow us to get objects `by_id`.



`StrategySettings.by_id()` would return a strategy we could use in another backtest.

This would also allow us to save a trial by a sequence of ids instead of storing objects directly. We'd store the objects on run.



### Reinforcement Learning

```py

import maya
from see137.trial import (
    RLEnvironment, TimeSettings, AssetSettings, 
    EpisodeSettings, UserSettings, RiskSettings,
    DagSettings, RewardSettings
)


step_settings = {
    "minute": 0,
    "hours": 1
}

time_settings = TimeSettings(
    step_size= step_settings
)


asset_settings = AssetSettings(
    assets=[
        {
            "name": "btc_usd",
            "market_information": {
                "market_type": "crypto",
                "exchange": "binance"
            }
        }
        ...
    ]

)

user_settings = UserSettings(
    user_id=user_id
)

# Indicating that we'd train on simulation data before running it on real data
episode_settings = EpisodeSettings(
    learning_strategy="sim2real",
    simulation_type="stochastic",
    episode_length=1000,
    episode_number=1000,
    # How many episodes we'll run at once before adding more
    parallel_max=200
)


risk_params = {
    "online": True,
    "ensemble": True
}
risk_settings = RiskSettings(
    **risk_params
)

# Set a dag of how we'd like price information to run before we pull the resulting information to form a statespace
dag_settings = DagSettings(
    
)

reward_settings = RewardSettings()

trainer = RLEnvironment(
    name="SimpleRL",
    user_scheme=user_settings,
    time_scheme=time_settings,
    asset_scheme=asset_settings,
    episode_scheme=episode_settings,
    risk_scheme=risk_settings,
    dag_settings=dag_settings,
    reward_scheme=reward_settings
)



trainer_id = trainer.id


trainer.train()


trainer.performance()
trainer.status()
trainer.resources()

trainer = RLEnvironment.by_id(backtest_id)
trainer.performance()
trainer.status()
trainer.resources()

```