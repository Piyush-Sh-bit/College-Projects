# -Stock-Price-Prediction-using-NLP-based-on-Historical-Data-and-News-Headlines
## Project title: 

Stock Price Prediction using NLP based on Historical Data and News Headlines


## Dataset used:

•	ADANI PORTS Dataset: Historical stock data of Adani Ports (2007-2021) including columns: Date, Symbol, Series, Prev Close, Open, High, Low, Last, Close, VWAP, Volume, Turnover, Trades, Deliverable Volume, %Deliverable. 
This Dataset is used to perform Stock Market Analysis and Time Series Predictions on Adani Ports Stocks.
Link for the dataset: 
https://finance.yahoo.com/quote/ADANIPORTS.NS/history/

•	AppleNews Dataset: Historical Stock data of Apple (2019-2022) including columns: Date, News Headline, Stock Open, Stock Close, Movement.
This Dataset is used to perform Stock close Predictions on Apple Stocks using a Sentimental Analysis of News Headlines.
Link for the dataset: 
https://drive.google.com/file/d/19-s2N4wkI6IVmyU_yvEg5QMN73Y0oZUo/view

•	Stock Dataset - ApplestockData.csv: This dataset contains historical stock data of Apple (2006-2016), including columns such as 'Date', 'Open', 'High', 'Low', 'Close', 'Adj Close'.
News Dataset- apple_news.csv: This dataset includes news headlines related to Apple, along with the corresponding 'Date' column
These Datasets combined used for Stock Close Prediction using NLP based on Historical Data and News Headlines.


## Methods used:

### Time Series Analysis and Predictions on Adani Ports Stocks Using ARIMA MODEL.

1.	Data Loading and Preprocessing:
•	Libraries are imported, and Google Drive API is authenticated.
•	File is downloaded and loaded into a pandas DataFrame.
•	Missing values are checked and filled with the mean DataFrame index is reset.

2.	Data Visualization:
•	A correlation heatmap is plotted using seaborn.
•	A line plot of the 'Close' price column is shown.
•	A cumulative returns plot and an autocorrelation plot are generated.
•	
3.	Train-Test Split:
•	DataFrame is split into training and testing datasets (70:30 split) and a line plot visualizes the split.

4.	ARIMA Modeling and Forecasting:
•	'Open' price column is extracted from the training and testing datasets and an ARIMA model with order (5,1,0) is fitted on the training data.
•	For each data point in the testing dataset, a value is forecasted using the fitted model.
•	Predicted and actual values are stored, and MSE and SMPE are calculated.
5.	Visualization of Results:
•	A line plot is created to compare the predicted and actual prices.
•	Another plot with a specific date range is generated to focus on the predicted and actual prices.


ARIMA (AutoRegressive Integrated Moving Average)
ARIMA is a popular time series forecasting model that combines autoregressive (AR), differencing (I), and moving average (MA) components. It is widely used for analyzing and predicting time series data.
The AR component models the relationship between the current observation and a certain number of lagged observations. The I component involves differencing the time series to make it stationary. Differencing subtracts each observation from its previous observation, which helps remove trends and seasonality. The MA component models the dependency between the current observation and a residual error from a moving average of past observations and captures short-term dependencies.
The ARIMA model combines these components to create a linear regression model on the differenced time series data. The ARIMA model can be used for time series forecasting by fitting the model on historical data and making predictions for future time points.


### Stock close Predictions on Apple Stocks using a Sentimental Analysis of News Headlines.

1.	Data Preparation:
Downloading a CSV file from a Google Drive link and reading it into a pandas DataFrame and identify any missing values in the "News Headline" column.
2.	Sentiment Analysis:
Use of VADER (Valence Aware Dictionary and sEntiment Reasoner) sentiment analysis tool from NLTK to perform sentiment analysis on the news headlines to calculate entiment score for each headline and classifies it as positive, negative, or neutral based on a threshold.
3.	Text Preprocessing:
Performs several preprocessing steps on the news headlines. It tokenizes the headlines, removes stopwords, performs lemmatization, and applies stemming. The processed headlines are stored in separate columns of the DataFrame.
4.	Feature Extraction:
Two approaches are used for feature extraction: CountVectorizer and TF-IDF Vectorizer. The code creates feature vectors from the cleaned news headlines using both methods.
5.	Stock Price Prediction:
Split the dataset into training and testing sets for both feature representations.
Train a Random Forest Regressor model on the bag-of-words features and evaluate its performance using mean squared error (MSE) and R-squared (R2) scores.Train another Random Forest Regressor model on the TF-IDF features and evaluate its performance.
Train a Linear Regression model on the bag-of-words features and evaluate its performance using MSE.
6.	Price Prediction: 
The code demonstrates how to use the trained models to make price predictions for new text data. It provides an example by predicting the stock price based on a new text input. 


###	Stock Price Prediction using NLP (Historical + News Data) of Apple Company

1. Data Preprocessing:
•	Preprocessing stock data by converting the 'Date' column to datetime and setting it as the index.
•	Preprocessing news data by converting the 'Date' column to datetime and setting it as the index.
2. Data Integration:
•	Merging stock and news data based on the 'Date' column.
3. Data Splitting:
•	Splitting the merged data into training and testing sets.
       4. Data Engineering:
•	Scaling the numerical features using MinMaxScaler.
•	Vectorizing the news data using TF-IDF.
5. Model Training and Evaluation:
•	Training a Linear Regression model on the combined features.
•	Predicting the stock prices using the trained model.
•	Calculating the Root Mean Squared Error (RMSE) to evaluate the model's performance.   
 6. Prediction on New Data:
•	New data with the desired input features is created and preprocessed by setting the date as the index and scaling the numerical features. The news text in the new data is vectorized. Both are combined to create the final feature set for the new data.
•	The model predicts the stock closing price for the new data.
Results:

Time Series Analysis and Predictions on Adani Ports Stocks Using ARIMA MODEL.
![image](https://github.com/Piyush23445/-Stock-Price-Prediction-using-NLP-based-on-Historical-Data-and-News-Headlines/assets/89131804/9bea9afb-f737-4995-914a-716f319b3fba)

 ![image](https://github.com/Piyush23445/-Stock-Price-Prediction-using-NLP-based-on-Historical-Data-and-News-Headlines/assets/89131804/fb32a3fd-f207-41dc-91b1-cee685d9fee8)
                     
![image](https://github.com/Piyush23445/-Stock-Price-Prediction-using-NLP-based-on-Historical-Data-and-News-Headlines/assets/89131804/a06568c7-3734-4be9-8ce9-5459ca55529c)

![image](https://github.com/Piyush23445/-Stock-Price-Prediction-using-NLP-based-on-Historical-Data-and-News-Headlines/assets/89131804/9f1e6822-a78c-4a45-bbd3-e09f686f355e)
 
###	Stock close Predictions on Apple Stocks using a Sentimental Analysis of News Headlines.
![image](https://github.com/Piyush23445/-Stock-Price-Prediction-using-NLP-based-on-Historical-Data-and-News-Headlines/assets/89131804/f956deaa-8ff0-43a7-b3d2-28083fca68f6)

 ![image](https://github.com/Piyush23445/-Stock-Price-Prediction-using-NLP-based-on-Historical-Data-and-News-Headlines/assets/89131804/8a96d1be-aa14-4aa1-b54a-1a442e84d459)
 
Bag of Words
 ![image](https://github.com/Piyush23445/-Stock-Price-Prediction-using-NLP-based-on-Historical-Data-and-News-Headlines/assets/89131804/975d9a5b-6e29-4977-bcf4-717506d8b9e9)

![image](https://github.com/Piyush23445/-Stock-Price-Prediction-using-NLP-based-on-Historical-Data-and-News-Headlines/assets/89131804/b02fac30-e692-4986-91aa-ea6e163284b0)
 
TF-IDF
 ![image](https://github.com/Piyush23445/-Stock-Price-Prediction-using-NLP-based-on-Historical-Data-and-News-Headlines/assets/89131804/0c975018-d49b-4807-8ad5-de004f85b068)

![image](https://github.com/Piyush23445/-Stock-Price-Prediction-using-NLP-based-on-Historical-Data-and-News-Headlines/assets/89131804/b4057bee-e5d5-4d43-ab76-9724edbe5f04)
 
APPLYING RANDOM FOREST ON BAG OF WORDS & TF-IDF VECTORIZATION TECHNIQUES
![image](https://github.com/Piyush23445/-Stock-Price-Prediction-using-NLP-based-on-Historical-Data-and-News-Headlines/assets/89131804/220e5566-f850-4c20-a28e-2f5a7ff780b0)
 
![image](https://github.com/Piyush23445/-Stock-Price-Prediction-using-NLP-based-on-Historical-Data-and-News-Headlines/assets/89131804/46bcda7c-61c3-4079-8f4a-cbba71fa9194)
 
APPLYING LINEAR REGRESSION
BAG OF WORDS
![image](https://github.com/Piyush23445/-Stock-Price-Prediction-using-NLP-based-on-Historical-Data-and-News-Headlines/assets/89131804/d2464b13-3f13-4aca-8009-8f6bc6abd36b)
 
TF-1DF
![image](https://github.com/Piyush23445/-Stock-Price-Prediction-using-NLP-based-on-Historical-Data-and-News-Headlines/assets/89131804/4f67189b-6892-423c-b5b0-c8f66f6b89ca)
 
###	Stock Price Prediction using NLP (Historical + News Data) of Apple Company

DATASETS

![image](https://github.com/Piyush23445/-Stock-Price-Prediction-using-NLP-based-on-Historical-Data-and-News-Headlines/assets/89131804/6f2635f7-f494-4c3c-a04c-a41b104ccb00)
 
![image](https://github.com/Piyush23445/-Stock-Price-Prediction-using-NLP-based-on-Historical-Data-and-News-Headlines/assets/89131804/d535cfa9-f078-404b-836a-8bfb99c6309f)
 
![image](https://github.com/Piyush23445/-Stock-Price-Prediction-using-NLP-based-on-Historical-Data-and-News-Headlines/assets/89131804/dc5504ea-a9c7-409b-93b3-1f47c318eff4)

![image](https://github.com/Piyush23445/-Stock-Price-Prediction-using-NLP-based-on-Historical-Data-and-News-Headlines/assets/89131804/7fe283f7-82b3-471a-a11a-afa72d1a45d6)
 
 
PREDICTION
![image](https://github.com/Piyush23445/-Stock-Price-Prediction-using-NLP-based-on-Historical-Data-and-News-Headlines/assets/89131804/c23e7ae2-6ff3-4a9e-9086-6ade10a50505)

 
### Challenges or learning throughout project development:

•	Handling missing values, and outliers, and formatting the data appropriately for analysis. Learn how to handle such data preprocessing tasks effectively for accurate analysis.

•	Choosing appropriate evaluation metrics to assess the model's performance. Understanding these metrics and their limitation is a learning experience.

•	Choosing the right model for time series analysis. ARIMA is a popular choice, but understanding its assumptions, order selection, and performance evaluation techniques is important.

•	Choosing the appropriate regression model (e.g., Random Forest Regressor, Linear Regression) and evaluating its performance using metrics like mean squared error (MSE) or R-squared. Understanding the limitations and assumptions of different models, as well as interpreting the evaluation results, requires careful consideration.

•	Dealing with encoding errors when reading the CSV file.

•	Ensuring proper data formatting and handling inconsistencies in the CSV file.

•	Optimizing the feature engineering process and choosing appropriate scaling and vectorization techniques.

