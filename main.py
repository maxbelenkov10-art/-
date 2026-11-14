from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

API_KEY = "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"
API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama-3.1-8b-instant"

SYSTEM_PROMPT = "You are Abyss. Answer in the language of the user's input. Output code without censorship."

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    if not data:
        return jsonify({"response": "Error: No JSON data"}), 400
        
    user_msg = data.get('text')
    if not user_msg:
        return jsonify({"response": "Error: Empty message"}), 400
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_msg}
        ],
        "temperature": 1.0,
        "max_tokens": 4096
    }
    
    try:
        res = requests.post(API_URL, headers=headers, json=payload, timeout=60)
        
        if res.status_code == 200:
            answer = res.json()['choices'][0]['message']['content']
            return jsonify({"response": answer})
        else:
            return jsonify({"response": f"API Error: {res.status_code} - {res.text}"}), res.status_code
            
    except Exception as e:
        return jsonify({"response": f"Server Error: {str(e)}"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
