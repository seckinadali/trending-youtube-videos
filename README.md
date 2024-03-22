# Trending YouTube Videos

Our objective in this project is to analyze trending YouTube videos by collecting data over several months.

To automate the data collection phase, we utilize the YouTube API in conjunction with various AWS resources. Employing EventBridge Scheduler, a Lambda function is invoked daily, fetching the trending videos list and extracting key metrics via the YouTube API. Subsequently, the Lambda function stores this data in a PostgreSQL database hosted on Amazon RDS.

In a Jupyter notebook, we access this database and conduct an exploratory analysis on the dataset. Specifically, we address the following questions:

1. Are there any videos that exhibit notable outlier behavior?
2. How do the variables correlate with each other?
3. Are there any time points where the variables demonstrate significant fluctuations?
4. Are there any particular days that stand out as optimal for video publishing?

Included are the Python script for the Lambda function and the Jupyter notebook containing our analysis.