from flask import Flask, render_template
from parallel import run_parallel
from visualization import plot_results

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/run")
def run_simulation():
    results = run_parallel()
    
    # Generate graph
    plot_results(results)
    
    return render_template("index.html", results=results, graph=True)

if __name__ == "__main__":
    app.run(debug=True)