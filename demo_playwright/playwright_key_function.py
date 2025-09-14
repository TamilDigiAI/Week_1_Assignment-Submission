# math_api.py
from flask import Flask, request, jsonify

app = Flask(__name__)

def compute(op: str, a: float, b: float):
    op = (op or "").lower()
    if op == "add":
        return a + b
    if op == "subtract":
        return a - b
    if op == "multiply":
        return a * b
    if op == "divide":
        if b == 0:
            raise ValueError("Division by zero not allowed")
        return a / b
    raise ValueError(f"Unknown operation '{op}' (use add, subtract, multiply, divide)")

@app.get("/")
def home():
    return jsonify({
        "ok": True,
        "try": [
            "/calc?op=add&a=5&b=10",
            "/math?op=add&a=5&b=10",
            "/math/add?a=5&b=10",
            "/math/add/5/10"
        ],
        "post_json_example": {"op": "add", "a": 5, "b": 10}
    })

# Main endpoint (query params)
@app.get("/calc")
@app.get("/math")  # alias so /math works
def calc_query():
    op = request.args.get("op", "")
    a = request.args.get("a", None)
    b = request.args.get("b", None)
    if a is None or b is None or not op:
        return jsonify({"error": "Provide op, a, b (e.g., /calc?op=add&a=5&b=10)"}), 400
    try:
        a = float(a); b = float(b)
        result = compute(op, a, b)
        return jsonify({"operation": op, "a": a, "b": b, "result": result})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Path op + query numbers: /math/add?a=5&b=10
@app.get("/math/<op>")
def calc_path_query(op):
    a = request.args.get("a", None)
    b = request.args.get("b", None)
    if a is None or b is None:
        return jsonify({"error": "Provide a and b (e.g., /math/add?a=5&b=10)"}), 400
    try:
        a = float(a); b = float(b)
        result = compute(op, a, b)
        return jsonify({"operation": op, "a": a, "b": b, "result": result})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Pure path style: /math/add/5/10
@app.get("/math/<op>/<a>/<b>")
def calc_path_all(op, a, b):
    try:
        a = float(a); b = float(b)
        result = compute(op, a, b)
        return jsonify({"operation": op, "a": a, "b": b, "result": result})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# JSON body: POST /math  { "op": "add", "a": 5, "b": 10 }
@app.post("/math")
def calc_post_json():
    data = request.get_json(silent=True) or {}
    op = data.get("op"); a = data.get("a"); b = data.get("b")
    if op is None or a is None or b is None:
        return jsonify({"error": "JSON must include op, a, b"}), 400
    try:
        a = float(a); b = float(b)
        result = compute(op, a, b)
        return jsonify({"operation": op, "a": a, "b": b, "result": result})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Run: python math_api.py
    app.run(host="127.0.0.1", port=5000, debug=True)
