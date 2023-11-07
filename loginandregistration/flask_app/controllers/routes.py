from flask_app import app
from flask import render_template,redirect,request,session
from flask_app.models.login import Login
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask import flash

@app.route("/")
def index():
    # users = User.get_all() # regresa los valores del metodo get all y almacena todos los datos de lbd
    # print(users)
    return render_template("index.html") 

@app.route("/success")
def success():
    if 'user_id' not in session:
        return redirect('/')
    return render_template("response.html")

@app.route("/newuser", methods=["POST"])
def newuser():
    
    pw_hash = bcrypt.generate_password_hash(request.form['password']) # crear Hash del password
    print(pw_hash)
    data = {
            "first_name": request.form["first_name"],
            "last_name": request.form["last_name"],
            "email": request.form["email"],
            "password": pw_hash
        }
    user_id = Login.save(data)
    session['user_id'] = user_id
    return redirect('/success')

@app.route("/login", methods=["POST"])
def login():
    if not Login.validate_login(request.form): # is la validacion es falso mandamos a index
        return redirect('/')
    # see if the username provided exists in the database
    data = { 
        "email" : request.form["email"] 
        }
    user_in_db = Login.get_by_email(data)
    # user is not registered in the db
    if not user_in_db: # Si es falso, que no hay un email in la Base de Datos
        flash("Invalid Email/Password")
        return redirect("/")
    # Si es verdadero, crear el HASH del password de la forma, y verificar so el HASH de la Base de Datos es el mismo
    # Recibe dos parametros, el primero es el HASH de la Base de Datos y el segundo el password de la forma del HTML, y los compara
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        # if we get False after checking the password
        flash("Invalid Email/Password")
        return redirect('/')
    # if the passwords matched, we set the user_id into session
    session['user_id'] = user_in_db.id
    # never render on a post!!!
    return redirect('/success')
 

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
 

# @app.route('/create_user', methods=["POST"])
# def create_user():
#     data = {
#         "uname": request.form["uname"],
#         "ulastname": request.form["ulastname"],
#         "uemail": request.form["uemail"]
#         # guarda los valores del formulario
#         }
   
#     id=User.save(data) # manda llamar al metodo para guardar
#     print(id)
   
#     return redirect(f"/show_user/{id}")# lo que me regreso de la base al html
#         # si es otra pagina 

# @app.route('/delete_user/<int:id>')
# def delete_user(id):
#     print(id)
#     data = {
#         "id": id
#         }
#     User.delete(data)
#     users = User.get_all()
#     return render_template("users.html",users=users)
   


# @app.route('/show_user/<int:id>')
# def show_user(id):
#     print(id)
#     data = {
#         "id": id,
    
#         }
#     user_id = User.get_user_by_id(data)
#     print(user_id)
#     return render_template("showuser.html",user= user_id) # lo que me regreso de la base al html
#         # si es otra pagina 

# @app.route('/update_user/<int:id>')
# def update_user(id):
#     print(id)
#     data = {
#         "id": id
#         }
#     user_id = User.get_user_by_id(data)
#     print(user_id)
#     return render_template("updateuser.html",user_id= user_id) # lo que me regreso de la base al html
#         # si es otra pagina 

# @app.route('/update_user/<int:id>', methods=["POST"])
# def update_user_post(id):
#     print(id)
#     data = {
#         "id": id,
#         "uname": request.form["uname"],
#         "ulastname": request.form["ulastname"],
#         "uemail": request.form["uemail"]
#         }
#     User.update(data)
#     print(f"/show_user/{id}")
#     return redirect(f"/show_user/{id}") # lo que me regreso de la base al html
#         # si es otra pagina 