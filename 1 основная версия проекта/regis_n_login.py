# ВКЛЮЧАЕМ http://127.0.0.1:5000/login


# Этот код представляет собой веб-приложение на Flask для регистрации пользователей и их аутентификации.
# Импортируются необходимые модули и классы, такие как Flask, SQLAlchemy и форма регистрации (RegistrationForm)
# Создается экземпляр приложения Flask.
# Устанавливается секретный ключ для сессий.
# Определяется базовая модель SQLAlchemy (SqlAlchemyBase) и глобальная переменная для сессии SQLAlchemy (__factory)
# Имеется функция global_init(), которая инициализирует подключение к базе данных SQLite и создает таблицу для пользователей, если она не существует
# Функция create_session() создает и возвращает сессию SQLAlchemy.
# Определяется модель пользователя (User), которая представляет собой таблицу в базе данных и содержит методы для установки и проверки пароля
# Есть маршрут /register, который обрабатывает запросы для регистрации новых пользователей. Если запрос метода POST, данные из формы регистрации обрабатываются, новый пользователь добавляется в базу данных, а затем пользователь перенаправляется на страницу входа. Если запрос метода GET, отображается страница с формой регистрации.
# Есть маршрут /login, который обрабатывает запросы для входа пользователей. Если запрос метода POST, данные из формы входа обрабатываются, пользователь аутентифицируется и сессия пользователя устанавливается. Если запрос метода GET, отображается страница с формой входа.
# Есть маршрут /logout, который обрабатывает запросы для выхода пользователя из системы. При выходе из системы сеанс пользователя завершается, и пользователь перенаправляется на страницу входа.
# Если данный файл запускается напрямую (а не импортируется), выполняется инициализация базы данных и запуск приложения Flask в режиме отладки.


import os
import sqlalchemy.orm as orm
import sqlalchemy.ext.declarative as dec
import sqlalchemy as sa
from flask import Flask, request, redirect, url_for, session, render_template, flash
from werkzeug.security import generate_password_hash, check_password_hash
from forms import RegistrationForm
# Инициализация приложения Flask
app = Flask(__name__)
# Установка секретного ключа для сессий
app.secret_key = 'your_secret_key'

# Определение базовой модели SQLAlchemy
SqlAlchemyBase = dec.declarative_base()

# Глобальная переменная для сессии SQLAlchemy
__factory = None

# Инициализация подключения к базе данных
def global_init(db_file):
    global __factory
    if __factory is not None:
        return
    if not db_file or not db_file.strip():
        raise ValueError("Необходимо указать файл БД")
    conn_str = f"sqlite:///{db_file.strip()}?check_same_thread=False"
    engine = sa.create_engine(conn_str, echo=False)
    __factory = orm.sessionmaker(bind=engine)
    print(f"Подключение к БД: {conn_str} ...")
    SqlAlchemyBase.metadata.create_all(engine)

# Создание сессии SQLAlchemy
def create_session() -> orm.Session:
    global __factory
    return __factory()

# Модель пользователя
class User(SqlAlchemyBase):
    __tablename__ = 'users'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    surname = sa.Column(sa.String)
    name = sa.Column(sa.String)
    age = sa.Column(sa.Integer)
    address = sa.Column(sa.String)
    email = sa.Column(sa.String, unique=True)
    hashed_password = sa.Column(sa.String)

    # Установка пароля с хэшированием
    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    # Проверка пароля
    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def __repr__(self):
        return f"<User {self.id} {self.name} {self.email}>"

# Регистрация нового пользователя
@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegistrationForm()  # Создаем объект формы
    if request.method == 'POST':
        db_session = create_session()
        # Получение данных формы регистрации из запроса
        name = request.form['name']
        surname = request.form['surname']
        age = request.form['age']
        address = request.form['address']
        email = request.form['email']
        password = request.form['password']

        try:
            # Зарегистрировать нового пользователя
            existing_user = db_session.query(User).filter_by(email=email).first()
            if existing_user:
                return "Пользователь с таким email уже существует!", 400

            new_user = User(name=name, surname=surname, age=age, address=address, email=email)
            new_user.set_password(password)
            db_session.add(new_user)
            db_session.commit()
            db_session.close()
            return "Вы умнички и Алина тоже бумбастик.на этом все", 200
        except Exception as e:
            return str(e), 500
    else:
        return render_template('register.html', form=form)  # Передаем объект формы в шаблон

# @app.route('/success_registration')
# def success_registration():
#     return render_template('main.html')
    # # Получаем путь к корневой директории проекта
    # root_dir = os.path.dirname(os.path.abspath(__file__))
    # # Составляем полный путь к файлу main.html
    # main_html_path = os.path.join(root_dir, 'main.html')
    # # Отображаем main.html
    # return render_template(main_html_path)




# @app.route('/success_registration')
# def success_registration():
#     return render_template('main.html')


# Вход пользователя
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        db_session = create_session()
        # Получение данных формы входа из запроса
        email = request.form['email']
        password = request.form['password']

        # Поиск пользователя в базе данных по email
        user = db_session.query(User).filter_by(email=email).first()

        if user and user.check_password(password):
            # Успешная аутентификация: установка сеанса пользователя
            session['user_id'] = user.id
            db_session.close()
            return "Вы умнички и Алина тоже бумбастик.на этом все", 200
        else:
            db_session.close()
            return "Неправильный email или пароль. Попробуйте ещё раз.", 401
    else:
        return render_template('login.html')

# # Защищённая страница
# @app.route('/home')
# def home():
#     if 'user_id' in session:
#         return "Добро пожаловать на защищённую страницу!"
#     else:
#         return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Вы успешно вышли из системы', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    global_init("your_database.db")  # Инициализация базы данных
    app.run(debug=True)



