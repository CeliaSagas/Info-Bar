![Banner](https://github.com/CeliaSagas/Info-Bar/blob/51d90c419d913a71ef2cb94e56d167421c62a673/img/InfoBarHeader.jpeg)






# Info-Bar
Critical Information Bar For Supporting Media Literacy


**Abstract**

Media Literacy is a huge issue for the internet-driven culture of the 20's. Identifying the key metrics and features that can help users make decisions about what information to believe and integrate is vital to restoring faith in the internet as a source of information.

**Design**

This project is inspired by the current need for information processing tools for internet users. By making the power of machine learning available to users with a simple point and click interface, users are supported to make their own decisions about their sources of media. To that end, the main focus of this project is a front-facing web application that can be accessed by internet users in order to gain more insight into articles they encounter online.


**Data**

The data is scraped from articles posted on five major media websites: New York Times, Fox News, BBC, Breitbart, and NBC. Scrapy spiders are automated to run every 5 minutes and add unique articles to the cloud database hosted on heroku. That same database also accepts user input in the form of article queries. If the article has not already been scraped by scrapy, the article is processed and and then added to the database.

**Algorithms**

Scrapy, Crontab, SpaCy, TextBlob, Newspaper, and NLTK are used to generate and process article data posted online.

**Feature Engineering**

The following transformations were performed on the data in order to prepare it for users:

  1.	Identified Author and Title with Newspaper
  2.	Valence was calculated with Vader
  3.	Subjectivity was calculated with TextBlob
  4.	Summary and Keywords were generated with SpaCy



**Tools**

  -	Pandas, Numpy, SpaCy, Newspaper, Vader, TextBlob
  -	Crontab, Scrapy, Flask, HTML, CSS


**Communication**

Data Visualization and write-up will be shared on Medium, Celiasagastume.com, and in class through PowerPoint presentation.
