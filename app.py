from flask import Flask, render_template, request, jsonify
from groq import Groq
import sqlite3
import json

app = Flask(__name__)

client = Groq(api_key="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")
def init_db():
    conn = sqlite3.connect("history.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS analyses
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  brand_name TEXT,
                  review TEXT,
                  result TEXT,
                  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

init_db()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    brand_name = data.get("brand_name")
    review = data.get("review")

    prompt = f"""Analyze this consumer review for brand '{brand_name}' and provide:
1. Trust Score (0-100)
2. Consumer Adoption Level (Low/Medium/High)
3. Sentiment (Positive/Negative/Neutral)
4. Trust Violation Signals (list 3 points)
5. Key Insights (list 3 points)
6. Brand Health Score (0-100)

Review: {review}

Respond in JSON format only with keys: trust_score, adoption_level, sentiment, trust_violations, key_insights, brand_health_score"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    result = response.choices[0].message.content

    conn = sqlite3.connect("history.db")
    c = conn.cursor()
    c.execute("INSERT INTO analyses (brand_name, review, result) VALUES (?, ?, ?)",
              (brand_name, review, result))
    conn.commit()
    conn.close()

    return jsonify({"result": result})

@app.route("/history")
def history():
    conn = sqlite3.connect("history.db")
    c = conn.cursor()
    c.execute("SELECT brand_name, review, result, timestamp FROM analyses ORDER BY timestamp DESC LIMIT 10")
    rows = c.fetchall()
    conn.close()
    return jsonify({"history": rows})

if __name__ == "__main__":
    app.run(debug=True)