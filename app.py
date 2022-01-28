from flask import Flask, render_template, request, redirect, flash,session
from cs50 import SQL
from flask_session import Session

app = Flask(__name__) 
DB = SQL("sqlite:///database.db")
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = "filesystem"
Session(app)


@app.route("/")
def index():
    if not session.get("user_id",None):
        return redirect("/login")

    blogs = DB.execute("SELECT * from blogs join users on blogs.user_id = users.id")
    return render_template("blogs.html", blogs=blogs)

@app.route("/login", methods=['GET','POST'])
def login():

    if session.get("user_id",None):
        return redirect("/")

    if request.method == 'POST':
        email = request.form.get("email", None)
        password = request.form.get("pass", None)

        if not email or not password:
            flash("check your information", "danger")
            return redirect("/login")

        rows = DB.execute("SELECT * FROM users where email= ?",email)
        if len(rows) < 1:
            flash("user does not exist","danger")
            return redirect("/register")
        
        if not password == rows[0]['password']:
            flash("check you info","danger")
            return redirect("/login")


        session['user_id'] = rows[0]['id']
        flash("welcome","success")
        return redirect("/")
        



    return render_template("login.html")
    


@app.route("/register", methods=['GET','POST'])
def register():
    if session.get("user_id",None):
        return redirect("/")

    if request.method == 'POST':
        email = request.form.get("email", None)
        password = request.form.get("pass", None)
        name = request.form.get("name", None)

        if not email or not password or not name:
            flash("check your information", "danger")
            return redirect("/register")

        rows = DB.execute("SELECT * FROM users where email=?",email)
        if len(rows) > 0:
            flash("user already exists please login","danger")
            return redirect("/login")

        row = DB.execute("INSERT INTO users(name,email,password)VALUES(?,?,?)",name,email,password)
        session['user_id'] = row
        flash("welcome","success")
        return redirect("/")
        



    return render_template("register.html")

@app.route("/logout")
def logout():
    if not session.get("user_id",None):
        return redirect("/login")
    del session['user_id']
    return redirect("/login")


@app.route("/view")
def view():
    if not session.get("user_id",None):
        return redirect("/login")

@app.route("/update")
def update():
    if not session.get("user_id",None):
        return redirect("/login")

@app.route("/delete?id=1")
def delete():
    if not session.get("user_id",None):
        return redirect("/login")

    # id = request.args.get('id')
    # SELECT * FROM blogs where id=?",id
    # DELETE FROM blogs where id =
    


@app.route("/new", methods=['GET','POST'])
def new():
    if not session.get("user_id",None):
        return redirect("/login")

    if request.method == 'POST':
        title = request.form.get("title", None)
        description = request.form.get("description", None)

        if not title or not description:
            flash("check your information", "danger")
            return redirect("/new")

        DB.execute("INSERT INTO blogs(title,description,user_id)VALUES(?,?,?)",title,description,session['user_id'])
        flash("blog created.", "success")
        return redirect("/")
        
    
    return render_template("create_update_blog.html", title='Create new blog' , blog=None)


if __name__ == '__main__':
    app.run(debug=True)