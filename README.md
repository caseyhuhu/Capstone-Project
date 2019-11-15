# Capstone-Project

Predicting future trends in the stock market has been a long-researched topic in market analysis. Commonly, stock brokers use various judgments on past patterns in a stock as well as existing trends to predict how a stock’s price will change. However, the SEC database known as EDGAR (Electronic Data Gathering, Analysis, and Retrieval System) contains huge amounts of financial data that has not been used to its fullest potential in the field of stock market prediction. The aim of our project was to create a scraper for EDGAR data and to use that data in a Recurrent Neural Network (RNN) to make correlations and predictions on the future value of stocks.

There are three main steps in using the web application:

1. Upload a CSV in the same format as our starter CSV.
    * All 12 features must be present for each company.
    * All columns containing stock price must be the rightmost columns of the CSV.
    * Columns must be labeled exactly as seen in the example, with company names listed using their stock symbol.  


2. Cluster companies based on their stock value over time. This can be used separately from the other two steps.
    * Enter a comma-separated list of one or more stock symbols to add companies to the cluster calculation.
    * Each cluster is displayed on a graph of the stock price since 1/1/2008.
    * Press reset button to reset 'Stock data.csv' and 'clusters.txt' on the backend to how they were originally.  
    
    
3. Predict the future value of a given stock.
    * Enter the stock symbol of a company to begin predicting its future stock price.
    * Press the predict button to automatically reset the clusters and create new clusters using the companies in the user-inputted CSV
    * The user-inputted CSV is combined with the starter data and fed to the RNN, which produces a prediction.