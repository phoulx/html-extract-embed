import json
from pathlib import Path

from flask import Flask, request

import service

app = Flask(__name__)

@app.route("/hello")
def hello():
    return 'Ciao!'

@app.route('/submit', methods=['POST'])
def receive() -> tuple[str, int]:
    file_path = request.get_json().get('filePath', '')
    result = service.handle(Path(file_path))

    return json.dumps(result), 200
