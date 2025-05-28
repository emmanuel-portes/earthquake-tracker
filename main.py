from flask import Flask, jsonify, request

app: Flask = Flask(__name__)

@app.route('/home', methods = ['GET'])
def home():
	data: dict = dict()
	if request.method == 'GET':
		data.setdefault('message','hello from homepage')
	
	return jsonify(data)

if __name__ == '__main__':
	app.run(debug=True)

