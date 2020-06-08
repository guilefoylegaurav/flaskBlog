from flask_blog import app, db, bcrypt, mail
from flask import render_template, url_for, flash, redirect
from flask_blog.forms import PasswordResetForm, LoginForm, RegistrationForm, UpdateAccount, CreatePost, PasswordRecoveryForm
from flask_blog.models import User, Post
from flask_login import current_user, login_user, logout_user
from flask import request
from flask_blog.utilities import save_picture
from flask_mail import Message


@app.route("/forgot_password/<token>", methods = ["GET","POST"])
def fix_password(token):
    if current_user.is_authenticated:
        flash("Don't try to mess with me!", 'danger')
        return redirect(url_for('home'))
    else:
        user = User.verify_auth_token(token)
        if user == None:
            flash("Invalid or expired link", 'danger')
            return redirect(url_for('home'))
        else:
            form = PasswordResetForm()
            if form.validate_on_submit():
                pw_hash = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
                user.password = pw_hash
                db.session.commit()
                flash("Successfully changed password", 'success')
                return redirect(url_for('login'))
            return render_template('password_reset.html', form = form)









@app.route("/forgot_password", methods=["GET", "POST"])
def fetch_password():
    if current_user.is_authenticated:
        flash("Don't try to mess with me!", 'danger')
        return redirect(url_for('home'))
    else:
        form = PasswordRecoveryForm()
        if form.validate_on_submit():
            gaurav = User.query.filter_by(email = form.email.data).first()
            token = gaurav.generate_token()

            msg = Message(subject = "Bam", 
                sender = 'noreply@demo.com',
                recipients = [form.email.data],
                body = f'''Head to this link to reset password:
                {url_for('fix_password', token = token)}
                ''' )
            mail.send(msg)
            flash('Check your email', 'success')
            return redirect(url_for('login'))
        return render_template('forgot_password.html', form = form)

    



@app.route("/home/<int:id>/delete", methods = ["POST"])
def delete(id):
    post = Post.query.get_or_404(id)
    if current_user.is_authenticated and post.user_id == current_user.id:
        db.session.delete(post)
        db.session.commit()
        flash('Deleted that post!', 'success')
    else:
        flash('Not authorized!')
    return redirect(url_for('home'))
    

@app.route("/")
@app.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=3)
    return render_template('home.html', posts=posts)



@app.route("/create_post", methods = ["GET", "POST"])
def create_post():
    if current_user.is_authenticated:
        form = CreatePost()
        if form.validate_on_submit():
            post = Post(title = form.title.data, content = form.content.data, user_id = current_user.id)
            db.session.add(post)
            db.session.commit()
            flash(f'Congrats! {current_user.username}, you have written your first post!', 'success')
            return redirect(url_for('home'))
        return render_template('create_post.html', title = 'Create Post', form = form)
        
    else:
       flash('You need to login for this!', 'danger')
    return redirect(url_for('login'))
        
    


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = form.username.data, email = form.email.data, password = hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    else:
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email = form.email.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember = form.remember.data)
                flash('You have been logged in!', 'success')
                return redirect(url_for('home'))
            else:
                flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title = 'Login', form = form)

@app.route("/home/<int:id>")
def fetch_post(id):
    my_post = Post.query.get_or_404(int(id))
    return render_template("one_post.html", title = my_post.title, post = my_post)


@app.route("/logout", methods = ['GET','POST'])
def logout():
    if current_user.is_authenticated:
        logout_user()
        flash('Hope you had a nice time! See you again!','success')
        
    return redirect(url_for('home'))
    
@app.route('/account', methods = ['GET','POST'])
def account():
    if current_user.is_authenticated:
        form = UpdateAccount()
        if request.method == 'GET':
            
            form.username.data = current_user.username
            form.email.data = current_user.email
            
        if form.validate_on_submit():
            if form.picture.data:
                current_user.image_file = save_picture(form.picture.data)
                    
            current_user.username = form.username.data
            current_user.email = form.email.data
            db.session.commit()
            flash('Updated details!','success')
        image_file = url_for('static', filename = 'profile_pictures/' + current_user.image_file)
        return render_template('account.html', title = 'Account', form = form, image_file = image_file)
    else:
        flash('Need to login for seeing this!','danger')
        return redirect(url_for('login'))
