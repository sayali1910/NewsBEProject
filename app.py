from bs4 import BeautifulSoup
import requests
import pandas as pd
import spacy
import heapq
import re
import nltk
import matplotlib.pyplot as plt
import json
from flask import Flask, Response, render_template,request
import plotly
import plotly.graph_objs as go
pd.options.plotting.backend = "plotly"

    
app = Flask(__name__)


@app.route('/')
def index():
	
    global df,dfcity
    df = pd.DataFrame(columns = ['Date','Year','Time', 'City','URL', 'Headline','Type'])

    dfcity = pd.DataFrame(columns=['City','CrimeRate'])

    NoCrime = getNews('https://timesofindia.indiatimes.com/city/mumbai','Mumbai')
    dfcity = dfcity.append({'City':'Mumbai','CrimeRate':NoCrime},ignore_index = True)

    NoCrime = getNews('https://timesofindia.indiatimes.com/city/delhi','Delhi')
    dfcity = dfcity.append({'City':'Delhi','CrimeRate':NoCrime},ignore_index = True)

    NoCrime = getNews('https://timesofindia.indiatimes.com/city/bangalore','Bengaluru')
    dfcity = dfcity.append({'City':'Bengaluru','CrimeRate':NoCrime},ignore_index = True)

    NoCrime = getNews('https://timesofindia.indiatimes.com/city/kolkata','Kolkata')
    dfcity = dfcity.append({'City':'Kolkata','CrimeRate':NoCrime},ignore_index = True)

    NoCrime = getNews('https://timesofindia.indiatimes.com/city/amritsar','Amritsar')
    dfcity = dfcity.append({'City':'Amritsar','CrimeRate':NoCrime},ignore_index = True)

    values=dfcity['CrimeRate']
    labels=dfcity['City']
    legend="Daily Crime Rates"


    return render_template('index.html',values=values, labels = labels, legend=legend)

def prog_sent(news):

    typeOfCrime=""
    pattern1 = [r'\b(?i)'+'abduction'+r'\b',r'\b(?i)'+'assaulted'+r'\b',r'\b(?i)'+'rape'+r'\b',r'\b(?i)'+'abuse'+r'\b',r'\b(?i)'+'maltreatment'+r'\b',r'\b(?i)'+'rapine'+r'\b']
    pattern2 = [r'\b(?i)'+'bribe'+r'\b',r'\b(?i)'+'fraud'+r'\b',r'\b(?i)'+'cheat'+r'\b',r'\b(?i)'+'property'+r'\b',r'\b(?i)'+'fraudster'+r'\b',r'\b(?i)'+'swindler'+r'\b',r'\b(?i)'+'cheater'+r'\b',r'\b(?i)'+'trickster'+r'\b']
    pattern3 = [r'\b(?i)'+'Hitting'+r'\b',r'\b(?i)'+'slapping'+r'\b',r'\b(?i)'+'biting'+r'\b',r'\b(?i)'+'choking'+r'\b',r'\b(?i)'+'Aggressive'+r'\b']
    pattern4 = [r'\b(?i)'+'addictive'+r'\b',r'\b(?i)'+'heroin'+r'\b',r'\b(?i)'+'weed'+r'\b',r'\b(?i)'+'narcotics'+r'\b',r'\b(?i)'+'dope'+r'\b',r'\b(?i)'+'anesthetic'+r'\b']
    pattern5 = [r'\b(?i)'+'smuggling'+r'\b',r'\b(?i)'+'gunrunning'+r'\b',r'\b(?i)'+'gun'+r'\b',r'\b(?i)'+'bomb'+r'\b']
    pattern6 = [r'\b(?i)'+'capture'+r'\b',r'\b(?i)'+'hijack'+r'\b',r'\b(?i)'+'seize'+r'\b',r'\b(?i)'+'snatch'+r'\b',r'\b(?i)'+'steal'+r'\b',r'\b(?i)'+'lure'+r'\b']
    pattern7 = [r'\b(?i)'+'bloodshed'+r'\b',r'\b(?i)'+'homicide'+r'\b',r'\b(?i)'+'shooting'+r'\b',r'\b(?i)'+'kill'+r'\b',r'\b(?i)'+'slay'+r'\b']
    pattern8 = [r'\b(?i)'+'burglary'+r'\b',r'\b(?i)'+'embezzlement'+r'\b',r'\b(?i)'+'heist'+r'\b',r'\b(?i)'+'theft'+r'\b',r'\b(?i)'+'wrongdoing'+r'\b']
    
    output = []
    flag = 0
    for pat in pattern1:
        if re.search(pat, news) != None:
            typeOfCrime="Rape"
            output.append(typeOfCrime)
            break
    for pat in pattern2:
        if re.search(pat, news) != None:
            typeOfCrime="Financial Fraud"
            output.append(typeOfCrime)
            break
    for pat in pattern3:
        if re.search(pat, news) != None:
            typeOfCrime="Domestic violence"
            output.append(typeOfCrime)
            break
    for pat in pattern4:
        if re.search(pat, news) != None:
            typeOfCrime="Illegal drug trade"
            output.append(typeOfCrime)
            break
    for pat in pattern5:
        if re.search(pat, news) != None:
            typeOfCrime="Arms trafficking"
            output.append(typeOfCrime)
            break
    for pat in pattern6:
        if re.search(pat, news) != None:
            typeOfCrime="kidnapping"
            output.append(typeOfCrime)
            break
    for pat in pattern7:
        if re.search(pat, news) != None:
            typeOfCrime="Murder"
            output.append(typeOfCrime)
            break
    for pat in pattern8:
        if re.search(pat, news) != None:
            typeOfCrime="Robbery"
            output.append(typeOfCrime)
            break
    if len(output)>=1:
        return output
    else:
        return ""

def getNews(URL,city):

    global df
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    #list of crimes on indantimes 
    results = soup.find_all(class_='list5 clearfix')
    noCrime=0
    for ul in results:
        for li in ul.find_all('li'):
            link = li.find('a',href=True)
            if link != None:

                URL1 = URL+link['href']
                page1 = requests.get(URL1)
                soup = BeautifulSoup(page1.content, 'html.parser')
                results1 = soup.find("div",{'class':'_3Mkg- byline'})
                if results1 != None:
                    l1=results1.text.split("|")
                    l2=l1[len(l1)-1].split(',')
                    l2[0]=l2[0].replace('Updated:','')
                    results2 = soup.find("div",{'class':'ga-headlines'})
                    news = results2.text
                
                    if results2 != None:
                        typeOfCrime = prog_sent(news)
                        if len(typeOfCrime)>=1:
                            typeOfCrime=typeOfCrime[0]
                            noCrime+=1
                        else:
                            typeOfCrime=None
                        df = df.append({'Date' :l2[0] ,'Year':l2[1] , 'Time':l2[1],'City':city,'URL' :URL1 , 'Headline' :link['title'] ,'Type':typeOfCrime},ignore_index = True)
                        df=df.dropna(axis=0, how='any')
    print(noCrime)
                        
    return noCrime

if __name__ == '__main__':
    app.run()
