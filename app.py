from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import uuid

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://maja:maja@localhost:5432/baza'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'gigatajny_kluuucz'

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


# Models
class User(UserMixin, db.Model):
    __tablename__ = 'uzytkownik'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)


class Ad(db.Model):
    __tablename__ = 'ogloszenia'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tresc = db.Column(db.Text, nullable=False)
    tytul = db.Column(db.Text, nullable=False)
    uzytkownik_id = db.Column(db.String(36), db.ForeignKey('uzytkownik.id'), nullable=False)
    zwierzeta_id = db.Column(db.String(36), db.ForeignKey('zwierzeta.id'), nullable=False)


class Animal(db.Model):
    __tablename__ = 'zwierzeta'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    imie = db.Column(db.Text, nullable=False)
    typ = db.Column(db.Text, nullable=False)
    uzytkownik_id = db.Column(db.String(36), db.ForeignKey('uzytkownik.id'), nullable=False)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/')
def index():
    search_query = request.args.get('q', '').strip()
    if search_query:
        ads = Ad.query.join(Animal, Ad.zwierzeta_id == Animal.id).filter(
            (Ad.tytul.ilike(f"%{search_query}%")) |
            (Animal.typ.ilike(f"%{search_query}%"))
        ).all()
    else:
        ads = Ad.query.all()
    return render_template('index.html', ads=ads, current_user=current_user, search_query=search_query)


@app.route('/ad/<uuid:ad_id>')
def ad_details(ad_id):
    ad = Ad.query.get(str(ad_id))
    if not ad:
        return "Ogłoszenie nie znalezione", 404
    return render_template('ad_details.html', ad=ad)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Hasła nie są zgodne!', 'danger')
            return render_template('register.html')

        if User.query.filter_by(email=email).first():
            flash('Użytkownik z tym adresem email już istnieje!', 'danger')
        else:
            new_user = User(email=email, password=password)  # Użyj odpowiedniego hashowania hasła w produkcji
            db.session.add(new_user)
            db.session.commit()
            flash('Konto zostało pomyślnie utworzone!', 'success')
            return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            login_user(user)
            flash("Zalogowano pomyślnie!", "success")
            return redirect(url_for('index'))
        else:
            flash("Błędne dane logowania", "danger")
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Wylogowano pomyślnie!', 'success')
    return redirect(url_for('index'))


@app.route('/add_ad', methods=['GET', 'POST'])
@login_required
def add_ad():
    user_animals = Animal.query.filter_by(uzytkownik_id=current_user.id).all()
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        animal_id = request.form['animal_id']
        new_ad = Ad(tytul=title, tresc=description, uzytkownik_id=current_user.id, zwierzeta_id=animal_id)
        db.session.add(new_ad)
        db.session.commit()
        flash('Ogłoszenie dodane pomyślnie!', 'success')
        return redirect(url_for('index'))
    return render_template('add_ad.html', user_animals=user_animals)


@app.route('/add_animal', methods=['GET', 'POST'])
@login_required
def add_animal():
    if request.method == 'POST':
        name = request.form['name']
        animal_type = request.form['type']
        new_animal = Animal(imie=name, typ=animal_type.upper(), uzytkownik_id=current_user.id)
        db.session.add(new_animal)
        db.session.commit()
        flash('Zwierzę dodane pomyślnie!', 'success')
        return redirect(url_for('index'))
    return render_template('add_animal.html')


if __name__ == '__main__':
    app.run()
