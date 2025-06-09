from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, IntegerField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length, NumberRange
from models import User
from flask_login import current_user

class LoginForm(FlaskForm):
    """Formulir untuk login pengguna."""
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    """Formulir untuk registrasi pengguna baru."""
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('That email is taken. Please choose a different one.')

class ContactForm(FlaskForm):
    """Formulir untuk halaman kontak."""
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    subject = StringField('Subject', validators=[DataRequired()])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Send Message')

class CheckoutForm(FlaskForm):
    """Formulir untuk proses checkout."""
    fullname = StringField('Full Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[DataRequired()])
    address = TextAreaField('Shipping Address', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    country = StringField('Country', validators=[DataRequired()])
    zipcode = StringField('Zip Code', validators=[DataRequired()])
    payment_method = SelectField('Payment Method', choices=[
        ('credit_card', 'Credit Card'), 
        ('bank_transfer', 'Bank Transfer'), 
        ('e_wallet', 'E-Wallet')
    ], validators=[DataRequired()])
    submit = SubmitField('Place Order')

class ProductForm(FlaskForm):
    """Formulir untuk menambah/mengedit produk (Admin)."""
    name = StringField('Product Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    price = StringField('Price', validators=[DataRequired()])
    category = SelectField('Category', choices=[
        ('Baju', 'Baju'), 
        ('Sepatu', 'Sepatu'), 
        ('Aksesoris', 'Aksesoris')
    ], validators=[DataRequired()])
    stock = IntegerField('Stock', validators=[DataRequired(), NumberRange(min=0)])
    image_url = StringField('Image URL', validators=[DataRequired()])
    submit = SubmitField('Save Product')

class SearchForm(FlaskForm):
    """Formulir untuk pencarian produk."""
    search_query = StringField('Search', validators=[DataRequired()])
    submit = SubmitField('Search')

class ReviewForm(FlaskForm):
    """Formulir untuk ulasan produk."""
    rating = SelectField('Your Rating', 
                         choices=[('5', '5 - Excellent'), ('4', '4 - Very Good'), ('3', '3 - Good'), ('2', '2 - Fair'), ('1', '1 - Poor')], 
                         validators=[DataRequired()])
    comment = TextAreaField('Your Review', validators=[DataRequired(), Length(min=10, max=500)])
    submit = SubmitField('Submit Review')

# ===== FORM BARU UNTUK PROFIL PENGGUNA =====
class UpdateAccountForm(FlaskForm):
    """Formulir untuk memperbarui akun pengguna."""
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Update Account')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')

class ChangePasswordForm(FlaskForm):
    """Formulir untuk mengganti password."""
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm New Password', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Change Password')
