from flask import Flask,render_template,request

app = Flask(__name__)
@app.route('/')
def index():
    word = request.args.get('word')
    return render_template('time_attack.html',word=word)

@app.route('/result',methods=['GET'])
def check():
    word = request.args.get('word')
    ms = request.args.get('ms')
    print('%s,%s'%(word,ms))
    return "asd"

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5001)