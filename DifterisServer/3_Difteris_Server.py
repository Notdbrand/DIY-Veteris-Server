from flask import Flask, jsonify, request
import json
import random
import os

app = Flask(__name__)

def load_json_data(filename):
    with open(filename, 'r') as json_file:
        return json.load(json_file)

apps_data = load_json_data('data/apps.json')
categories_data = load_json_data('data/categories.json')

def get_apps_by_category(category):
    return [app for app in apps_data['applications'] if app['category'] == category]

def get_app_details_by_bundleid(bundleid):
    for app in apps_data['applications']:
        if app['bundleid'] == bundleid:
            return app.copy()
    return None

@app.route('/1.1/client/updates', methods=['GET'])
def update():
    response = {
        "clientUpdates": "No updates bro"
    }
    return jsonify(response)

@app.route('/1.1/listing/recommended', methods=['GET'])
def recommended():
    recommended_apps = random.sample(apps_data['applications'], min(50, len(apps_data['applications'])))
    response = {
        "applications": recommended_apps
    }
    return jsonify(response)

@app.route('/1.1/listing/all', methods=['GET'])
def all_apps():
    response = {
        "applications": apps_data['applications']
    }
    return jsonify(response)

@app.route('/1.1/listing/app/<string:bundleid>', methods=['GET'])
def app_details(bundleid):
    app_info = get_app_details_by_bundleid(bundleid)
    if app_info:
        return jsonify(app_info)
    else:
        return jsonify({"error": "NO"}), 404

@app.route('/1.1/listing/categories', methods=['GET'])
def categories():
    response = {
        "categories": categories_data['categories']
    }
    return jsonify(response)

@app.route('/1.1/listing/category/<int:category_number>', methods=['GET'])
def category(category_number):
    apps_in_category = get_apps_by_category(category_number)
    response = {
        "applications": [
            {
                "bundleid": app['bundleid'],
                "name": app['name'],
                "iconurl": app.get('iconurl'),
                "developer": app['developer'],
                "versions": app['versions']
            }
            for app in apps_in_category
        ]
    }
    return jsonify(response)

@app.route('/1.1/listing/suggest', methods=['GET'])
def suggest():
    query = request.args.get('query', '')
    filtered_apps = [app for app in apps_data['applications'] if query.lower() in app['name'].lower()]
    response = {
        "applications": [
            {
                "bundleid": app['bundleid'],
                "name": app['name'],
            }
            for app in filtered_apps
        ]
    }
    return jsonify(response)

@app.route('/static/IPAs/<string:bundleid>.ipa', methods=['GET'])
def serve_ipa(bundleid):
    app_info = get_app_details_by_bundleid(bundleid)
    if app_info:
        ipa_file_path = f"static/IPAs/{app_info['bundleid']}.ipa"
        if os.path.exists(ipa_file_path):
            return send_file(ipa_file_path, as_attachment=True)
        else:
            return jsonify({"error": "IPA file not found"}), 404
    else:
        return jsonify({"error": "App not found"}), 404

@app.route('/status', methods=['GET'])
def status():
    return jsonify({"status": "online"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5010)
# You reviewed the code :D
# -NDB