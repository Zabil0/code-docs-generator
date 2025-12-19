from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


NOVITA_API_KEY = os.getenv('NOVITA_API_KEY', 'sk_Tr_2i8fVyuTJNZDqhSP4McFT8Rz19pTJQ_WWOth4dNE')
NOVITA_API_URL = "https://api.novita.ai/openai/chat/completions"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate-docs', methods=['POST'])
def generate_docs():
    try:
        data = request.json
        code = data.get('code', '')
        language = data.get('language', 'python')
        
        if not code.strip():
            return jsonify({'error': 'Please paste some code'}), 400
        
        
        prompt = f"""You are a professional code documentation generator. 
        
Generate comprehensive documentation for the following {language} code:

```{language}
{code}
```

Provide documentation in the following format:
1. **Function/Class Name**: [name]
2. **Purpose**: [brief description]
3. **Parameters**: [list with types and descriptions]
4. **Returns**: [return type and description]
5. **Example Usage**: [code example]
6. **Notes**: [any important notes or warnings]

Make it professional, clear, and concise."""

        
        headers = {
            "Authorization": f"Bearer {NOVITA_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "baidu/ernie-4.5-21B-a3b",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "max_tokens": 1000,
            "temperature": 0.7
        }
        
        response = requests.post(NOVITA_API_URL, headers=headers, json=payload)
        
        if response.status_code != 200:
            return jsonify({'error': f'API Error: {response.text}'}), 400
        
        result = response.json()
        documentation = result['choices'][0]['message']['content']
        
        return jsonify({
            'success': True,
            'documentation': documentation,
            'code': code,
            'language': language
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    return jsonify({'status': 'ok'})

    
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)