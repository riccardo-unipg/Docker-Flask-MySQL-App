from flask import Flask, jsonify, render_template, request, json
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

app=Flask(__name__)

# MySQL configurations 
app.config['MYSQL_USER'] = 'ric'
app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'bucketlist'
app.config['MYSQL_HOST'] = 'db'
app.config['MySQL_PORT'] = 3306

mysql = MySQL(app)

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

@app.route('/showSignUp/showDatabase')
def showDatabase():
    return render_template('table.html')

@app.route('/signUp', methods=['POST'])
def signUp():
    #try:
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']

        if _name and _email and _password:
            #conn = db.connection
            curs = mysql.connection.cursor()

            # Hide password
            _hashed_password = generate_password_hash(_password)

            curs.callproc('sp_createUser',(_name,_email,_hashed_password))
            data = curs.fetchall()

            if len(data) == 0:
                #conn.commit()
                mysql.connection.commit()
                curs.close()
                return json.dumps({'message':'User created successfully !'})
            else:
                return json.dumps({'error':str(data[0])})
            
        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})
        
@app.route('/tbl_user', methods=['GET'])
def get_table_rows():
    # Connessione al database
    cur = mysql.connection.cursor()

    # Query per selezionare tutte le righe dalla tabella specificata
    query = "SELECT * FROM tbl_user"
    cur.execute(query)

    # Estrazione dei risultati della query
    rows = cur.fetchall()

    # Chiusura della connessione al database
    cur.close()

    # Restituzione dei risultati come JSON
    results = []
    for row in rows:
        result = {}
        for i, column_name in enumerate(cur.description):
            result[column_name[0]] = row[i]
        results.append(result)
        #print(jsonify(results))
    return jsonify(results)

if __name__=='__main__':
    app.run(host='0.0.0.0')






