![Banner](https://github.com/CeliaSagas/Lidar-Net/blob/394ca201bff3ef4ecdc1b805da835338b488298e/img/Lidar-Net.jpeg)



# Info-Bar
Critical Information Bar For Supporting Media Literacy




**Question/Need:**

1. What is the question behind your analysis? What is the purpose of the model/system you plan to build?

      - Media literacy is a big issue in this time, as verifying the veracity of claims made online can take a significant amount of research which is prohibitive to many internet users. This project aims to offer internet users the information they need in order to make proactive decisions around their media intake.




2. Who benefits from exploring this question or building this model/system?

    - All internet users who intake information from online platforms can benefit from an app that supplies the background information they need in order to make proactive decisions around what claims they believe as valid and truthful.



**Data Description:**

1. What dataset(s) do you plan to use, and how will you obtain the data?

    - The dataset I will be using comes from [All The News](https://www.kaggle.com/snapcrack/all-the-news), a collection of over 100,000 articles published between the years 2015 - 2017 on a variety of publications such as the New York Times, Breitbart, Buzzfeed, and Vox.

2. What is an individual sample/unit of analysis in this project?

    - A single unit of analysis is a single article.

3. What characteristics/features do you expect to work with?

    - I expect to work the Title, Author, Date of Publication, and article content in order to create features of interest, such as % of hyperbolic language, one line summary, author info, quotes, statistics, and other points of view.

4. If modeling, what will you predict as your target?

    - I have to do more research on hyperbolic nlp classifiers to adequately answer that.


**Tools:**

1. How do you intend to meet the tools requirement of the project?

    - I plan to use Google Colab, Flask, and Heroku on a base dataset of over 100,000 data points.

2. Are you planning in advance to need or use additional tools beyond those required?

    - Yes, I may develop this as a google chrome extension.



**MVP Goal:**

1. What would a minimum viable product (MVP) look like for this project?

    - My MVP will be a baseline nlp classifier that can detect % of hyperbolic language in an article.
