from flask import Flask, request, render_template, send_file, url_for
import os
from dotenv import load_dotenv
import pandas as pd
from utile.Timer import timer
load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') or 'abcd1234'

@timer()
def fac_ext(code, f_name):
    dataset = pd.read_csv(f'{f_name}')
    faculties = list(dataset[dataset['CCODE']==f'{code}']['EMPLOYEE NAME'].unique())
    df = pd.DataFrame(faculties)
    # df.to_csv(f"result.csv")
    return faculties, dataset[dataset["CCODE"] == code]["CNAME"].unique()[0]

@app.route('/',  methods=["POST", "GET"])
def home():
    lis = []
    code=""
    cname=""
    if request.method == "POST":
        code = request.form.get('code')
        code = code.upper()
        lis, cname = fac_ext(code, "m.csv")
        return render_template('index.html', lis=lis, code=code, cname=cname)
    else:
        return render_template('index.html', lis=lis, code=code, cname=cname)

    

@app.route('/download')
def download_file():
    return send_file(f"result.csv", as_attachment=True , mimetype='text/csv')




if __name__ == "__main__":
    app.run()