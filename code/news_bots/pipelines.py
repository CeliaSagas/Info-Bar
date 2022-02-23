# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from newspaper import Article, fulltext
import spacy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import en_core_web_sm
import re
from textblob import TextBlob
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from info_bar.models import *
from sqlalchemy.orm import sessionmaker
from datetime import date

#set maxthreads
NUMEXPR_MAX_THREADS=8

#function for getting publisher name from URL
def Get_Publisher(url):
    reg_exp = r'\bhttps?://(?:www\.|ww2\.)?((?:[\w-]+\.){1,}\w+)\b'
    reg = re.compile(reg_exp, re.M)
    domain = reg.findall(url)[0]
    if domain.endswith(".com"):
        domain = domain[:-4]
        if domain == "nytimes":
            domain = "New York Times"
        if domain == "newyorker":
            domain = "New Yorker"
        if domain == "cnn":
            domain = domain.upper()
        if domain == "oann":
            domain = "One America News Network"
        if domain == "foxnews":
            domain = "Fox News"
        if domain == "nation.foxnews":
            domain = "Fox News"
        if domain == "nbcnews":
            domain = "NBC News"
        if domain =="bbc":
            domain = "BBC"
        if domain =="foxbusiness":
            domain ="Fox News"
        if domain =="breitbart":
            domain ="Breitbart"

    elif domain.endswith(".uk"):
        domain = domain[:-6]
        if domain == "bbc":
            domain = "BBC"
        if domain == "news.bbc":
            domain = "BBC"
    return domain




    return domain

class SavetoDB:
    def __init__(self):
        """
        initializes db connection
        creates tables
        """
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)


    def process_item(self,item, spider):

        session = self.Session()
        article_row = article_db()

        #check if article is already in database:
        article_exists = session.query(article_db).filter_by(URL = item['link']).first()
        if article_exists is None:

            try:





                #initiate spacy
                spacy_nlp= en_core_web_sm.load()

                #initiate vader
                analyzer=SentimentIntensityAnalyzer()

                #get article information from newspaper

                article = Article(item['link'])

                #download article
                article.download()

                #parse article with newspaper
                article.parse()
                article.nlp()

                #retrieve article author and article text with newspaper
                try:
                    author = article.authors[0]
                except IndexError:
                    author = "Not Listed"



                #retrieve article title with newspaper
                title = article.title

                #get article publisher from url
                publisher = Get_Publisher(item['link'])

                #retrieve text
                text = re.sub(r'http\S+', '', article.text).replace("\n", " . ")

                #analyze article content
                sentiment_dict = analyzer.polarity_scores(text)
                blob = TextBlob(text)

                #retrieve compount valence score
                valence_score = sentiment_dict['compound'] * 100

                #calculate subjectivity score
                subjectivity_score = round(blob.sentiment[1] * 100,2)

                #evaluate valence score from vader and add to db
                if sentiment_dict['compound'] > 0.0 :
                    valence_eval = "Positive"

                if sentiment_dict['compound'] < 0.0 :
                    valence_eval = "Negative"

                elif sentiment_dict['compound'] == 0.0 :
                    valence_eval ="Neutral"

                #evaluate subjectivity score from textblob and add to db
                if (blob.sentiment[1]) > .65:
                    subjective_eval ="Very Subjective"
                elif round((blob.sentiment[1]),2) >= .50:
                    subjective_eval ="Subjective"
                elif (blob.sentiment[1]) > .35:
                    subjective_eval ="Somewhat Objective"
                else:
                    subjective_eval ="Objective"

                #evaluate text with spacy
                doc = spacy_nlp(text)

                #calculate word frequency
                corpus = [sent.text.lower() for sent in doc.sents]
                cv = CountVectorizer(stop_words="english")
                cv_fit = cv.fit_transform(corpus)
                word_list = cv.get_feature_names();
                count_list = cv_fit.toarray().sum(axis=0)
                word_frequency = dict(zip(word_list,count_list))

                #save keywords
                val = sorted(word_frequency.values())
                keywords = article.keywords


                #calculate relative frequency
                higher_frequency = val[-1]
                for word in word_frequency.keys():
                    word_frequency[word] = (word_frequency[word]/higher_frequency)

                #save publish date


                if article.publish_date == None:
                    date_ = date.today()
                else:
                    date_ = article.publish_date




                #calculate text summary
                sentence_rank = {}
                for sent in doc.sents:
                    for word in sent:
                        if word.text.lower() in word_frequency.keys():
                            if sent in sentence_rank.keys():
                                sentence_rank[sent] += word_frequency[word.text.lower()]
                            else:
                                sentence_rank[sent] = word_frequency[word.text.lower()]

                top_sentences = dict(sorted(sentence_rank.items(),key=lambda item:item[1], reverse=True))
                summary =list(top_sentences.keys())[0:2]
                summ = "".join([token.text_with_ws for token in summary]).replace(" . ", " ")


                #add all features to dict
                item['date'] = date_
                item['Author'] = author
                item['publisher'] = publisher
                item['Title'] = title
                item['Valence_score'] = valence_score
                item ['Subjectivity_score'] = subjectivity_score
                item['Valence_eval'] = valence_eval
                item['Subjective_eval'] = subjective_eval
                item['Summary'] = summ
                item['Keyword_1'] = keywords[0]
                item['Keyword_2'] = keywords[1]
                item['Keyword_3'] = keywords[2]
                item['Keyword_4'] = keywords[3]
                item['Keyword_5'] = keywords[4]

                #add all features to db object

                article_row.Title = title
                article_row.Author = author
                article_row.Publisher = publisher
                article_row.Publish_date = date_
                article_row.URL = item['link']
                article_row.Summary = summ
                article_row.Valence_eval = valence_eval
                article_row.Subjective_eval = subjective_eval
                article_row.Valence_score = valence_score
                article_row.Subjective_score = subjectivity_score
                article_row.Keyword_1 = keywords[0]
                article_row.Keyword_2 = keywords[1]
                article_row.Keyword_3 = keywords[2]
                article_row.Keyword_4 = keywords[3]
                article_row.Keyword_5 = keywords[4]




                session.add(article_row)
                session.commit()

            except:
                session.rollback()
                raise

            finally:
                session.close()




        return item
