from flask import Flask, logging
from flask_ask import Ask, statement, question, session, request
import json
import requests
import time
import unidecode
from flask_ask import session
app = Flask(__name__)
ask = Ask(app, "/alexa")
log = logging.getLogger()

def get_headlines():
    user_pass_dict = {'user': '',
                      'passwd': '',
                      'api_type': 'json'}
    sess = requests.Session()
    sess.headers.update({'User-Agent': 'I am testing Alexa: Sentdex'})
    sess.post('https://www.reddit.com/api/login', data=user_pass_dict)
    time.sleep(1)
    url = 'https://reddit.com/r/worldnews/.json?limit=10'
    html = sess.get(url)
    data = json.loads(html.content.decode('utf-8'))
    titles = [unidecode.unidecode(listing['data']['title']) for listing in data['data']['children']]
    titles = '... '.join([i for i in titles])
    return titles


@app.route('/')
def homepage():
    return "hello, this is route for alexa"





@ask.launch
def start_skill():
    print(session)
    status=False
    if 'accessToken' in session['user']:
        status=True

    if(status==True):
        return statement("welcome! How i can help")
    else:
        return statement('Please link your account in the Alexa app') \
        .link_account_card()


@ask.intent("YesIntent")
def share_headlines():

    headlines = get_headlines()
    headline_msg = 'The current world news headlines are {}'.format(headlines)
    return statement(headline_msg)


@ask.intent("NoIntent")
def no_intent():
    bye_text = 'I am not sure why you asked me to run then, but okay... bye'
    return statement(bye_text)


if __name__ == '__main__':
    app.run(debug=True)
