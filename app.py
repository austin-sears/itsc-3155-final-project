# version 4
from flask import Flask, render_template, url_for, request, redirect
from repository import *

app = Flask(__name__)

#
#USE ALL THE FUNCTIONS FROM THIS PAGE DO NOT USE REPOSITYORY.PY PAGE 
#
#
#TODO - Matt
#add abort errors for each function
# if username = '' or prefname = '' .....
# abort(400)
#^^^ This is an example for you
#
#
#
#TODO - FRONT END TEAM - only add in html files
#add names for each of the imputs, you can see how I did this in the username input on the Profile_Create page (the part where it says name ="new_username")
#you can reference create_acct and new_post to see what the names are
#
#TODO - FRONT END TEAM CONT
#make sure the names are the same as what is in single quotes 
#create an html file for account page other than home
#either create or upload the feed.html file to the project
#need an html file for a single post page (single_post.html)
#I changed Def post to def home post will now be the post page
#
#TODO - FRONT END TEAM CONT AGAIN (OR MATT)
#When referencing the data to display you will need to use the variables I used 
#for single_post.html (refer to line 84-103) use post and do post.name, post.whatever you need
#You will need to do this with all information, refer to this file and then hook up the correct variablees
#
#RENDER TEMPLATES-----------------------------------------------
#

#TODO REESE - For render templates and html
#need to make a file in html for account page other than home (account.html)
#need to make an app.route for account page (account)
#need to make an app.route upload or create post page 
#need to make an app.route for a single post page
@app.route('/')
def index():
    return render_template('login.html')

@app.route('/create_profile')
def create():
    return render_template('Profile_Create.html')

@app.route('/Home')
def home():
    return render_template('home.html')

@app.route('/upload')
def upload():
    return render_template('upload.html')

@app.route('/feed')
def feed():
    return render_template('Feed_page.html')

@app.route('/Post')
def post():
    return render_template('Post_Page.html')

@app.route('/get_comment', methods=['GET'])
def get_comment():
    return jsonify({'message': 'Post_Page.html'})

@app.route('/add_comment', methods=['POST'])
def add_comment():
    return jsonify({'message': 'Post_Page.html' })

#
#FUNCTIONS----------------------------------------------------
#

#Creates post
@app.route('/create_acct', methods=['GET', 'POST'])
def create_acct():
    Username = request.form.get('new_username')
    PrefName = request.form.get('new_prefname')
    Title = request.form.get('new_title')
    Email = request.form.get('new_email')
    AboutMe = request.form.get('new_aboutme')
    Password = request.form.get('new_password')
    #Backend: Add a github variable name and corresponding functions.
    print(Username + " "+ PrefName + " "+ Email + " "+ Password + " ")

    user = auth.create_user(email = Email, password = Password)

    new_account_id = create_account(Username = Username, Prefname = PrefName, Title = Title, Email = Email, AboutMe = AboutMe, Password = Password)
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

@app.route('/feed')
def get_posts():
    try:
        all_posts = get_all_posts()
   
        if all_posts:
            return render_template('Feed_page.html', posts=all_posts)
        else:
            abort(404, "No posts found.")
    except Exception as e:
        abort(500, f"Internal Server Error: {str(e)}")

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


@app.route('/login', methods=['POST'])
def login():
    # Extract login credentials from request
    email = request.form['email']
    password = request.form['password']

    # Sign in the user
    try:
        user = auth.sign_in_with_email_and_password(email, password)
    except FirebaseAuthError as e:
        print(e.message)
        return redirect(url_for('login'))

    # Login successful
    print('Login successful.')
    return redirect(url_for('home'))

#Placeholder FOR REESE 
#DO NOT EDIT THIS FILE 

if __name__ == "__main__":
    app.run()
