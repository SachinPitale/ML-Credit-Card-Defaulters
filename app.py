from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin

app=Flask(__name__)


@app.route('/',methods=['GET'])  # route to display the home page
@cross_origin()
def homePage():
    return render_template("index.html")

if __name__=="__main__":
    app.run(port=5000)




    