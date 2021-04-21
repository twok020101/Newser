import requests
import json
import time
import datetime
from decouple import config


#Initilize Connection
def connection():
    url = "https://google-news.p.rapidapi.com/v1/top_headlines"

    querystring = {"lang":"en","country":"IN"}

    headers = {
        'x-rapidapi-key': config('KEY'),
        'x-rapidapi-host': "google-news.p.rapidapi.com"
        }
    
    try:
        response = requests.request("GET",url,headers=headers,params=querystring)
    except requests.exceptions.RequestException as e:
        print("Exception: ",e)
    
    print("Connected")
    
    return response.text

#Parsing JSON file to readable format
def parse_output(NewsDict):
    FinalDict={}
    try:
        for item in NewsDict['articles']:
            thisTitle = item['title']
            thisLink = item['link']
            FinalDict[thisTitle]=thisLink

        print("Converted")
        return FinalDict
    except Exception as e:
        print("Please wait for some time! \n",NewsDict['message'])
        return None

#Telegram group message sender
def telegram_sender(Message,number):
    try:
        print("Sending",number)
        base_url='https://api.telegram.org/bot{0}/sendMessage?chat_id={1}&text="{2}"'.format(config('BOT_ID'),config('CHAT_ID'),Message)
        requests.get(base_url)
    except Exception as e:
        print("Exception: ",e)


#Main function
def main():
    TotalNewsCovered=0
    while(True):
        #Gets news in JSON format
        NewsDict=json.loads(connection())
        #Parsing and output
        FinalDict=parse_output(NewsDict)
        if (FinalDict!=None):
            final_string=""
            i=0
            # for x in range(ceil(len(FinalDict.keys())//4)):
            for i,news in enumerate(FinalDict.keys()):
                final_string=(str(i+1)+": "+ news + "\nFor more information click on the link: " + FinalDict[news] +"\n")
                telegram_sender(final_string,i)
        TotalNewsCovered+=i
        time.sleep(3600*0.5)


#Main function!
if __name__=="__main__":
    main()