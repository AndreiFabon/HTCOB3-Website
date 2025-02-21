from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from .models import Team  # Import the Team model
from . import db
import re  # For team name validation

auth = Blueprint('auth', __name__)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        team_name = request.form.get('teamName')
        password = request.form.get('password')
        confirm_password = request.form.get('password1')

        # Validate team name
        if not team_name or len(team_name) < 3 or len(team_name) > 50:
            flash("Team name must be between 3 and 50 characters.", category="error")
        elif not re.match("^[a-zA-Z0-9_-]+$", team_name):
            flash("Team name can only contain letters, numbers, hyphens, and underscores.", category="error")
        elif password != confirm_password:
            flash('Passwords do not match.', category='error')
        elif Team.query.filter_by(name=team_name).first():
            flash('Team name already exists.', category='error')
        else:
            # Hash password and save new team
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
            new_team = Team(name=team_name, password=hashed_password)
            db.session.add(new_team)
            db.session.commit()

            flash('Account created successfully! Please log in.', category='success')
            return redirect(url_for('auth.login'))  # Redirect to login

    return render_template('signup.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        team_name = request.form.get('teamName')
        password = request.form.get('password')

        team = Team.query.filter_by(name=team_name).first()

        if not team or not check_password_hash(team.password, password):
            flash('Invalid credentials.', category='error')  # Generic error message
        else:
            flash('Logged in successfully!', category='success')

            # Store team info in session
            session['team_id'] = team.id
            session['team_name'] = team.name

            return redirect(url_for('views.home'))  # Redirect to home/dashboard

    return render_template('login.html')