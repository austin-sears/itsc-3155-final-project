# version 4
from flask import Flask, render_template, url_for, request, redirect, abort, session
from repository import *
# from flask_session import Session
# from flask_firebase import Firebase
# from flask_firebase_session import FlaskFirebaseSession

app = Flask(__name__)

# app.config['SECRET_KEY'] = "yasdfghjk"

# firebase = Firebase(app)
# Session(app)

currentUser = {}

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/create_profile')
def create():
    return render_template('Profile_Create.html')

@app.route('/Home')
def home():
    return render_template('home.html')

@app.route('/upload', methods = ['GET', 'POST'])
def upload():
    print(request.method)
    if request.method == 'POST':
        Name = request.form.get("new_name")
        Link = request.form.get("new_link")
        Description = request.form.get("new_description")
        CreatedBy = request.form.get("CreatedBy")
        Code = request.form.get("new_code")
        print(Name)
        print(Link)
        print(Description)
        print(CreatedBy)
    
        if not Name or not Link or not Description or not CreatedBy or not Code:
            abort(400, "Missing required information. Please fill out all fields.")

        new_post_id = create_post(Name = Name, Link = Link, Description = Description, CreatedBy = CreatedBy, Code = Code)
        if new_post_id:
            return redirect('/feed')
        else:
            return abort(500, "Failed to Create Post")
    return render_template('upload.html')

@app.route('/Post')
def post():
    return render_template('Post_Page.html')

@app.route('/get_comment', methods=['GET'])
def get_comment():
    return jsonify({'message': 'Post_Page.html'})

@app.route('/add_comment', methods=['POST'])
def add_comment():
    return jsonify({'message': 'Post_Page.html' })

@app.route('/profile')
def home_acct():
    return render_template('Account_page.html')

#
#FUNCTIONS----------------------------------------------------
#

#Creates post
@app.route('/create_acct', methods=['GET', 'POST'])
def create_acct():
    Username = request.form.get('new_username')
    Email = request.form.get('new_email')
    AboutMe = request.form.get('new_aboutme')
    Password = request.form.get('new_password')
    #Backend: Add a github variable name and corresponding functions.
    print(Username +" "+ Email + " "+ Password + " ")

    new_account_id = create_account(Username = Username, Email = Email, AboutMe = AboutMe, Password = Password)
    print('Registration successful. Please login to continue.')
    return redirect(f'/account/{new_account_id}')
    # try:
    #     if not Username or not PrefName or not Email or not AboutMe or not Password:
    #         abort(400, "Missing required information. Please fill out all fields.")

        
    # except:
    #     print("Registration unsuccessful.")
    #     return redirect(url_for('create'))


#gets account info
#FRONT END TEAM - NAME account html page "account.html"
@app.route('/account/<acct_id>')
def get_acct(acct_id):
    single_account = get_account(acct_id)
    if single_account:
        return render_template('Account_page.html', account = single_account)
    else: 
        abort(404, "Account not found.")

@app.route('/Post')
def get_post():
    single_post = get_one_post(post_id)
    if single_post:
        return render_template('Post_Page.html', post = single_post)
    else:
        abort(404, f"Post with ID {post_id} not found.")

@app.post('/upload')
def new_post():
    Name = request.form.get("new_name")
    Link = request.form.get("new_link")
    Description = request.form.get("new_description")
    CreatedBy = request.form.get("CreatedBy")
    Code = request.form.get("new_code")
    print('Upload successful.')
    
    if not Name or not Link or not Description or not CreatedBy or not Code:
        abort(400, "Missing required information. Please fill out all fields.")

    new_post_id = create_post(Name = Name, Link = Link, Description = Description, CreatedBy = CreatedBy, Code = Code)
    return redirect('/feed')


@app.route('/Account/<int:post_id>/delete')
def del_acct(acct_id):
    try:
        if get_account(acct_id):
            delete_account(acct_id)
            return redirect('/login')
        else:
            abort(404, "Account not found.")
    except Exception as e:
        abort(500, f"Internal Server Error: {str(e)}")

@app.route('/get_comment', methods=['GET'])
def get_comments_route():
    post_id = request.args.get('post_id')
    if not post_id:
        return jsonify({'error': 'Missing required parameter: post_id'}), 400
    comments = get_comments(post_id)
    return jsonify({'comments': comments})


@app.route('/add_comment', methods=['POST'])
def add_comment_route():
    data = request.json
    post_id = data.get('post_id')
    commenter_username = data.get('commenter_username')
    comment_text = data.get('comment_text')

# firebase_admin.initialize_app()


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        # Extract login credentials from request
        email = request.form.get('email')
        password = request.form.get('password')
        print(email)
        print(password)
        # Sign in the user
        try:
            user = verify(email, password)
            print(user)
            if user != None:
                currentUser = user
                print("debug app.py login function")
                print(currentUser)
                # session['uid'] = currentUser.get('uid')
                return redirect('/feed')
        except Exception as e:
            print(e)
            return redirect(url_for('login'))

        # Login successful
            print('Login successful.')
        return redirect('/feed')
        #return redirect(f'/account/{new_account_id}')
    return render_template('login.html')

@app.route('/feed')
def feed():
    try:
        all_posts = get_all_posts()
        print("feed")
        print(currentUser.get('uid'))
        if True: # 'uid' in session:
            # uid = session['uid']
            if all_posts:
                return render_template('Feed_page.html', posts=all_posts)
            else:
                abort(404, "No posts found.")
    except Exception as e:
        abort(500, f"Internal Server Error: {str(e)}")
    return render_template('Feed_page.html')

#Placeholder FOR REESE 
#DO NOT EDIT THIS FILE 

if __name__ == "__main__":
    app.run()
