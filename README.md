# Tick_by_Tick_Algotrader

Create a pipeline of Reader -> Filter -> Algorithm to find good investments opportunities with high frequency data

The project has 3 parts that work sequentially as it offers the ability to test each part individually, making the whole structure more reliable and modular.
* The first part of the model is the data receiver and broadcaster; this part would be responsible for
reading the data from the dataset and broadcasting it to the model. 
* The second part is the filter; it would receive all the data from the dataset and create a filtered version of the data with less noise and smoother transitions. 
* The final one is the trading algorithm; this last part uses the filtered data
to decide whether it should or should not trade the stock. Figure 3 illustrates the whole pipeline.

As for running the project a tkinter interface was created so it became easier to work with and test algorithms, the inputs and outputs of this interface are described bellow.

The software had to have for inputs:
* trade date or range – To allow for different dates to be simulated
* Graph refresh rate – To allow the user to see the day develop as an actual simulation
* Filter selection – Select time, volume, or ticks moving average with or without bagging
* Filter specifications – Select moving average step
* Trading algorithm selection – Select signal (Derivatives) and Trading Algorithm
(Standard, Waiter)
* Trading algorithm specifications – Select the signal α and amount of stocks to buy
* Begin/Stop simulation button – Allow users to start and restart the simulation

And for outputs:
* Filter precision and lag – Graph to display how well the filter is following the data
* Trading algorithm trades – Graph to display the type, time and value of trades made
* Raw profit (not considering taxes) – Graph to display how the model profit is behaving
* Real profit – A absolute value with the taxes calculation result
* Current BID and ASK – The absolute value of best BID and best ASK values
* Number of trades – The absolute value of trades made in the day

As for the available filters there are 3 main available filters, moving averages in ticks, in time and in volume.

Regarding the algorithm the main algorithms is an equation based on the numerical derivative of the filtered data. This algorithm calculates the numerical derivative of the stock price with difference of the last step of the filter and current step divided by the time that past between them (Equation 1), then it would see if the stock price is rising (derivative greater the 0), decreasing (derivative smaller than 0) or stable (derivative equal to 0). With the derivative, the trading algorithm assumed that the value tendency would remain constant and bought stocks when the price was rising, sold when it was decreasing and zeroed when it was stable.

Still in the algorithm a dead-zone filter is a gap between values, in this case derivatives, and it is used so model doesn’t skip any signals or abruptly change signal with small price fluctuations. For that the parameter 𝛼 represents the length of the dead zone and regulates how sensitive the signal is to the price derivatives.

Finally there are 2 Trading Algorithms a really simple "fulfill the order regardless of the price" and was named "standard" as no algorithm is necessary for this kind of trade and a broker called "waiter" was developed, this new algorithm after receiving the signal did not immediately react and bought or sold stocks instead it waited to see if the BID or ASK price would fluctuate toward the exact price it wished to buy or sell the stock. If that did not happen it would wait a certain amount of ticks and then proceed to buy the stock if it was still close enough to the original price.
