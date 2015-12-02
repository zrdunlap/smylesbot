import json, os, random
from slackclient import SlackClient
from flask import Flask, request
from pygoogle import pygoogle

# Initiate the Flask app which the slash command /askstuart interacts with
app = Flask(__name__)

@app.route("/", methods = ['GET'])
def reply():
    '''
     The slash command from flask sends a POST with data such as the request text, channel origination, user info and others,
     this data is being retrieved using Flask request since it comes through as a URL variable
    '''
    text = request.args.get('text')
    channel = request.args.get('channel_name')
    user_id = request.args.get('user_id')
    user_name = request.args.get('user_name')
    # These are some Stuart-isms for fun :-)
    flavor_text = ['"There are only two hard things in Computer Science: cache invalidation and naming things."',
                   '"Perhaps, these links will help?"',
                   '"According to Aristotle, In a race, the quickest runner can never overtake the slowest, since the pursuer must first reach the point whence the pursued started, so that the slower must always hold a lead."',
                   '"Maybe one of these three links can help?"',
                   '"Could we consider some other options? One of these, maybe?"',
                   '"Interesting."',
                   '"Have you looked on SharePoint?"',
                   '"That\'s not bad, but I might suggest:"',
                   '"I hear what you\'re saying, but I don\'t totally agree. How about we try one of these?"',
                   '"That is a very brave proposal. However, have you considered any of these?"',
                   '"Not sure that\'s giphy-supported.  Try one of these:"',
                   '"I see what you\'re getting at but I\'m not sure that\'s right. Take a look at one of these."',
                   '"Your answer is probably the SWARM. But until that\'s ready, try these:"']
    '''
     When a user runs the slash command, this script makes a random choice from the flavor_text (Stuart-isms),
     calls the necessary environment variable on the machine hosting the script to get the necessary Slack token
     Using the pygoogle library the search text from the slash command is searhced against google
     The response is limited to 1 page for brevity, the URLs are retireve for the first 3 search results and returned
     The return is sent back to slack privately to the user
    '''
    flavor_random = random.choice(flavor_text)
    sc = SlackClient(os.environ['slack_token'])
    g = pygoogle(text)
    g.pages = 1
    search_response = g.get_urls()
    return flavor_random + '\n'+ 'Your query was: ' + text + '\n' + '\n'.join(search_response[:3])

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
