from flask import Flask, render_template, redirect, url_for, request

#Add the API key
API_KEY = "XXXXXXXXXXXXXX"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={
"apikey": API_KEY, 
"grant_type": 'urn:ibm:params:oauth:grant-type:apikey'
})
mltoken = token_response.json()["access_token"]
 header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

app = Flask(__name__)

@app.route("/", methods = ['POST', 'GET'])
def index():
    if request.method == 'POST':
        arr = []
        for i in request.form:
            val = request.form[i]
            if val == '':
                return redirect(url_for("index"))
            arr.append(float(val))
       
        payload_scoring = {
            "input_data": [{"fields":[  'GRE Score',
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
          'XXXXXXXXXXXXXXXXXXXXXX'#Add the API key from Deployment
          json=payload_scoring,
            headers=header
        ).json()
        
        result = response_scoring['predictions'][0]['values']
        
        if result[0][0] > 0.5:
            return redirect(url_for('chance', percent=result[0][0]*100))
        else:
            return redirect(url_for('no_chance', percent=result[0][0]*100))
    else:
        return redirect(url_for("index"))

@app.route("/home")
def demo2():
    return render_template("index.html")

@app.route("/chance/<percent>")
def chance(percent):
    return render_template("chance.html", content=[percent])

@app.route("/nochance/<percent>")
def no_chance(percent):
    return render_template("noChance.html", content=[percent])

@app.route('/<path:path>')
def catch_all():
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run()
