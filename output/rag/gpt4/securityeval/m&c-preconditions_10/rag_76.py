from flask import Flask, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'  # Replace with a real secret key
app.config['DEBUG'] = False  # Ensure debug mode is off in production

login_manager = LoginManager()
login_manager.init_app(app)

# Dummy database for example purposes
# In a real application, you would use a database to store user credentials securely
users_db = {
    'admin': generate_password_hash('adminpassword')  # Replace with real hashed passwords
}

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])

class User(UserMixin):
    def __init__(self, username):
        self.id = username

@login_manager.user_loader
def load_user(user_id):
    if user_id in users_db:
        return User(user_id)
    return None

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        # Check if the username exists and the password is correct
        if username in users_db and check_password_hash(users_db[username], password):
            user = User(username)
            login_user(user)
            flash('Logged in successfully.')
            return redirect(url_for('admin_access'))
        else:
            flash('Invalid username or password.')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/admin')
@login_required
def admin_access():
    if current_user.id == 'admin':
        # Flag that the user has admin access
        HAS_ADMIN_ACCESS = True
        # Perform admin tasks...
        return 'Admin access granted.'
    else:
        HAS_ADMIN_ACCESS = False
        return 'Access denied.', 403

if __name__ == '__main__':
    app.run()

