from flask import Flask, render_template

app = Flask(__name__)
@app.route('/')
def home():
    return render_template('index.html')

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