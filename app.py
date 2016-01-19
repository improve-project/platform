from AnalysisPackage import analysishandler
from flask import Flask, jsonify, request
app = Flask(__name__)

#############################################
from database_handler import DatabaseHandler 


database = DatabaseHandler()

#############################################

@app.route('/')
def hello_world():
    return 'Running!'

@app.route('/api/v1/analysis/analysisModules')
def get_modules():
	#TODO: Handle username
	try:
		modules = analysishandler.get_available_analysis_modules("root", database)
	except Exception as e:
		print "Something went wrong. Error message: "
		print e

	return jsonify(modules)

@app.route('/api/v1/analysis/analysisModules/<string:moduleName>/start', methods=['POST'])
def analyse(moduleName):
	#TODO: Handle username
	settings = request.json
	try:
		msg = analysishandler.perform_analysis("Evalan_u_1", moduleName, settings, database)
	except Exception as e:
		print "Something went wrong. Error message: "
		print e
	return jsonify({"status": msg}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080)

