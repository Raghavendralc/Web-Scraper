# Flask Trending Tweets Application
This guide provides step-by-step instructions for installing and deploying the Flask application that fetches and displays trending tweets.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Installing the Packages](#installing-the-packages)
- [Creating requirements.txt](#creating-requirementstxt)
- [Summary](#summary)


# Prerequisites
Before you begin, ensure you have the following installed:

Python 3.7+
pip (Python package installer)
MongoDB (Ensure MongoDB is running on your machine or accessible remotely)

To run the Flask application for fetching and displaying trending tweets, you'll need to install several Python packages. Below is the list of required packages along with a brief description of each:

Flask: A micro web framework for Python used to create web applications.
pymongo: A Python driver for MongoDB, used to interact with the MongoDB database.
twscrape: A package used to scrape X for trending tweets.

# Installing the Packages
You can install these packages using pip. Here is the requirements.txt file that lists these dependencies:

plaintext
Flask==2.1.3
pymongo==4.2.0
twscrape==1.0.1
Installing the Packages
Using requirements.txt:
Save the above content in a file named requirements.txt and run the following command to install all the packages at once:

pip install -r requirements.txt
Individually:
If you prefer to install the packages individually, you can run the following commands:

sh
pip install Flask
pip install pymongo
pip install twscrape


# Creating requirements.txt
To create a requirements.txt file, you can use the following commands to freeze the current environment's packages:

pip freeze > requirements.txt
This will generate a requirements.txt file with all the currently installed packages and their versions.

# Summary
Ensure you have the above packages installed to run the Flask application. Use the requirements.txt file for easy installation of dependencies, especially when setting up the project on a new machine or for deployment.
