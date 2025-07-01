
from flask import Flask, request
import joblib 

app = Flask(__name__)

@app.route("/")
def titanic():
    
    
    pclass = request.args.get("pclass", "unknown") #1=1st,2=2nd,3=3rd
    sex = request.args.get("sex", "unknown")
    Age	= request.args.get("Age", "unknown")
    sibsp =	request.args.get("sibsp", "unknown") # of siblings 
    parch = request.args.get("parch", "unknown") # of parents 	
    ticket	= request.args.get("ticket", "unknown") # Ticket number	
    fare = request.args.get("fare", "unknown") # Passenger fare	
    cabin = request.args.get("cabin", "unknown") # Cabin number
    embarked = request.args.get("embarked", "unknown") # (Port of Embarkation	C = Cherbourg, Q = Queenstown, S = Southampton)
    
    x = [[pclass, sex, Age,sibsp, parch,ticket,fare,cabin,embarked]]
    
    model = joblib.load("titanic_model.pkl")
    prediction = model.predict(x)
    
    return prediction
    
    


app.run(debug=True)