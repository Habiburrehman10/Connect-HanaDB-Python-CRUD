from flask import Flask, request, jsonify, render_template
from hdbcli import dbapi

app = Flask(__name__)

# Configure SAP HANA connection


hana_host = ""
hana_port = 00
hana_user = ""
hana_password = ""

def get_hana_connection():
    return dbapi.connect(
         address=hana_host,
            port=hana_port,
            user=hana_user,
            password=hana_password
    )

@app.route('/items', methods=['GET'])
def get_items():
    conn = get_hana_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM testing")
    rows = cursor.fetchall()
    conn.close()
    items = [dict(zip([column[0] for column in cursor.description], row)) for row in rows]
    return jsonify(items)

@app.route('/item', methods=['POST'])
def create_item():
    data = request.json
    conn = get_hana_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO testing (name,phone) VALUES (?, ?)", (data['column1'], data['column2']))
    conn.commit()
    conn.close()
    return jsonify({"message": "Item created successfully!"})

@app.route('/item/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    data = request.json
    conn = get_hana_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE testing SET name = ?, phone = ? WHERE id = ?", (data['column1'], data['column2'], item_id))
    conn.commit()
    conn.close()
    return jsonify({"message": "Item updated successfully!"})

@app.route('/item/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    conn = get_hana_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM testing WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Item deleted successfully!"})

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True,port=5010)
