from flask import Flask, request, render_template
import numpy as np
import pandas as pd
from sklearn import metrics 
import warnings
import pickle
import requests
import os
warnings.filterwarnings('ignore')
from feature import FeatureExtraction
import json

#file = open("model.pkl", "rb")
#gbc = pickle.load(file)
#file.close()



API_KEY="45JdlIfSqHAGFG36tbomvffhiSi69OyCYuGUKw3_0kpN"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token'
                               , data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}


app = Flask(__name__)

@app.route("/")
def home():
     return render_template("home.html")


@app.route("//index")
def index():
    return render_template("index.html", xx =-1)
@app.route("/result", methods=["GET", "POST"])
def result():
    if request.method == "POST":
    
        url = request.form["url"]
        obj = FeatureExtraction(url)
        x = np.array(obj.getFeaturesList()).reshape(1,31)
        x1= x.tolist()

      
        payload_scoring = {"input_data": [{"field": [["index","UsingIP","LongURL","ShortURL","Symbol@","Redirecting//","PrefixSuffix-","SubDomains","HTTPS","DomainRegLen","Favicon","NonStdPort","HTTPSDomainURL","RequestURL","AnchorURL","LinksInScriptTags","ServerFormHandler","InfoEmail","AbnormalURL","WebsiteForwarding","StatusBarCust","DisableRightClick","UsingPopupWindow","IframeRedirection","AgeofDomain","DNSRecording","WebsiteTraffic","PageRank","GoogleIndex","LinksPointingToPage","StatsReport"
]], "values":x1}]}
        response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/1ce91725-cf1d-43e4-aeba-24ea24ee2980/predictions?version=2022-11-19', json=payload_scoring,
 headers={'Authorization': 'Bearer ' + mltoken})
        print("Scoring response")
        predictions=response_scoring.json()
        print(x1)
        print(predictions)     
        print(predictions['predictions'][0]['values'][0][1])

        y_pro_non_phishing = predictions['predictions'][0]['values'][0][1][1]
 # if(y_pred ==1 ):
        #pred = "It is {0:.2f} % safe to go ".format(y_pro_phishing*100)
        return render_template('index.html',xx=y_pro_non_phishing,url=url )


    



if __name__ == "__main__":
    app.run(debug=True,port=2002)