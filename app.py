import os
from pyclbr import Class

from cs50 import SQL
import sqlite3 as sql
from flask import Flask, flash, jsonify, redirect, render_template, request, session,url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Length
# Configure application
app = Flask(__name__)
app.secret_key="super key"
# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")

@app.route("/")
@app.route("/index")
def index():
    # con=sql.connect("db_web.db")
    # con.row_factory=sql.Row
    # cur=con.cursor()
    # db = SQL("sqlite:///birthdays.db")

    # db.execute("select * from complaint_details")
    con=sql.connect("birthdays.db")
    con.row_factory=sql.Row
    cur=con.cursor()
    cur.execute("select * from complaint_details")
    data=cur.fetchall()
    # data=cur.fetchall()
    return render_template("index.html",complaint_details=data)

@app.route("/add", methods=["GET", "POST"])

def add():
    if request.method == "POST":
        # db = SQL("sqlite:///birthdays.db")
        complaint_id=request.form.get("complaint_id")
        registered_name=request.form.get("registered_name")
        block_no=request.form.get("block_no")
        floor_no=request.form.get("floor_no")
        door_no=request.form.get("door_no")
        type_of_issue=request.form.get("type_of_issue")
        complaint_description=request.form.get("complaint_description")
        con=sql.connect("birthdays.db")
        cur=con.cursor()
        cur.execute("Insert into complaint_details (complaint_id,registered_name,block_no,floor_no,door_no,type_of_issue,complaint_description) values(?,?,?,?,?,?,?)",(complaint_id,registered_name,block_no,floor_no,door_no,type_of_issue,complaint_description))
        con.commit()
        flash('User Added','success')

        return redirect(url_for("index"), code=302)
    return render_template("add.html")
@app.route("/edit/<string:complaint_id>",methods=['POST','GET'])
def edit(complaint_id):
    if request.method == "POST" :   
         registered_name= request.form.get("registered_name")
         block_no=request.form.get("block_no")
         floor_no=request.form.get("floor_no")
         door_no=request.form.get("door_no")
         type_of_issue=request.form.get("type_of_issue")        
         complaint_description=request.form.get("complaint_description")
         con=sql.connect("birthdays.db")
         cur=con.cursor()

         cur.execute("update complaint_details SET registered_name = ?,block_no=?,floor_no=?,door_no=?,type_of_issue=?,complaint_description=? where complaint_id = ?",
         (registered_name,block_no,floor_no,door_no,type_of_issue,complaint_description,complaint_id))
         con.commit()
         flash('User Updated','success') 
         return redirect(url_for("index"),code=301)
    con=sql.connect("birthdays.db")
    con.row_factory=sql.Row
    cur=con.cursor() 

    cur.execute("select * from complaint_details where complaint_id=?",(complaint_id,))
    complaint_details=cur.fetchone()
    return render_template("edit.html",complaint_details=complaint_details)
             
             
@app.route("/delete/<string:complaint_id>",methods=['GET'])
def delete(complaint_id):  
    if complaint_id:
        con=sql.connect("birthdays.db")
        cur=con.cursor()
        cur.execute("DELETE FROM complaint_details WHERE complaint_id = ?",(complaint_id,))
        con.commit()
        return redirect(url_for("index"))
# class SearchForm(FlaskForm):
# 	searched = StringField("Searched", validators=[DataRequired()])
# 	submit = SubmitField("Submit")
# def base():
#     form=SearchForm()
#     return dict(form=form)
@app.route('/search.html', methods=['GET'])
def search():
     
    keywords = request.args.get('keywords')

    # Connect to the SQLite database
    conn = sql.connect('birthdays.db')
    c = conn.cursor()

    # Execute the search query
    c.execute("SELECT * FROM complaint_details WHERE "
              "complaint_id LIKE ? OR "
              "registered_name LIKE ? OR "
              "block_no LIKE ? OR "
              "floor_no LIKE ? OR "
              "door_no LIKE ? OR "
              "type_of_issue LIKE ? OR "
              "complaint_description LIKE ?",
              ('%'+keywords+'%', '%'+keywords+'%', '%'+keywords+'%', '%'+keywords+'%', '%'+keywords+'%',
               '%'+keywords+'%', '%'+keywords+'%'))
    results = c.fetchall()

    # Close the database connection
    conn.close()
    return render_template('search.html', results=results)
        # all in the search box will return all the tuples
        # if len(data) == 0 and registered_name == 'all': 
        #     cur.execute("SELECT complaint_id,registered_name from complaint_details")
        #     con.commit()
        #     data = cur.fetchall()
        # return render_template('search.html', complaint_details=data)
# class complaints(db.model):
#     complaint_id=db['complaint_id']
#     registered_name=db['registered_name']
#     block_no=db['block_no']
#     floor_no=db['floor_no']
#     door_no=db["door_no"]
#     type_of_issue=db['type_of_issue']
#     complaint_description=db['complaint_description']


if __name__=='__main__':
    app.run(debug=True)
