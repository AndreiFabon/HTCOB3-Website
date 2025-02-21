from flask import Blueprint, render_template, request, session, flash, redirect, url_for
from .models import Team, Flag, FlagSubmission  # Import the Team model
from . import db  # For the database connection

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template('index.html')

@views.route('/submit', methods=['GET', 'POST'])
def submit():
    if 'team_id' not in session:
        flash('You must be logged in to submit a flag.', category='error')
        return redirect(url_for('auth.login'))

    team_id = session['team_id']
    team = Team.query.get(team_id)

    if request.method == 'POST':
        flag_input = request.form.get('flag')

        # Check if the flag exists in the 'flags' table
        flag = Flag.query.filter_by(flag=flag_input).first()
        if not flag:
            flash('Invalid flag!', category='error')
        else:
            # Check if the team has already submitted this flag
            existing_submission = FlagSubmission.query.filter_by(team_id=team_id, flag_id=flag.id).first()
            if existing_submission:
                flash('You have already submitted this flag!', category='error')
            else:
                # Add the flag submission and update the team's score
                new_submission = FlagSubmission(team_id=team_id, flag_id=flag.id)
                db.session.add(new_submission)
                team.points += flag.points
                db.session.commit()
                flash(f'Flag submitted successfully! You earned {flag.points} points.', category='success')

    return render_template('submit.html', team=team)

@views.route('/leaderboard')
def leaderboard():
    # Query the top 3 teams by score in descending order
    top_teams = Team.query.order_by(Team.points.desc()).limit(5).all()
    
    # Convert the query result to a format that can be passed to the template
    teams = [{'team': team.name, 'score': team.points} for team in top_teams]
    
    return render_template('leaderboard.html', teams=teams)




