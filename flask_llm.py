from flask import Flask, request, jsonify
import json
from werkzeug.exceptions import BadRequest
from llm_process import process_prompt

app = Flask(__name__)



@app.route('/',methods = ["POST"])
def processclaim():
    try:
        if request.method == 'POST':
            data = request.get_json() 
            print(data)
            response = process_prompt(data)

            return jsonify(response), 200
    except BadRequest as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred.", "details": str(e)}), 500


if __name__ == "__main__":
    app.run()