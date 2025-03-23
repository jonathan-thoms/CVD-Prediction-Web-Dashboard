from flask import Flask, render_template, request, jsonify
import requests
import pandas as pd
import plotly.express as px

app = Flask(__name__)

# Replace with your latest ngrok API URL
API_URL = "https://f593-116-68-110-183.ngrok-free.app/predict"

# Dictionary of health recommendations based on risk factors
HEALTH_SUGGESTIONS = {
    "bmi": "Maintaining a healthy BMI through balanced diet and regular exercise can lower cardiovascular risk.",
    "chol": "High cholesterol increases heart disease risk. Consider reducing saturated fats and increasing fiber intake.",
    "trestbps": "High blood pressure can strain the heart. Reduce sodium intake, manage stress, and exercise regularly.",
    "diabp": "Elevated diastolic BP can indicate heart strain. Monitor it closely and maintain a heart-healthy lifestyle.",
    "glucose": "High glucose levels may indicate diabetes risk. Maintain a low-sugar diet and stay physically active.",
    "smoking": "Smoking is a major risk factor. Quitting can significantly improve heart health and overall well-being.",
    "alcohol": "Excess alcohol intake can raise blood pressure. Limit consumption to recommended levels.",
    "exercise": "Regular exercise improves heart function and reduces disease risk. Aim for at least 30 minutes a day."
}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Get user input
        user_input = {key: float(request.form[key]) for key in request.form}

        # Send request to API
        response = requests.post(API_URL, json=user_input)
        api_result = response.json()

        # Extract API response data
        prediction = api_result.get("prediction", "Unknown")
        probability = api_result.get("probability", 0)
        factors = api_result.get("important_factors", [])

        # Generate a detailed explanation
        explanation = f"The model predicts a **{prediction} ({probability * 100}%)** risk of cardiovascular disease. "
        explanation += "The key influencing factors are: "

        for factor in factors:
            explanation += f"\n- **{factor.capitalize()}**: {HEALTH_SUGGESTIONS.get(factor, 'Consider improving this health metric.')}"

        # Generate a bar chart for SHAP factors
        df = pd.DataFrame({"Factor": factors, "Impact": [1, 1, 1]})  # Dummy impact values
        fig = px.bar(df, x="Impact", y="Factor", orientation="h", title="Top 3 Risk Factors")
        graph_html = fig.to_html(full_html=False)

        return jsonify({
            "prediction": prediction,
            "probability": probability,
            "explanation": explanation,
            "graph": graph_html
        })

    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == "__main__":
    app.run(debug=True, port=5001)
