html = open("templates/index.html", "w", encoding="utf-8")
html.write("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Brand Trust Intelligence Dashboard</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/3.9.1/chart.min.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', sans-serif; background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); min-height: 100vh; color: white; }
        .navbar { background: rgba(255,255,255,0.05); padding: 15px 40px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255,255,255,0.1); }
        .navbar h1 { font-size: 22px; background: linear-gradient(90deg, #a78bfa, #60a5fa); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .container { max-width: 1100px; margin: 40px auto; padding: 0 20px; }
        .input-section { background: rgba(255,255,255,0.05); border-radius: 20px; padding: 40px; border: 1px solid rgba(255,255,255,0.1); margin-bottom: 30px; }
        .input-section h2 { font-size: 24px; margin-bottom: 25px; color: #a78bfa; }
        .form-group { margin-bottom: 20px; }
        label { display: block; margin-bottom: 8px; color: #94a3b8; font-size: 14px; }
        input, textarea { width: 100%; padding: 14px; background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15); border-radius: 10px; color: white; font-size: 15px; outline: none; }
        textarea { height: 120px; resize: none; }
        .analyze-btn { width: 100%; padding: 15px; background: linear-gradient(90deg, #a78bfa, #60a5fa); border: none; border-radius: 10px; color: white; font-size: 16px; font-weight: bold; cursor: pointer; }
        .results-section { display: none; }
        .cards-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-bottom: 30px; }
        .card { background: rgba(255,255,255,0.05); border-radius: 15px; padding: 25px; border: 1px solid rgba(255,255,255,0.1); text-align: center; }
        .card h3 { font-size: 13px; color: #94a3b8; margin-bottom: 10px; text-transform: uppercase; }
        .card .value { font-size: 36px; font-weight: bold; }
        .trust { color: #f87171; } .health { color: #34d399; }
        .charts-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 30px; }
        .chart-card { background: rgba(255,255,255,0.05); border-radius: 15px; padding: 25px; border: 1px solid rgba(255,255,255,0.1); }
        .chart-card h3 { margin-bottom: 15px; color: #a78bfa; }
        .insights-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
        .insight-card { background: rgba(255,255,255,0.05); border-radius: 15px; padding: 25px; border: 1px solid rgba(255,255,255,0.1); }
        .insight-card h3 { margin-bottom: 15px; color: #a78bfa; }
        .insight-card ul { list-style: none; }
        .insight-card ul li { padding: 8px 0; border-bottom: 1px solid rgba(255,255,255,0.05); font-size: 14px; color: #cbd5e1; }
        .loading { display: none; text-align: center; padding: 20px; color: #a78bfa; font-size: 16px; }
    </style>
</head>
<body>
    <div class="navbar">
        <h1>Brand Trust Intelligence Dashboard</h1>
        <span style="color: #94a3b8; font-size: 13px;">AI Powered Consumer Behavior Analysis</span>
    </div>
    <div class="container">
        <div class="input-section">
            <h2>Analyze Brand Trust & Consumer Behavior</h2>
            <div class="form-group">
                <label>Brand Name</label>
                <input type="text" id="brandName" placeholder="e.g. Apple, Nike, Amazon...">
            </div>
            <div class="form-group">
                <label>Consumer Review / Feedback</label>
                <textarea id="review" placeholder="Paste consumer review or feedback here..."></textarea>
            </div>
            <button class="analyze-btn" id="analyzeBtn">Analyze Now</button>
        </div>
        <div class="loading" id="loading">Analyzing consumer behavior...</div>
        <div class="results-section" id="results">
            <div class="cards-grid">
                <div class="card"><h3>Trust Score</h3><div class="value trust" id="trustScore">-</div></div>
                <div class="card"><h3>Brand Health Score</h3><div class="value health" id="healthScore">-</div></div>
                <div class="card"><h3>Consumer Adoption</h3><div class="value" id="adoptionLevel">-</div></div>
            </div>
            <div class="charts-grid">
                <div class="chart-card"><h3>Trust vs Health Score</h3><canvas id="barChart"></canvas></div>
                <div class="chart-card"><h3>Sentiment Analysis</h3><canvas id="doughnutChart"></canvas></div>
            </div>
            <div class="insights-grid">
                <div class="insight-card"><h3>Trust Violation Signals</h3><ul id="trustViolations"></ul></div>
                <div class="insight-card"><h3>Key Insights</h3><ul id="keyInsights"></ul></div>
            </div>
        </div>
    </div>
    <script>
        let barChartInstance = null;
        let doughnutChartInstance = null;
        document.getElementById("analyzeBtn").addEventListener("click", analyze);
        async function analyze() {
            const brandName = document.getElementById("brandName").value;
            const review = document.getElementById("review").value;
            if (!brandName || !review) { alert("Please enter both brand name and review!"); return; }
            document.getElementById("loading").style.display = "block";
            document.getElementById("results").style.display = "none";
            try {
                const response = await fetch("/analyze", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ brand_name: brandName, review: review })
                });
                const data = await response.json();
                let result = data.result;
                result = result.replace(/```json|```/g, "").trim();
                const parsed = JSON.parse(result);
                document.getElementById("trustScore").textContent = parsed.trust_score;
                document.getElementById("healthScore").textContent = parsed.brand_health_score;
                document.getElementById("adoptionLevel").textContent = parsed.adoption_level;
                const trustViolationsList = document.getElementById("trustViolations");
                trustViolationsList.innerHTML = "";
                parsed.trust_violations.forEach(v => { const li = document.createElement("li"); li.textContent = v; trustViolationsList.appendChild(li); });
                const keyInsightsList = document.getElementById("keyInsights");
                keyInsightsList.innerHTML = "";
                parsed.key_insights.forEach(i => { const li = document.createElement("li"); li.textContent = i; keyInsightsList.appendChild(li); });
                if (barChartInstance) barChartInstance.destroy();
                if (doughnutChartInstance) doughnutChartInstance.destroy();
                barChartInstance = new Chart(document.getElementById("barChart"), {
                    type: "bar",
                    data: { labels: ["Trust Score", "Brand Health"], datasets: [{ data: [parsed.trust_score, parsed.brand_health_score], backgroundColor: ["#f87171", "#34d399"] }] },
                    options: { plugins: { legend: { display: false } }, scales: { y: { min: 0, max: 100, ticks: { color: "#94a3b8" } }, x: { ticks: { color: "#94a3b8" } } } }
                });
                doughnutChartInstance = new Chart(document.getElementById("doughnutChart"), {
                    type: "doughnut",
                    data: { labels: [parsed.sentiment, "Other"], datasets: [{ data: [parsed.trust_score, 100 - parsed.trust_score], backgroundColor: ["#a78bfa", "#1e1b4b"] }] },
                    options: { plugins: { legend: { labels: { color: "#94a3b8" } } } }
                });
                document.getElementById("loading").style.display = "none";
                document.getElementById("results").style.display = "block";
            } catch(e) {
                document.getElementById("loading").style.display = "none";
                alert("Error: " + e.message);
            }
        }
    </script>
</body>
</html>""")
html.close()
print("Done!")