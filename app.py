import math
from flask import Flask, render_template, request
from rdflib import Graph, Namespace

app = Flask(__name__)

# Load the ontology
g = Graph()
g.parse("AreaOfShapes.owl", format="xml")

# Namespace for the ontology
ns = Namespace("http://www.example.org/AreaOfShapes#")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get the selected shape
        shape = request.form.get("shape", "")

        # Parse dimensions, ignoring empty fields
        dimensions = {key: float(value) for key, value in request.form.items() if key != "shape" and value.strip()}

        # Ensure all required dimensions for the shape are provided
        required_dimensions = {
            "Rectangle": ["length", "width"],
            "Triangle": ["base", "height"],
            "Circle": ["radius"]
        }

        missing_dimensions = [
            dim for dim in required_dimensions.get(shape, []) if dim not in dimensions
        ]

        if missing_dimensions:
            return render_template(
                "index.html",
                error=f"Missing dimensions: {', '.join(missing_dimensions)}",
                shape=shape,
                dimensions=dimensions
            )

        # Query to get the formula for the selected shape
        formula_query = f"""
        SELECT ?expression
        WHERE {{
            <{ns[shape]}> <http://www.example.org/AreaOfShapes#usesFormula> ?formula .
            ?formula <http://www.example.org/AreaOfShapes#formulaExpression> ?expression .
        }}
        """
        formula = None
        for row in g.query(formula_query):
            formula = str(row.expression)

        # Replace dimensions in the formula and calculate the area
        if formula:
            try:
                for dim, value in dimensions.items():
                    formula = formula.replace(dim, str(value))
                formula = formula.replace("^", "**")
                area = eval(formula, {"__builtins__": None}, {"pi": math.pi})

                # Prepare descriptive message
                dimension_text = ", ".join(f"{dim}={value} units" for dim, value in dimensions.items())
                result_message = f"The area of the {shape.lower()} with {dimension_text} is {area} square units."

                return render_template(
                    "index.html",
                    area_message=result_message,
                    shape=shape,
                    dimensions=dimensions
                )
            except Exception as e:
                return render_template(
                    "index.html",
                    error=f"Error calculating area: {e}",
                    shape=shape,
                    dimensions=dimensions
                )

    return render_template("index.html", area_message=None, shape=None, dimensions={})


if __name__ == "__main__":
    app.run(debug=True)
