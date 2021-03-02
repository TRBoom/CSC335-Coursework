from flask import render_template, flash, redirect, url_for, request, Flask
from flask_login import LoginManager, UserMixin, login_user, logout_user, \
    current_user, login_required
from werkzeug.urls import url_parse
from werkzeug.security import check_password_hash, generate_password_hash
from wtforms import Form, TextField, PasswordField, validators, SubmitField,\
     SelectField, IntegerField, FieldList,FormField
from wtforms.validators import ValidationError, DataRequired, EqualTo, Length, \
     Regexp, AnyOf, NoneOf, Email, InputRequired, Optional

from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
import sys


from courses import *
from wish_list import *
from user_pass_role import *
from notifications import *
from course_list import *

'''
Class for checking if a form
field is required.
'''

class RequiredIf(DataRequired):
    #Currently used in ClassLookupForm
    field_flags = ('requiredif',)
    def __init__(self, message=None, *args, **kwargs):
        super(RequiredIf).__init__()
        self.message = message
        self.conditions = kwargs

    def __call__(self, form, field):
        for name, data in self.conditions.items():
            other_field = form[name]
            if other_field is None:
                raise Exception('no field named "%s" in form' % name)
            if other_field.data == data and not field.data:
                DataRequired.__call__(self, form, field)
            Optional()(form, field)

'''
Most of our forms for login/signup, adding/deleting wishes/courses
and user accoutn management.

The rest are located in their own functions.
'''
class LoginForm(FlaskForm):
    user = TextField('Username', validators=[DataRequired()])
    passw = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')


class AddForm(FlaskForm):
    submit = SubmitField('Add to Wishlist')


class CreateUserForm(FlaskForm):
    name = TextField('Full Name', validators=[DataRequired()])
    user = TextField('Email', validators=[DataRequired(),Email()])
    passw = PasswordField('Password', validators=[DataRequired(),
                         EqualTo('pass2',  message='Passwords must match')])
    pass2 = PasswordField('Password2', validators=[DataRequired()])
    role = SelectField('User Role', choices =[('s','Student'), ('f','Faculty'),
                        ('a','Admin')])
    submit = SubmitField('Create User')
    

class ForgotPassForm(FlaskForm):
    email = TextField('Email', validators=[DataRequired(),Email(),EqualTo('email2', message='Emails must match')])
    email2 = TextField('Email Again', validators=[DataRequired(),Email()])
    submit = SubmitField('Send Reset Email')
    

class ChangePassForm(FlaskForm):
    newpassw = PasswordField('Password', validators=[DataRequired(),
                         EqualTo('newpass2',  message='Passwords must match')])
    newpass2 = PasswordField('Password Again', validators=[DataRequired()])    
    submit = SubmitField('Change Password')


class ChangeEmailForm(FlaskForm):
    newemail = TextField('New Email', validators=[DataRequired(),Email(),EqualTo('newemail2', message='Emails must match')])
    newemail2 = TextField('New Email Again', validators=[DataRequired(),Email()])
    submit = SubmitField('Send Reset Email')   


class ChangeClassForm(FlaskForm):
    year = SelectField('New Class', choices =[('Freshman','Freshman'), 
                        ('Sophomore','Sophomore'),
                        ('Junior','Junior'),('Senior','Senior')])

    submit = SubmitField('Submit') 


class User(UserMixin):
    def __init__(self, username, password, role):
        self.id = username
        self.pass_hash = generate_password_hash(password)
        print(self.pass_hash, file=sys.stderr)
        self.role = role


app = Flask(__name__)
app.config['SECRET_KEY'] = 'a hard to guess string'
bootstrap = Bootstrap(app)
moment = Moment(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

'''
Determind user role
'''

def is_admin():
    if current_user:
        if current_user.role == 'a':
            return True
        else:
            return False
    else:
        print('User not authenticated.', file=sys.stderr)

        
def is_faculty():
    if current_user:
        if current_user.role == 'f':
            return True
        else:
            return False
    else:
        print('User not authenticated.', file=sys.stderr)

def is_student():
    if current_user:
        if current_user.role == 's':
            return True
        else:
            return False
    else:
        print('User not authenticated.', file=sys.stderr)


@login_manager.user_loader
def load_user(id):
    return User(id, user_pass(id), user_role(id))


@app.route('/')
@app.route('/index')
def index():
    if current_user.is_authenticated:
        return render_template('index.html', name=current_user.id)
    else:
        return render_template('index.html', name="Stranger")


@app.route('/admin_only')
@login_required
def admin_only():
    if is_admin():
        return render_template('admin.html', message="I am admin.")
    else:
        return render_template('unauthorized.html')

'''
Sign up, include sign up form.
Student enters name, ID, year, email and password.
Sends an email after successful sign up.
'''
@app.route('/signup', methods=['GET', 'POST'])
def sign_up():
    
    class SignUpForm(FlaskForm):
        name = TextField('Full Name', validators=[DataRequired()])
        studentID = TextField('Student ID', 
                    validators=[DataRequired(),NoneOf(id_list(),
                    message='That ID is in use already.'),Length(8, 
                    message='Field must be 8 characters long.'), Regexp('^[0-9]*$', 
                    message='Input must be numerical.')])
        year = SelectField('Class', choices =[('Freshman','Freshman'), 
                        ('Sophomore','Sophomore'),
                        ('Junior','Junior'),('Senior','Senior')])
        user = TextField('Email', validators=[DataRequired(),Email()])
        passw = PasswordField('Password', validators=[DataRequired(),
                                EqualTo('pass2', message='Passwords must match')])
        pass2 = PasswordField('Enter Password Again')
        
        submit = SubmitField('Sign Up')
        
    form = SignUpForm()
    if form.validate_on_submit():
        newUser = User(form.user.data, form.passw.data, 's')
        if does_user_exist(form.user.data):
            return render_template('message.html', message="User already exists.")
        else:
            user_add(form.name.data, form.user.data, form.studentID.data, 
                    form.year.data, form.passw.data, 's')
            login_user(newUser)
            account_email(form.user.data,'created')
            return render_template('message.html', message="Account Created!")
    return render_template('signup.html', title='Sign up', form=form)

'''
Create user for admins.
'''

@app.route('/create_user', methods=['GET', 'POST'])
@login_required
def create_user():
    form = CreateUserForm()    
    if is_admin():
        if form.validate_on_submit():
            newUser = User(form.user.data, form.passw.data, form.role.data)
            if does_user_exist(form.user.data):
                return render_template('admin.html', message="User already exists.")
            else:
                user_add(form.name.data, form.user.data, 'faculty', 'faculty', 
                        form.passw.data, form.role.data)
                account_email(form.user.data,'created')
                return render_template('admin.html', message="User Created!") 
        return render_template('signup.html', form=form)
    else:
        return render_template('unauthorized.html')

'''
Login to page via email and password.
If invalid, show an error message.
'''
        
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))   
    form = LoginForm()
    if form.validate_on_submit():
        if not does_user_exist(form.user.data):
            return render_template('message.html', message="User not found.")        
        user = User(form.user.data, user_pass(form.user.data), 
                    user_role(form.user.data))
        valid_password = check_password_hash(user.pass_hash, form.passw.data)
        if user is None or not valid_password:
            print('Invalid username or password', file=sys.stderr)
            redirect(url_for('index'))
        else:
            login_user(user)
            if current_user.role == 's':
                return redirect(url_for('wishlist'))
            else:
                return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/success')
def success():
    return render_template('success.html')


@app.route('/sitemap')
def sitemap():
    return render_template('sitemap.html')

'''
User management functions. Allows user to 
change password, email, class year and 
delete account.

Sends an email verification for all, excluding 
class year.
'''

@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePassForm()
    if form.validate_on_submit():
        user_pass_change(current_user.id, form.newpassw.data)
        account_email(current_user.id, '3')
    return render_template('change_password.html', title='Change Password', form=form)


@app.route('/forgot_password', methods=['GET', 'POST'])
#Generates a random string and changes the user's password to that string
def forgot_password():
    form = ForgotPassForm()
    if form.validate_on_submit():
        randoStr = randomString(8)
        user_pass_change(form.email.data, randoStr)
        password_reset(form.email.data, randoStr)
    return render_template('forgot_password.html', title='Reset Password', form=form)


@app.route('/change_email', methods=['GET', 'POST'])
@login_required
def change_email():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        user_email_change(current_user.id, form.newemail.data)
        account_email(current_user.id, '2')
    return render_template('change_email.html', title='Change Email', form=form)


@app.route('/change_class',methods=['GET', 'POST'])
@login_required
def change_class():
    form=ChangeClassForm()
    if form.validate_on_submit():
        user_class_change(current_user.id, form.year.data)
    return render_template('change_class.html', title='Change class', form=form)   


@app.route('/delete_account',methods=['GET', 'POST'])
@login_required
def del_account():
    class AccountDeletionForm(FlaskForm):
        password = PasswordField('Verify password', validators=[DataRequired()])
        submit = SubmitField('Submit')     
    form=AccountDeletionForm()
    if form.validate_on_submit():
        valid_password = check_password_hash(current_user.pass_hash, form.password.data)
        if not valid_password:
            print('Invalid username or password', file=sys.stderr)
            return redirect(url_for('index'))
        else:
            user_delete(current_user.id)
            logout()
            return redirect(url_for('index'))
    return render_template('delete_account.html',form=form)

'''
Wishlist page. Can add and remove wishes directly
from the page.
'''

@app.route('/wishlist', methods=['GET', 'POST'])
@login_required
def wishlist():
    class WishRemove(FlaskForm):
        CRN = IntegerField('Course Number', validators=[DataRequired(),
                    AnyOf(wishlist_get(current_user.id),
                    message='This course is not on your wishlist.')])
        submit = SubmitField('Remove Wish')

    class WishAdd(FlaskForm):
        CRN = IntegerField('Course Number', validators=[DataRequired(),
                    AnyOf(course_valid(),
                        message='That course number could not be found.'),
                    NoneOf(course_invalid(),
                        message="""This course is not full!  
                        It is available for sign up on Banner."""),
                    NoneOf(wishlist_get(current_user.id),
                           message='This course is already on your wishlist.')])  
        submit = SubmitField('Add Wish')
        
    addForm = WishAdd()     
    remForm = WishRemove()
    wlist=[]         
    if is_student():
        if remForm.validate_on_submit():
            wish_remove(current_user.id,remForm.CRN.data)
            render_template('wishlist.html', wlist=wlist, remForm=remForm, addForm=addForm)
            return redirect(url_for('wishlist'))
        elif addForm.validate_on_submit():
            wish_add(current_user.id,addForm.CRN.data)
            render_template('wishlist.html',wlist=wlist, remForm=remForm, addForm=addForm)
            return redirect(url_for('wishlist'))
        for wish in wishlist_get(current_user.id):
            wlist.append(course_get(wish)[0])
        return render_template('wishlist.html', wlist=wlist, remForm=remForm, addForm=addForm)
    else:
        return render_template('unauthorized.html')

'''
Courselist page. Can add or remove current courses
directly from the page
'''

@app.route('/courselist', methods=['GET', 'POST'])
@login_required
def courselist():
    
    class CourseRemove(FlaskForm):
        CRN = IntegerField('Course Number', validators=[DataRequired(),
                    AnyOf(courselist_get(current_user.id),
                    message='This course is not on your wishlist.')])
        submit = SubmitField('Remove Course')

    class CourseAdd(FlaskForm):
        CRN = IntegerField('Course Number', validators=[DataRequired(),     
                    AnyOf(course_valid(),
                        message='That course number could not be found.'),
                    NoneOf(courselist_get(current_user.id),
                        message='This course is already on your list.')])
        submit = SubmitField('Add Course')
   
    addForm = CourseAdd()
    remForm = CourseRemove()
    clist=[]
    if is_student():
        if remForm.validate_on_submit():
            course_remove(current_user.id,remForm.CRN.data)
            render_template('courselist.html',clist=clist,remForm=remForm,addForm=addForm)
            return redirect(url_for('courselist'))
        elif addForm.validate_on_submit():
            course_add(current_user.id,addForm.CRN.data)
            render_template('courselist.html', clist=clist, remForm=remForm, addForm=addForm) 
            return redirect(url_for('courselist'))
        for course in courselist_get(current_user.id):
            clist.append(course_get(course)[0])
        return render_template('courselist.html', clist=clist, remForm=remForm, addForm=addForm)
    else:
        return render_template('unauthorized.html')

'''
Course add was a little buggy, so we kept this page
just in case.
'''

@app.route('/courseadd', methods=['GET', 'POST'])
@login_required
def courseadd():
    
    class CRNForm(FlaskForm):
        CRN = IntegerField('Course Number', validators=[DataRequired(),
                    AnyOf(course_valid(),
                        message='That course number could not be found.'),
                    NoneOf(courselist_get(current_user.id),
                        message='This course is already on your list.')])
        
        submit = SubmitField('Submit')
        
    form = CRNForm()     
    if form.validate_on_submit():
        course_add(current_user.id,form.CRN.data)
        return redirect(url_for('courselist'))
    return render_template('courseadd.html', form=form)

'''
Class search. User can search for courses via
CRN, subject, or course name. Can add directly
to their wishlist.
'''

@app.route('/lookup', methods=['GET', 'POST'])
@login_required
def course_lookup():
    
    class CourseLookupForm(FlaskForm):
        search_method = SelectField('Choose search criteria', 
                        choices =[('CRN','Course Registration Number'), 
                        ('SUB','Subject'),('CRSE','Course title (ex/ART150)')], 
                        validators=[DataRequired()])

        CRN = IntegerField('Course Number', 
                    validators=[RequiredIf(search_method='CRN'),
                    AnyOf(course_valid(),message='This course could not be found')])

        SUB = TextField('Subject name', 
                    validators=[RequiredIf(search_method='SUB'),Length(3, 
                    message='Field must be 3 characters long. (ex/ART)')])

        CRSE = TextField('Course name', 
                    validators=[RequiredIf(search_method='CRSE'),Length(6, 
                    message='Field must be 6 characters long. (ex/ART150)')])
    
        submit = SubmitField('Search')
        
    class CRNForm(FlaskForm):
        course = IntegerField('Enter Course CRN', validators=[
                    AnyOf(course_valid(),
                        message='That course number could not be found.'),
                    NoneOf(course_invalid(),
                           message="""This course is not full! 
                           It is available for sign up on Banner."""),
                    NoneOf(wishlist_get(current_user.id),
                           message='This course is already on your wishlist.')])
        addcourse = SubmitField('Add to wishlist')
       
    
    clist=[]
    form = CourseLookupForm()
    formAdd=CRNForm()
    if form.validate_on_submit():
        if (form.search_method.data=="CRN"):
            clist=course_get(form.CRN.data)
        elif (form.search_method.data=="SUB"):
            clist=subject_get(form.SUB.data.upper())
        else:
            clist=courseName_get(form.CRSE.data.upper())
        form = CourseLookupForm(formdata=None)

    if formAdd.validate_on_submit():
        print(formAdd.course.data)
        print("test")
        wish_add(current_user.id,formAdd.course.data)
        return redirect(url_for('wishlist'))
    return render_template('lookup.html', form=form, clist=clist, formAdd=formAdd)


'''
Faculty page. Faculty and admin can 
view reports on wishes, and what students
wish for them.
'''

@app.route('/faculty', methods=['GET', 'POST'])
@login_required
def faculty():
    class CourseLookupForm(FlaskForm):
        SUB = TextField('Subject',validators=[DataRequired(),
                    AnyOf(subject_valid(),
                        message='That Subject could not be found.')])
        course = TextField('Course',validators=[DataRequired(),
                    AnyOf(class_valid(),
                        message='That course number could not be found.')])
        SEC = TextField('Section',validators=[DataRequired(),
                    AnyOf(section_valid(),
                        message='That section number could not be found.')])
        submit = SubmitField('View')
    wisher_list=[]
    form = CourseLookupForm()  
    if is_faculty() or is_admin():
        if form.validate_on_submit():
            wisher_list=faculty_lookup(form.SUB.data, form.course.data, form.SEC.data)
        return render_template('faculty.html', form=form,wisher_list=wisher_list)
    else:
        return render_template('unauthorized.html')

'''
Account management page. Allows user to
delete account, change password, email or
class year.
''' 

@app.route('/account',methods=['GET', 'POST'])
@login_required
def account_management():
    return render_template('account.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))