from flask import (
    Flask, render_template,request,
    flash,redirect,url_for, session,jsonify
)
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Users, Polls, Topics, Options


votr = Flask(__name__)

#load config form teh config file we created earlier
votr.config.from_object('config')

#initialize and create the database
db.init_app(votr)
db.create_all(app=votr)

@votr.route('/')
def home():
    return render_template('index.html')

@votr.route('/signup', methods = ['GET','POST'])
def signup():
    if request.method == 'POST':
        #get the user details from the form
        email = request.form['username']
        username = request.form['username']
        password = request.form['password']
	
        	#hash the password 
        password = generate_password_hash(password)
    	
        user = Users(email=email, username=username, password=password)
    
        db.session.add(user)
        db.session.commit()
        
        flash('Thanks for signing up please login')
        
        return redirect(url_for('home'))
    
    #it's a GET request, just render the template
    return render_template('signup.html')

@votr.route('/login', methods=['POST'])
def login():
    # we don't need to check the request type as flask will raise a bad request
    # error if a request aside from POST is made to this url
    
    username = request.form['username']
    password = request.form['password']

    #serach the database for the User
    user = Users.query.filter_by(username=username).first()

    if user: 
        password_hash = user.password
        
    if check_password_hash(password_hash, password):
        #The hash matches the password int eh database log the user i
        session['user'] = username
        flash('Login was successful')
        
    else:
        #user wasn't found in the databse
        flash('Username or password is incorrect please try again', 'error')
    
    return redirect(url_for('home'))

@votr.route('/logout')
def logout():
    if 'user' in session:
        session.pop('user')
        flash('We hope to see you again!')

    return redirect(url_for('home'))

@votr.route('/polls')
def polls():
    return render_template('polls.html')
'''
@votr.route('/api/polls', methods = ['GET','POST'])
#retrieves/adds polls from/to the database
def api_polls():
    if request.moth == 'POST':
        #get the poll and save it in the database
        poll = request.get_json()
        return "The title of the poll is {} and the options are {} and {}".format(poll['title'], *poll['options'])
     
    else:
        #query the db and return all the polls as json 
        all_polls = {}
        
        #get all the topics in the database
        topics = Topics.query.all()
        for topic in topics: 
            # for each topic get the all options that are associated with it
            all_polls[topic.title] = {'options': [poll.option.name for poll in Polls.query.filter_by(topic=topic)]}
            
        return jsonify(all_polls)
 '''   

@votr.route('/it')
def run_home():
    return 'wudup homie'

if __name__ == '__main__':
    votr.run(debug=True)
