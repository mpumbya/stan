from flask import flash, redirect, render_template, url_for, request, session, Markup, abort
from this_app import app
from this_app.models import User, Shoplist, Activity
from werkzeug.security import check_password_hash
from .forms import SignupForm, LoginForm,  ShoplistForm, ActivityForm

# Set var to check if user is logged in
global logged_in
logged_in = False