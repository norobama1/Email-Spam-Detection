import streamlit as st
import pickle
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

ps = PorterStemmer()

def transform_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)
    y = []
    for i in text:
        if i.isalnum():
            y.append(i)
            
    text = y[:]
    y.clear()
    
    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)
            
    text = y[:]
    y.clear()
    
    for i in text:
        y.append(ps.stem(i))
            
    return " ".join(y)

tfidf = pickle.load(open('vectorizer.pkl','rb'))
model = pickle.load(open('model.pkl','rb'))

st.title('Email/SMS Spam detection')

input_sms = st.text_area('Enter the text')

if st.button('predict'):

    #1) Preprocess
    transform_sms = transform_text(input_sms)

    #2) Vectorize
    vectorized_sms = tfidf.transform([transform_sms])

    #3)Predict the model
    result = model.predict(vectorized_sms)[0]

    #4) Display
    if result == 1:
        st.header('Spam')
    else:
        st.header('Not Spam')
    