app = Flask(__name__)

@app.route("/")
def index():
    # Get the first 150 recipes (originally Pokémon) from the API
    response = requests.get("https://pokeapi.co/api/v2/pokemon?limit=150")
    data = response.json()
    recipe_list = data['results']
    
    # Create a list to hold recipe details
    recipes = []
    
    for recipe in recipe_list:
        # Each recipe URL looks like "https://pokeapi.co/api/v2/pokemon/1/"
        url = recipe['url']
        parts = url.strip("/").split("/")
        id = parts[-1]  # The last part is the recipe's ID
        
        # Create an image URL using the recipe's ID
        image_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{id}.png"
        
        recipes.append({
            'name': recipe['name'].capitalize(),
            'id': id,
            'image': image_url
        })
    
    # Send the recipe list to the index.html page
    return render_template("index.html", recipes=recipes)

# New route: When a user clicks a recipe card, this page shows more details and a stats chart
@app.route("/recipe/<int:id>")
def recipe_detail(id):
    # Get detailed info for the recipe using its id
    response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{id}")
    data = response.json()
    
    # Extract extra details like types, height, and weight
    types = [t['type']['name'] for t in data['types']]
    height = data.get('height')
    weight = data.get('weight')
    name = data.get('name').capitalize()
    image_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{id}.png"
    
    # Extract base stats for the chart (e.g., hp, attack, defense, etc.)
    stat_names = [stat['stat']['name'] for stat in data['stats']]
    stat_values = [stat['base_stat'] for stat in data['stats']]
    
    # Send all details to the recipe.html template
    return render_template("recipe.html", recipe={
        'name': name,
        'id': id,
        'image': image_url,
        'types': types,
        'height': height,
        'weight': weight,
        'stat_names': stat_names,
        'stat_values': stat_values
    })

if __name__ == '__main__':
    app.run(debug=True)
    