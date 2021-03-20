# Johnson Lai / 1002298079 / CSCB20 A2
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def root():
    return "Welcome! It appears you have no name?"
    # return render_template('index.html')

@app.route('/<name>')
def generateResponse(name):
    reply = ''
    if hasNum(name):
        for letter in name:
            if not letter.isdigit():
                reply += letter
    else:
        for letter in name:
            if letter.isupper():
                reply += letter.lower()
            else:
                reply += letter.upper()

    return "Welcome, " + reply + ", to my CSCB20 website!"
    # return render_template('index.html', retrievedName = reply)
    # HTML has {{retrievedName}} in body, if this were to render an HTML site.

# Determine if there is a number in the String
def hasNum(string):
    return any(letter.isdigit() for letter in string)

if __name__ == '__main__':
    app.run(debug=True)