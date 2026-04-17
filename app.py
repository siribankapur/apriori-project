from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <h2>Apriori Algorithm</h2>
    <form action="/run">
        Input File: <input name="file" value="1000-out1.csv"><br>
        Min Support: <input name="minsup" value="20"><br>
        <input type="submit">
    </form>
    '''

@app.route('/run')
def run():
    file = request.args.get('file')
    minsup = request.args.get('minsup')

    import subprocess
    output = subprocess.getoutput(f"python3 apriori_2932103.py -i {file} -m {minsup}")

    return f"<pre>{output}</pre>"

app.run()
