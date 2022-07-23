from flask import Flask

app=Flask(__name__)

@app.route("/",methods=['GET','POST'])
def index():
    return "It's ML Credit card Defaulters project"

if __name__=="__main__":
    app.run(port=5001)




    