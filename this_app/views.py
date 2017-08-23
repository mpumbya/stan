from flask import flash, redirect, render_template, url_for, request, session, Markup, abort
from this_app import app
from this_app.models import User, Shoplist, Activity
from werkzeug.security import check_password_hash
from .forms import SignupForm, LoginForm,  ShoplistForm, ActivityForm

# Set var to check if user is logged in
global logged_in
logged_in = False

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    global logged_in
    if logged_in:
        return logout_required()
    else:
        form = SignupForm(request.form)

        if form.validate_on_submit(): 
            # Throw an error if email is already registered
            users_dict = User.users.items()    
            existing_user = {k:v for k, v in users_dict if form.email.data in v['email']}
            if existing_user:
                email_exists = Markup("<div class='alert alert-info' role='alert'>\
                                            The email entered is registered, please login instead\
                                        </div>")
                flash(email_exists)

                return render_template("login.html", form=LoginForm())
            
            # If email is not registered, register the user
            new_user = User(form.email.data, form.username.data, form.password.data)
            new_user.create_user()

            for key, value in users_dict:     # gets id, eg 2
                if form.email.data in value['email']:
                    session['user_id'] = key

            successful_signup = Markup("<div class='alert alert-success' role='alert'>\
                                            Account created successfully\
                                        </div>")
            flash(successful_signup)

            return redirect(url_for("login", form=LoginForm()))

        if form.errors:
            if len(form.password.data) < 4:
                form_error = Markup("<div class='alert alert-danger' role='alert'>\
                                        Password should be more than 4 chars\
                                    </div>")
                flash(form_error)
            if len(form.username.data) < 4:
                form_error = Markup("<div class='alert alert-danger' role='alert'>\
                                        Username should be more than 4 chars\
                                    </div>")
                flash(form_error)
            else:
                form_error = Markup("<div class='alert alert-danger' role='alert'>\
                                        Enter valid email, like demo@mail.com\
                                    </div>")
                flash(form_error)

        # If GET
        logged_in = False
        return render_template("signup.html", form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    global logged_in
    if logged_in:
        return logout_required()
    
    # If user is not logged in
    form = LoginForm(request.form)

    if form.validate_on_submit():
        users_dict = User.users.items()
        existing_user = {k:v for k, v in users_dict if form.email.data in v['email']}
        if existing_user:
            valid_user = [v for v in existing_user.values() if check_password_hash(v['password'], form.password.data)]
            if valid_user:
                #global logged_in
                logged_in = True

                successful_login = Markup("<div class='alert alert-success' role='alert'>\
                                                Login successful\
                                            </div>")
                flash(successful_login)

                for key, value in users_dict:
                    if form.email.data in value['email']:
                        session['user_id'] = key

                        shoplist_dict = Shoplist. Shoplists.items()
                        has_shops = {k:v for k, v in shoplist_dict if session['user_id'] in v.values()}
    
                        # If this user has  Shoplists
                        if has_shops:
                            return render_template('show_shoplists.html', form= ShoplistForm(), data=has_shops)

                        # If user has no  Shoplists
                        return redirect(url_for('show_shoplists', form= ShoplistForm()))
            # If wrong password
            incorrect_password = Markup("<div class='alert alert-danger' role='alert'>\
                                            Incorrect password. Please use the correct password\
                                        </div>")
            flash(incorrect_password)

            return render_template("login.html", form=form)

        # If email is not registered yet
        not_registered = Markup("<div class='alert alert-info' role='alert'>\
                                    Email not yet registered. Please create account to continue\
                                </div>")
        flash(not_registered)

        alt_form = SignupForm()
        return redirect(url_for('signup', form=alt_form ))

    if form.errors:
        form_error = Markup("<div class='alert alert-danger' role='alert'>\
                                Enter valid email, like demo@mail.com\
                            </div>")
        flash(form_error)

    # If GET
    logged_in = False
    return render_template("login.html", form=form)

@app.route('/show_shoplists', methods=['GET', 'POST'])
def show_shoplists():
    if logged_in:
        form =  ShoplistForm(request.form)
        if form.validate_on_submit():
            new_shoplist =  Shoplist(form.name.data, form.description.data)
            new_shoplist.create_shoplist()

            shoplist_created = Markup("<div class='alert alert-success' role='alert'>\
                                             Shoplist created successfully\
                                        </div>")
            flash(shoplist_created)

            shoplist_dict =  Shoplist. Shoplists.items()
            user_shoplists = {k:v for k, v in shoplist_dict if session['user_id']==v['user_id']}

            return render_template("show_shoplists.html", form=form, data=user_shoplists)

        if form.errors:
            form_error = Markup("<div class='alert alert-danger' role='alert'>\
                                    Form error. Could not create  Shoplist *#*#*??\
                                </div>")
            flash(form_error)

        shoplist_dict =  Shoplist. Shoplists.items()
        # Check if user has  Shoplists
        has_shops = {k:v for k, v in shoplist_dict if session['user_id'] in v.values()}

        if has_shops:

            return render_template('show_shoplists.html', form=form, data=has_shops)

        # If GET
        return render_template("show_shoplists.html", form=form)
    
    # If user is not logged in:
    return login_required()

@app.route('/show_activities/<int:shoplist_id>', methods=['GET', 'POST'])
def show_activities(shoplist_id):
    """
    Show a  Shoplists's activities
    """
    form = ActivityForm(request.form)
    if logged_in:

        # Check if shop has activities
        all_activities = Activity.activities
        shop_activities = {k:v for k, v in all_activities.items() if shoplist_id==v['shoplist_id']}
        if shop_activities:
            return render_template("show_activities.html", form=form, shoplist_id=shoplist_id, data=shop_activities)

        # If buck ids do not match
        return render_template('show_activities.html', form=form, shoplist_id=shoplist_id)

    # If user is not logged in:
    return login_required()

@app.route('/show_activities/create_activity/<int:shoplist_id>', methods=['GET', 'POST'])
def create_activity(shoplist_id):
    """
    Creates and adds activities to a  Shoplist
    """
    form = ActivityForm(request.form) 
    if form.validate_on_submit():
        new_activity = Activity(form.title.data, form.description.data, form.status.data)
        new_activity.create_activity(shoplist_id)

        activity_created = Markup("<div class='alert alert-success' role='alert'>\
                                         Shoplist Item created successfully\
                                    </div>")
        flash(activity_created)
        
        # Select the activity for the current list and pass it to show_activities
        all_activities = Activity.activities.items()
        created_activities = {k:v for k, v in all_activities if shoplist_id==v['shoplist_id']}
        
        if created_activities:

            return redirect(url_for("show_activities", form=form, data=all_activities, shoplist_id=shoplist_id))
        
        # Else if the activity was not created
        return redirect(url_for('show_activities', form=form, shoplist_id=shoplist_id))

    if form.errors:
        form_error = Markup("<div class='alert alert-danger' role='alert'>\
                                Form error. Could not create  Shoplist Items *#*#*??\
                            </div>")
        flash(form_error)

    # If GET
    return render_template('show_activities.html', form=form, shoplist_id=shoplist_id)

@app.route('/delete_shoplist', methods=['GET', 'POST'])
def delete_shoplist():
    if logged_in: 
        shoplists_dict =  Shoplist. Shoplists.items()
        user_shoplists = {k:v for k, v in shoplists_dict if session['user_id']==v['user_id']}
        Shoplist.delete_shoplist()

        return redirect(url_for("show_shoplists", data=user_shoplists))

@app.route('/show_activities/delete_activity/<int:shoplist_id>/<int:key>', methods=['GET', 'POST'])
def delete_activity(shoplist_id, key):
    if logged_in:
        all_activities = Activity.activities
        shop_activities = {k:v for k, v in all_activities.items() if shoplist_id==v['shoplist_id']}
        if shop_activities:
            Activity.delete_activity(shoplist_id, key)

            return redirect(url_for("show_activities", form=ActivityForm(), shoplist_id=shoplist_id, data=shop_activities))
        # If buck not found
        return render_template("show_activities.html", form=ActivityForm(), shoplist_id=shoplist_id, data=shop_activities)
                

@app.route('/edit_shoplist', methods=['GET', 'POST'])
def edit_shoplist():
    if logged_in:
        form =  ShoplistForm(request.form)

        shoplists_dict =  Shoplist. Shoplists.items()
        user_shoplists = {k:v for k, v in shoplists_dict if session['user_id']==v['user_id']}
        Shoplist = {k:v for k, v in user_shoplists.items() if k==int(request.form['key'])}

        if form.validate_on_submit():
             Shoplist =  Shoplist(form.name.data, form.description.data)

             Shoplist.edit_shoplist()

        return redirect(url_for("show_shoplists", data=user_shoplists))

        if form.errors:
            form_error = Markup("<div class='alert alert-danger' role='alert'>\
                                    Form error. Could not edit  Shoplist *#*#*??\
                                </div>")
            flash(form_error)

        # If GET
        return redirect(url_for("show_shoplists", form=form))

@app.route('/show_activities/edit_activity/<int:shoplist_id>/<int:key>', methods=['GET', 'POST'])
def edit_activity(shoplist_id, key):
    if logged_in:
        form = ActivityForm(request.form)

        all_activities = Activity.activities.items()

        if form.validate_on_submit():
            new_activity = Activity(form.title.data, form.description.data, form.status.data)

            new_activity.edit_activity(shoplist_id, key)

            return redirect(url_for("show_activities", form=form, shoplist_id=shoplist_id, data=all_activities))

        if form.errors:
            form_error = Markup("<div class='alert alert-danger' role='alert'>\
                                    Form error. Could not edit Items *#*#*??\
                                </div>")
            flash(form_error)

        # If GET
        return redirect(url_for("show_activities", form=form, shoplist_id=shoplist_id, data=all_activities))

@app.route('/logout')
def logout():
    global logged_in
    logged_in = False
    session.pop('user_id', None)

    return redirect(url_for('index')) 

def login_required():
    # If user is not logged in:
    sign_in_first = Markup("<div class='alert alert-danger' role='alert'>\
                                Please sign in first to see your  Shoplists\
                            </div>")
    flash(sign_in_first)

    return render_template("login.html", form=LoginForm())

def logout_required():
    logout_instead = Markup("<div class='alert alert-info' role='alert'>\
                                    You are logged in. Please log out\
                                </div>")
    flash(logout_instead)

    return redirect(url_for("show_shoplists", form= ShoplistForm()))
