from flask import Flask,request,render_template,jsonify


app = Flask(__name__)

@app.route("/",methods=['POST','GET'])
def hello():
    
    return render_template("index.html")


@app.route("/among-us")
def among_us():
    print("This is print among us which is not printed on webpage")
    return "Hehehe..."

@app.route("/demo",methods=['POST'])
def math_operations():
    if(request.method == 'POST'):
        operation = request.json['operation']
        num1= request.json['num1']
        num2 = request.json['num2']
        result = 0
        if operation == "add":
            result = num1 + num2
        elif operation == "multiply":
            result = num1 * num2
        elif operation == "division":
            if num2!=0:
                result = num1 / num2
            else:
                result=0
        elif operation == "subtraction":
            result = num1 - num2

    # return f"{operation} is applied between {num1} and {num2} answer is {result}"
        
    return jsonify(f"{operation} is applied between {num1} and {num2} answer is {result}")



@app.route("/operations",methods=['POST'])
def math_operations_ops():
    if(request.method == 'POST'):
        operation = request.form['operation']
        try:
            num1= int(float(request.form['num1']))
        except ValueError:
            num1 = 0
        try:    
            num2 = int(float(request.form['num2']))
        except ValueError: 
            num2 = 0

        result = 0
        if operation == "add":
            result = num1 + num2
        elif operation == "multiply":
            result = num1 * num2
        elif operation == "division":
            if num2!=0:
                result = num1 / num2
            else:
                result=0
        elif operation == "subtraction":
            result = num1 - num2
        else:
            result = 0

    # return f"{operation} is applied between {num1} and {num2} answer is {result}"
        
    return render_template("result.html",result=[result,num1,num2,operation])



@app.route("/multiply",methods=['POST'])
def math_operations_multiply():
    if(request.method == 'POST'):
        operation = request.json['operation']
        num1= request.json['num1']
        num2 = request.json['num2']
        result = 0
        if operation == "multiply":
            result= num1 * num2
    return f"{operation} is applied and answer is {result}"


if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0",port=5001) 