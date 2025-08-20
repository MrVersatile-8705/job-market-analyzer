from flask import Flask, render_template
import pandas as pd
import json

app = Flask(__name__)

# Load the analysis results
def load_analysis_results():
    with open('data/results/analysis_results.json') as f:
        return json.load(f)

# Route for the dashboard
@app.route('/')
def dashboard():
    results = load_analysis_results()
    return render_template('dashboard.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)