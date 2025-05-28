from flask import Flask, request, jsonify, render_template
from edamam_client import search_recipes

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q')
    if not query:
        return jsonify({'error': 'Missing query parameter `q`'}), 400

    diet = request.args.get('diet')
    cuisine = request.args.get('cuisineType')

    try:
        results = search_recipes(query, diet, cuisine)
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
