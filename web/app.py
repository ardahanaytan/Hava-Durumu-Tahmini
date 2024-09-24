from flask import Flask, render_template
import sys
sys.path.append('/Users/ardahanaytan/Desktop/STAJ/Hava Durumu Tahmin Projesi/models')
from model_basinc import basinc_forecast
from model_bulut import bulut_forecast
from model_kar import kar_forecast
from model_nem import nem_forecast
from model_ruzgar_hizi import ruzgarhizi_forecast
from model_ruzgar_yonu import ruzgaryonu_forecast
from model_sicaklik import sicaklikmin_forecast, sicaklikmax_forecast
from model_yagmur import yagmur_forecast


app = Flask(__name__)
@app.route('/')
def home():
    df_basinc_dict = basinc_forecast.to_dict(orient='records')
    df_bulut_dict = bulut_forecast.to_dict(orient='records')
    df_kar_dict = kar_forecast.to_dict(orient='records')
    df_nem_dict = nem_forecast.to_dict(orient='records')
    df_ruzgarhizi_dict = ruzgarhizi_forecast.to_dict(orient='records')
    df_ruzgaryonu_dict = ruzgaryonu_forecast.to_dict(orient='records')
    df_sicaklikmin_dict = sicaklikmin_forecast.to_dict(orient='records')
    df_sicaklikmax_dict = sicaklikmax_forecast.to_dict(orient='records')
    df_yagmur_dict = yagmur_forecast.to_dict(orient='records')

    return render_template('index.html', df_basinc_dict=df_basinc_dict, df_bulut_dict=df_bulut_dict, df_kar_dict=df_kar_dict, df_nem_dict=df_nem_dict, df_ruzgarhizi_dict=df_ruzgarhizi_dict, df_ruzgaryonu_dict=df_ruzgaryonu_dict, df_sicaklikmin_dict=df_sicaklikmin_dict, df_sicaklikmax_dict=df_sicaklikmax_dict, df_yagmur_dict=df_yagmur_dict)

@app.route('/amsterdam')
def amsterdam():
    return render_template('amsterdam.html')

@app.route('/berlin')
def berlin():
    return render_template('berlin.html')

@app.route('/istanbul')
def istanbul():
    return render_template('istanbul.html')

@app.route('/londra')
def londra():
    return render_template('londra.html')

@app.route('/madrid')
def madrid():
    return render_template('madrid.html')

@app.route('/paris')
def paris():
    return render_template('paris.html')

@app.route('/roma')
def roma():
    return render_template('roma.html')

@app.route('/raporlar')
def raporlar():
    return render_template('raporlar.html')

if __name__ == '__main__':
    app.run(debug=True)