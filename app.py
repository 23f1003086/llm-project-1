from flask import Flask, request, jsonify
import base64
import os
import csv
app = Flask(__name__)

# ==== GitHub details   ====
GITHUB_USERNAME = "23f1003086"         

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")   

 
GITHUB_REPO = "llm-project-1"           
# ===============================================

@app.route('/api-endpoint', methods=['POST'])
def receive_task():
    data = request.json
    print("Received task:", data)

    # Save attachments
    attachment_html = ""
    for attach in data.get('attachments', []):
        name = attach['name']
        content = base64.b64decode(attach['url'].split(',')[1])
        with open(name, 'wb') as f:
            f.write(content)
        
        # If CSV, calculate sum of first column
        if name.endswith('.csv'):
            import csv
            total = 0
            with open(name, 'r') as f_csv:
                reader = csv.reader(f_csv)
                for row in reader:
                    if row and row[0].isdigit():
                        total += int(row[0])
            attachment_html += f"<p>Sum of first column in {name}: {total}</p>"

        # If image, display it
        if name.endswith(('.png', '.jpg', '.jpeg', '.gif')):
            attachment_html += f'<p>{name}:</p><img src="{name}" width="300"/>'

    # Create HTML page
    html_content = f"""
    <html>
      <body>
        <h1>Task Brief</h1>
        <p>{data.get('brief', '')}</p>
        {attachment_html}
      </body>
    </html>
    """
    with open("index.html", "w") as f:
        f.write(html_content)

    return jsonify({"usercode": "student123"}), 200


@app.route('/update', methods=['POST'])
def update_csv():
    if 'file' not in request.files:
        return "No file uploaded", 400

    file = request.files['file']
    filename = file.filename
    file.save(filename)  # save CSV in project folder

    # Calculate sum of first column
    total = 0
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row and row[0].isdigit():
                total += int(row[0])

    # Update HTML
    html_content = f"""
    <html>
      <body>
        <h1>CSV Sum Result</h1>
        <p>Sum of first column in {filename}: {total}</p>
      </body>
    </html>
    """
    with open("index.html", "w") as f:
        f.write(html_content)

    return jsonify({"sum": total}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
