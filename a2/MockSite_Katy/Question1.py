from flask import Flask
app = Flask(__name__)

@app.route('/<name>')
def generateResponse(name):
    temp = ''
    if name.isalpha():
        temp = name.swapcase()
    else:
        for char in name:
            if char.isalpha():
                temp += char

    return 'Welcome %s, to my CSCB20 website!' % temp

if __name__ == "__main__":
    app.run()