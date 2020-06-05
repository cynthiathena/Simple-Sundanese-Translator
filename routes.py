from flask import Flask, render_template, request, redirect
import test as func

app = Flask(__name__)

#menu utama 
@app.route('/')
def cover():
    return render_template('cover.html')

@app.route('/indo', methods=['GET','POST'])
def indo():
    res = ""
    inp = ""
    if request.method == "POST" :
        tipe = "Bahasa Indonesia"
        algoritma = request.form["algoritma"]
        inp = request.form["input"]
        res = func.run(tipe, inp, algoritma)
        return render_template("indo.html", result=res, input=inp)
    return render_template("indo.html", result=res, input=inp)

@app.route('/sunda', methods=['GET','POST'])
def sunda():
    res = ""
    inp = ""
    if request.method == "POST" :
        tipe = "Bahasa Sunda"
        algoritma = request.form["algoritma"]
        inp = request.form["input"]
        res = func.run(tipe, inp, algoritma)
        return render_template("sunda.html", result=res, input=inp)
    return render_template("sunda.html", result=res, input=inp)

if __name__ =="__main__":
    app.run(debug=True,port=8080)
        