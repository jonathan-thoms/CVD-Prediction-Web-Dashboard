from flask import Flask, render_template, request, jsonify
import requests
import pandas as pd
import plotly.express as px

app = Flask(__name__)

# Replace with your latest ngrok URL for the API
API_URL = "https://your-ngrok-url.ngrok.io/predict"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Get user input from form
        user_input = {key: float(request.form[key]) for key in request.form}

        # Send request to API
        response = requests.post(API_URL, json=user_input)
        api_result = response.json()

        # Extract response data
        prediction = api_result.get("prediction", "Unknown")
        probability = api_result.get("probability", 0)
        factors = api_result.get("important_factors", [])

        # Generate a bar chart for important factors
        df = pd.DataFrame({"Factor": factors, "Impact": [1, 1, 1]})  # Dummy values
        fig = px.bar(df, x="Impact", y="Factor", orientation="h", title="Top 3 Risk Factors")
        graph_html = fig.to_html(full_html=False)

        return jsonify({
            "prediction": prediction,
            "probability": probability,
            "graph": graph_html
        })

    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == "__main__":
    app.run(debug=True, port=5001)
