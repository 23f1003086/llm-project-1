from flask import Flask, request, jsonify
import base64
import os

app = Flask(__name__)

# ==== GitHub details   ====
GITHUB_USERNAME = "23f1003086"         
GITHUB_TOKEN = "REPLACE_WITH_ENV_VARIABLE"
 
GITHUB_REPO = "llm-project-1"           
# ===============================================

@app.route('/api-endpoint', methods=['POST'])
def receive_task():
    data = request.json
    print("Received task:", data)

   
    for attach in data.get('attachments', []):
        name = attach['name']
        content = base64.b64decode(attach['url'].split(',')[1])
        with open(name, 'wb') as f:
            f.write(content)

  
    html_content = f"<html><body><h1>Task Brief</h1><p>{data.get('brief', '')}</p></body></html>"
    with open("index.html", "w") as f:
        f.write(html_content)

    # ==== Push to GitHub ====
    os.system("git init")
    os.system("git add .")
    os.system("git commit -m 'Update task page'")
    os.system(f"git remote add origin https://{GITHUB_USERNAME}:{GITHUB_TOKEN}@github.com/{GITHUB_USERNAME}/{GITHUB_REPO}.git")
    os.system("git branch -M main")
    os.system("git push -u origin main")
    # ========================

    # Return a unique usercode
    return jsonify({"usercode": "student123"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
