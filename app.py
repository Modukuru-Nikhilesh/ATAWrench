# ATAWrench
# Tagline: Fix ATA codes with ATAWrench — drench your brain in aviation maintenance.

from flask import Flask, render_template, jsonify, request
from ata_skill import AviationATASkill

app = Flask(__name__)

try:
    skill = AviationATASkill("ata_database.json")
    print("✅ ATAWrench database loaded successfully!")
except Exception as e:
    print("❌ ATAWrench ERROR loading database:", e)
    raise

def generate_advisory(data, keywords):
    name = data.get("name", "System")
    code = data.get("ata_code", "")
    manuals = data.get("manuals") or ["the AMM"]
    components = data.get("components") or ["the primary component"]
    actions = data.get("corrective_actions") or ["perform a thorough visual inspection"]
    kw = ", ".join(keywords) if keywords else "general anomaly"
    return (
        f"As a senior maintenance engineer reviewing the {name} system (ATA {code}), "
        f"your reported keywords '{kw}' suggest a specific anomaly requiring targeted attention. "
        f"To proceed safely, isolate the {components[0]} and initiate the troubleshooting sequence outlined in {manuals[0]}. "
        f"Your immediate next step: '{actions[0]}'. Before physical intervention, ensure safety locks are engaged and "
        f"hydraulic/electrical power is tagged out. Cross-reference active BITE codes with the FIM and document all sensor readings. "
        f"If the fault persists, prepare for component removal and LRU bench testing. Prioritize safety and approved data."
    )

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/search")
def api_search():
    code = request.args.get("code", "").strip()
    keywords = [k.strip() for k in request.args.get("keywords", "").split(",") if k.strip()]
    result = skill.search_ata(code)
    if "error" not in result:
        result["advisory"] = generate_advisory(result, keywords)
    return jsonify(result)

@app.route("/api/codes")
def api_codes():
    return jsonify(skill.list_codes())

if __name__ == "__main__":
    app.run(debug=True, port=5000)