from flask import Flask
from flask import request, render_template
import pickle as pkl
import numpy as np
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from newspaper import Article, fulltext
import spacy
from sklearn.feature_extraction.text import CountVectorizer
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
import re
import datetime
from datetime import date
from flask_migrate import Migrate, migrate
import infobar_utils




app = Flask(__name__)

# # db path
# db_name = './data/articles.db'

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://vreeyruntyufxs:e87b80d25c5d82bdab814a289ab330140ddcc16439639aacbc502d942720f4bd@ec2-18-215-8-186.compute-1.amazonaws.com:5432/d37e6548jpe70"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# this variable, db, will be used for all SQLAlchemy commands
db = SQLAlchemy(app)

# Settings for migrations
migrate = Migrate(app, db)

# Data Model for DB
class article_db(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(), unique=False, nullable=False)
    Author= db.Column(db.String(), unique=False, nullable=True)
    Publisher= db.Column(db.String(), unique=False, nullable=True)
    Publish_date = db.Column(db.Date, unique=False, nullable = False)
    URL = db.Column(db.String(), nullable=True, unique=True)
    Summary = db.Column(db.String(), unique=False, nullable=True)
    Valence_eval = db.Column(db.String(), unique=False, nullable=True)
    Subjective_eval = db.Column(db.String(), unique=False, nullable=True)
    Valence_score = db.Column(db.Numeric(), unique=False, nullable=True)
    Subjective_score = db.Column(db.Numeric(), unique=False, nullable=True)
    Keyword_1 = db.Column(db.String(), unique=False, nullable=True)
    Keyword_2 = db.Column(db.String(), unique=False, nullable=True)
    Keyword_3 = db.Column(db.String(), unique=False, nullable=True)
    Keyword_4 = db.Column(db.String(), unique=False, nullable=True)
    Keyword_5 = db.Column(db.String(), unique=False, nullable=True)


    def __repr__(self):
        return f"Name : {self.Title}, Age: {self.Author}"

@app.route('/')
def home():
    return render_template('info_bar.html')



@app.route('/info', methods=[ "POST"])
def predict():







    if request.method=='POST':
        if (infobar_utils.Valid_URL(request.form['message'])==True):
            link = request.form['message']


            if article_db.query.filter_by(URL=link).first() is not None:

                article_record = article_db.query.filter_by(URL=link).first()
                return_dict ={
                "Title": article_record.Title,
                "Author":article_record.Author,
                "Publisher":article_record.Publisher,
                "Date": (article_record.Publish_date).strftime('%m/%d/%Y'),
                "Valence":str(article_record.Valence_eval) +" ("+ str(round(article_record.Valence_score,2))+")",
                "Subjectivity": str(article_record.Subjective_eval) +" ("+ str(round(article_record.Subjective_score,2))+")",
                "Summary":article_record.Summary,
                "Keywords": article_record.Keyword_1+", "+article_record.Keyword_2+", "+article_record.Keyword_3+", "+article_record.Keyword_4+", "+article_record.Keyword_5
                }
            else:



                #load spacy
                try:
                    spacy_nlp = spacy.load("en_core_web_sm")
                except: # If not present, we download
                    spacy.cli.download("en_core_web_sm")
                    spacy_nlp = spacy.load("en_core_web_sm")





                #initiate vader
                analyzer=SentimentIntensityAnalyzer()

                #get article information from newspaper

                article = Article(link)


                #download article
                article.download()

                #parse article with newspaper
                article.parse()
                article.nlp()

                #retrieve article author and article text with newspaper
                try:
                    author = article.authors[0]
                    if author == "Condé Nast":
                        author = article.authors[1]
                except IndexError:
                    author = "Not Listed"
                #get article text and clean links
                text = re.sub(r'http\S+', '', article.text).replace("\n", " . ")

                #get article publisher from url
                publisher = infobar_utils.Get_Publisher(link)

                #retrieve article title with newspaper
                title = article.title

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
                keywords = [word for word,freq in word_frequency.items() if freq in val[-5:]][0:5]

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



                p = article_db(
                    Title = title,
                    Author = author,
                    Publisher = publisher,
                    Publish_date = date_,
                    URL = request.form['message'],
                    Summary = summ,
                    Valence_eval = valence_eval,
                    Subjective_eval = subjective_eval,
                    Valence_score = valence_score,
                    Subjective_score = subjectivity_score,
                    Keyword_1 = keywords[0],
                    Keyword_2 = keywords[1],
                    Keyword_3 = keywords[2],
                    Keyword_4 = keywords[3],
                    Keyword_5 = keywords[4]
                    )

                if request.method == "POST":

                    return_dict ={

                        "Title":title,
                        "Author":author,
                        "Publisher":publisher,
                        "Date": date_.strftime('%m/%d/%Y'),
                        "Valence": str(valence_eval+" ("+str(round(valence_score,2))+")"),
                        "Subjectivity":str(subjective_eval+" ("+str(subjectivity_score)+")"),
                        "Summary":summ,
                        "Keywords":", ".join(keywords)
                    }

                    db.session.add(p)
                    db.session.commit()
                else:
                    return_dict = {
                        "Data":"Not Available",

                        }

        else:
            return render_template('info_bar_retry.html')




    return render_template('results.html', res = return_dict )




if  __name__=='__main__':
 app.run(debug=True)
