from flask import Flask, escape, request, render_template
import pickle
import numpy as np

app = Flask(__name__)
test_model= pickle.load(open('loan_predictions.sav', 'rb'))

@app.route('/')
def home():
    return render_template("page.html")


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method ==  'POST':
        Gender = request.form['Gender']
        Married = request.form['Married']
        Dependents = request.form['Dependents']
        Education = request.form['Education']
        Self_Employed = request.form['Self_Employed']
        Credit_History =float( request.form['Credit_History'])
        Property_Area = request.form['Property_Area']
        ApplicantIncome = float(request.form['ApplicantIncome'])
        CoapplicantIncome =float( request.form['CoapplicantIncome'])
        LoanAmount = float(request.form['LoanAmount'])
        Loan_Amount_Term = float(request.form['Loan_Amount_Term'])

        # gender
        if (Gender == "Male"):
            male=1
        else:
            male=0
        
        # married
        if(Married=="Yes"):
            married_yes = 1
        else:
            married_yes=0

        # dependents
        if(Dependents=='1'):
            dependents_1 = 1
            dependents_2 = 0
            dependents_3 = 0
        elif(Dependents == '2'):
            dependents_1 = 0
            dependents_2 = 1
            dependents_3 = 0
        elif(Dependents=="3+"):
            dependents_1 = 0
            dependents_2 = 0
            dependents_3 = 1
        else:
            dependents_1 = 0
            dependents_2 = 0
            dependents_3 = 0  

        # education
        if (Education=="Not Graduate"):
            not_graduate=1
        else:
            not_graduate=0

        # employed
        if (Self_Employed == "Yes"):
            employed_yes=1
        else:
            employed_yes=0

        # property area

        if(Property_Area=="Semiurban"):
            semiurban=1
            urban=0
        elif(Property_Area=="Urban"):
            semiurban=0
            urban=1
        else:
            semiurban=0
            urban=0


        ApplicantIncomelog = np.log(ApplicantIncome)
        totalincomelog = np.log(ApplicantIncome+CoapplicantIncome)
        LoanAmountlog = np.log(LoanAmount)
        Loan_Amount_Termlog = np.log(Loan_Amount_Term)

        prediction = test_model.predict([[Credit_History, ApplicantIncomelog,LoanAmountlog, Loan_Amount_Termlog, totalincomelog, male, married_yes, dependents_1, dependents_2, dependents_3, not_graduate, employed_yes,semiurban, urban ]])

        # print(prediction)

        if(prediction=="N"):
            prediction="Not be approved"
        else:
            prediction="be approved"


        return render_template("page.html", prediction_text="Loan will {}".format(prediction))




   


if __name__ == "__main__":
    app.run(debug=True)