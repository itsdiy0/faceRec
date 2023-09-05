from flask import Flask,render_template, request, url_for, flash, redirect,session
import os
from werkzeug.utils import secure_filename
from OCV.face_rec import recongnize
from functions import *

app = Flask(__name__)
app.config['SECRET_KEY'] = '95275a2e062866afcd099992eb0b09626e29a0e01041fe41'
app.config['UPLOAD_FOLDER'] = app.static_folder+'/uploads'
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']
app.config['MAX_CONTENT_PATH'] = 1024 * 1024


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/search',methods=["GET"])
def search():
    if request.method == "GET":
        search_word = request.args['search']
        print(type(search_word))
        conn = get_db_connection()
        sql = "SELECT * FROM users WHERE fullname LIKE '%{}%'".format(search_word) 
        users = conn.execute(sql).fetchall()
        conn.close()
    return render_template('view_users.html',users=users,search_word=search_word)

@app.route('/view_users')
def view_users():
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM users').fetchall()
    conn.close()
    return render_template('view_users.html',users=users)

@app.route('/add_users',methods=('POST','GET'))
def add_users():
    if request.method=='POST':
        full_name = request.form['full_name']
        folder_name = folder_name_generator(full_name)
        directory_genartor(folder_name)
        birth_date = request.form['birth_date']
        file = request.files['file_name']
        filename = file_name_generator(folder_name,1)
        file.filename = filename
        upload_address = os.path.join(app.config['UPLOAD_FOLDER']+f"/train/{folder_name}/",filename)
        file.save(upload_address)
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (fullname, photoAddress, birthdate) VALUES (?, ?, ?)",(folder_name,f"train/{folder_name}/{filename}",birth_date))
        conn.commit()
        cursor.close()
        flash("User succussfully added !")
    return render_template('add_users.html')

@app.route('/delete_user',methods=('POST','GET'))
def delete_user():
    id = str(request.args.get('id'))
    conn = get_db_connection()
    cursor = conn.cursor()
    file_address = cursor.execute(f'SELECT photoAddress FROM users WHERE id={id}').fetchone()
    os.remove('static/uploads/'+str(file_address[0]))
    cursor.execute(f'DELETE FROM users WHERE id={id}')
    conn.commit()
    cursor.close()
    remove_empty_trains()
    flash("user removed from system !")
    return redirect(url_for('view_users'))

@app.route('/recognition',methods=('POST','GET'))
def recognition():
    if request.method=='POST':
        file = request.files['file_name']
        file.filename = "uploaded.jpg"
        filename = secure_filename(file.filename)
        upload_address = os.path.join(app.config['UPLOAD_FOLDER']+"/check_upload/",filename)
        file.save(upload_address)
        data = {
            "uploaded_address" : str(upload_address)
        }
        return render_template("recegniton.html",data=data)
    else:
        return render_template("recegniton.html")

@app.route('/analyze')
def analyze():
    op = {}
    confidence,name = recongnize()
    file_name = file_name_generator(name,0)
    op["name"] = name 
    if confidence==0.0:
        confidence=100
    else:
        confidence = round(confidence,5)
    confidence = str(confidence)+"%"
    op["confidence"] = confidence 
    op["img_name"] = name+"/"+file_name
    conn = get_db_connection()
    cursor = conn.cursor()
    op["BOD"] = cursor.execute("SELECT birthdate FROM users WHERE fullname='{}'".format(name)).fetchone()[0]
    conn.commit()
    cursor.close()
    return render_template("recegniton.html",op=op)

if __name__ == '__main__':
   app.run(debug = False)