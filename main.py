from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase,relationship, DeclarativeBase, Mapped, mapped_column
from flask_bootstrap import Bootstrap5
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from forms import SingInForm, LogInForm
from sqlalchemy import Integer, String, Text
from werkzeug.security import generate_password_hash, check_password_hash

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)
app = Flask(__name__)



app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db.init_app(app)
Bootstrap5(app)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)



class User(UserMixin, db.Model):
    __tablename__ ="users"
    id:Mapped[int]= mapped_column(Integer,primary_key=True)
    email:Mapped[str] = mapped_column(String(100),unique=True)
    password :Mapped[str]=mapped_column(String(100))
    name: Mapped[str]=mapped_column(String(20))
    
with app.app_context():
    db.create_all()





@app.route('/')
def home():
    return render_template("index.html") 



@app.route('/login',methods = ["GET", "POST"])
def login():
    form = LogInForm()
    if form.validate_on_submit():
        email=form.email.data
        password = form.password.data
        result = db.session.execute(db.select(User).where(User.email == email))
        user = result.scalar()
        
        if user and check_password_hash(user.password,password):
            login_user(user)
            return redirect(url_for('contact'))
    return render_template("login.html",form = form)


@app.route('/singin',methods = ["GET", "POST"])
def singin():
    form = SingInForm()
    if form.validate_on_submit():
        ha_passord = generate_password_hash(
            form.password.data,
            method="pbkdf2:sha256",
            salt_length=8
        )
        new_uses=User(
            email = form.email.data,
            name= form.name.data,
            password = ha_passord
        )
        db.session.add(new_uses)
        db.session.commit()
        return redirect(url_for('contact'))
    return render_template("singin.html" ,form = form)

@app.route('/contact')
def contact():
    return render_template("contact.html")






















if __name__ == "__main__":
    app.run(debug=True, port=5003)