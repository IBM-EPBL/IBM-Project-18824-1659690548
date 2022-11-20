# Import necessary libraries

from flask import Flask, render_template, redirect, url_for, request
import requests
app = Flask(__name__)


@app.route("/")
def index():
     return render_template("index.html")

@app.route("/predict", methods=['POST', 'GET'])
# @app.route("/predict.html", methods = ['POST', 'GET'])
def predict():
    if request.method == 'POST':
        arr = []
        for i in request.form:
            val = request.form[i]
            if val == '':
                return redirect(url_for("predict"))
            arr.append(float(val))

        # Add the API key
        # API_KEY = "zzzzzzzzz"
        API_KEY = "zzzz"
        token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={
            "apikey": API_KEY,
            "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'
        })
        mltoken = token_response.json()["access_token"]
        header = {'Content-Type': 'application/json',
                  'Authorization': 'Bearer ' + mltoken}
        
        payload_scoring = {
            "input_data": [{"fields": ['GRE Score',
                                       'TOEFL Score',
                                       'University Rating',
                                       'SOP',
                                       'LOR ',
                                       'CGPA',
                                       'Research'],
                            "values": [arr]
                            }]
        }

        response_scoring = requests.post(
             
            'https://eu-de.ml.cloud.ibm.com/ml/v4/deployments/9aecac79-02b8-4ad2-955c-ff801c4bc43c/predictions?version=2022-11-17',
            json=payload_scoring,
            headers=header).json()
     
        result = response_scoring['predictions'][0]['values']

        if result[0][0] > 0.82:
            return redirect(url_for('chance', percent= round((result[0][0]*100), 2)))
        else:
            return redirect(url_for('no_chance', percent= round((result[0][0]*100), 2)))
    else:
        return redirect(url_for("demo"))


@app.route("/home")
def demo():
    return render_template("index.html")


@app.route("/index.html#about")
def about():
    return render_template("index.html#about")
    
@app.route("/index.html#team")
def team():
    return render_template("index.html#team")
    
@app.route("/index.html#contact")
def contact():
    return render_template("index.html#contact")

@app.route("/login")
def login():
    return render_template("signup.html")


@app.route("/signup.html")
def signup():
    return render_template("signup.html")


@app.route("/predict.html")
def predictPage():
    return render_template("predict.html")


@app.route("/chance/<percent>")
def chance(percent):
    return render_template("chance.html", content=[percent])


@app.route("/nochance/<percent>")
def no_chance(percent):
    return render_template("noChance.html", content=[percent])


@app.route('/<path:path>')
def catch_all():
    return redirect(url_for("demo"))


if __name__ == "__main__":
    app.run(debug=False)
