# Trending YouTube Videos

Our goal in this project is to analyze trending YouTube videos after collecting data for several months.

We use YouTube API and several AWS resources to automate the data gathering phase of our project. We use EventBridge Scheduler to invoke a Lambda function every day, which gets the trending videos list, and retrieves several metrics for these videos using YouTube API. The Lambda function then stores the gathered data in a PostgreSQL database in Amazon RDS.

We include the Python script for the Lambda function and a Jupyter notebook where we take a look at our database in its early stages.