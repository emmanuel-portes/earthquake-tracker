from flask import Flask, jsonify, request

app: Flask = Flask(__name__)

features: list = [
	{ "id": "tx2024kwiw",
		"type": "feature",
		"place": "55 km S of Whites City, New Mexico"
		},
	{ "id": "nm60584281",
		"type": "feature",
		"place": "84 km NW of Karluk, Alaska"
	},
	{ "id": "av93010189",
		"type": "feature",
		"place":"8 km NNW of The Geysers, CA"
	}
] 

@app.route('/home', methods = ['GET'])
def home():
	data: dict = {'message':'features homepage'}
	if request.method == 'GET':
		return jsonify(data)

@app.route('/features', methods = ['GET'])
def get_all_features():
	if request.method == 'GET':
		return jsonify(features)

@app.route('/features/<id>', methods = ['GET'])
def get_feature_by_id(id: str):
	if request.method == 'GET':
		for feature in features:
			if feature.get('id') == id:
				return jsonify(feature)

if __name__ == '__main__':
	app.run(debug=True)

