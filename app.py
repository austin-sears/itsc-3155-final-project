#adding import statements
from flask import Flask, jsonify, render_template, url_for, request, redirect, abort, session
from repository import *

#declares app
app = Flask(__name__)

#sets secret key
app.secret_key = "LOOP"


#############################################################################################################################################################################################################################################
#BASE PAGES & RUNNING APP
#########################

#runs app
if __name__ == "__main__":
    app.run()

#renders template for home
@app.route('/')
def index():
    return render_template('home.html')

#renders template for home
@app.route('/Home')
def home():
    return render_template('home.html')


#############################################################################################################################################################################################################################################
#USER RELATED FUNCTIONS
#######################

#logs in user and sets sessionToken id
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        # Extract login credentials from request
        email = request.form.get('email')
        password = request.form.get('password')
        print(email)
        print(password)
        # Sign in the user
        sessionToken_id = verify(email, password)
        print(sessionToken_id)
        user_dict = db.collection('Users').document(sessionToken_id).get().to_dict()
        print(user_dict)
        print('--------')
        session['user'] = {
            'st_id': sessionToken_id,
            'Username': user_dict['Username'],
            'user_dict': user_dict
        }
        return redirect('/feed')
    return render_template('login.html')

#logs out user
@app.route('/logout', methods = ['GET', 'POST'])
def logout():
    logout_user(session['user']['st_id'])
    del session['user']
    return redirect(url_for('login'))

#Creates account, sending to repository.py
@app.route('/create_profile', methods=['GET', 'POST'])
def create_acct():
    if request.method == 'POST':
        Username = request.form.get('new_username')
        Email = request.form.get('new_email')
        AboutMe = request.form.get('new_aboutme')
        Password = request.form.get('new_password')
        new_account_id = create_account(Username = Username, Email = Email, AboutMe = AboutMe, Password = Password)
        print('Registration successful. Please login to continue.')
        return redirect('/login')
    return render_template('Profile_Create.html')

#deletes account, calling function from repository.py
@app.route('/delete_acct')
def del_acct():
    delete_user(session['user']['st_id'])
    del session['user']
    return redirect(url_for('login'))

#renders template for home account page
@app.route('/profile')
def home_acct():
    user_info = session.get('user', None)
    print(user_info)
    posts = get_user_posts(user_info['Username'])

    return render_template('Account_page.html', account = user_info['user_dict'], posts = posts)


#############################################################################################################################################################################################################################################
#FEED RELATED METHODS
#####################

#adds element to feed
def add_element_to_feed(element):

        open("Feed_page.html", "r+")
        contents = file.read()
        start_index = contents.index("</template>") + 6  # find the index of "<body>" and add 6 to get after the tag
        new_contents = contents[:start_index] + "\n" + element + "\n" + contents[start_index:]  # insert new element
        file.seek(0)  # go back to the beginning of the file
        file.write(new_contents)  # overwrite with the new contents
        file.close()
        print ('Feed_page updated. File closed')

#renders template for the feed page
@app.route('/feed')
def feed():
    try:
        user_info = session.get('user', None)
        print(user_info)
        all_posts = get_all_posts()
        print(all_posts)
        return render_template('Feed_page.html', posts=all_posts, username = user_info['Username'])
    except Exception as e:
        abort(500, f"Internal Server Error: {str(e)}")

#############################################################################################################################################################################################################################################
#POST RELATED FUNCTIONS
#######################

#uploads post and calls function from repository.py
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

#second upload function
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

#gets single post calling repository,py function
@app.route('/Post/<post_id>')
def get_post(post_id):
    user_info = session.get('user', None)

    single_post = get_one_post(post_id)
    if single_post:
       if single_post['CreatedBy'] == user_info['Username']:
           CreatedBy = True
       else:
           CreatedBy = False
        #   comments = get_comments(post_id)
       return render_template('Post_Page.html', post_id = post_id, post = single_post, username = user_info, CreatedBy = CreatedBy)
    return render_template('Post_Page.html')

#deletes post, calling repository.py function
@app.route('/Post/delete/<post_id>')
def del_post(post_id):
    # post_id = request.form.get('post_id')
    print(post_id)
    delete_post(post_id)
    return redirect('/profile')


#############################################################################################################################################################################################################################################
#COMMENT RELATED FUNCTIONS
##########################

@app.route('/get_comment', methods=['GET'])
def get_comment():
    return jsonify({'message': 'Post_Page.html'})

@app.route('/add_comment', methods=['POST'])
def add_comment():
    return jsonify({'message': 'Post_Page.html' })

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

@app.route('/remove_comment', methods = ["DELETE"])
def remove_comment_route():
    comment_id = request.args.get('comment_id')
    if not comment_id:
        return jsonify({'error': 'Missing required parameter: comment_id'}), 400
    success = remove_comment(comment_id)

    if success:
        return jsonify({'message': 'Comment removed successfully'})
    else:
        return jsonify({'error': 'Comment not found or could not be removed'}), 404


#############################################################################################################################################################################################################################################
#TAG RELATED FUNCTIONS
##########################

@app.route('/add_tag', methods=['POST'])
def add_tag_route():
    data = request.json
    tag_id = data.get('tag_id')
    tag_name = data.get('tag_name')

    if not tag_id or not tag_name:
        return jsonify({'error': 'Missing required parameters'}), 400
    success = add_tag(tag_id, tag_name)

    if success:
        return jsonify({'message': 'Tag added successfully'})
    else:
        return jsonify({'error': "Tag with given ID already exists"})

@app.route('/remove_tag', methods=[DELETE])
def remove_tag_route():
    tag_id = request.args.get('tag_id')

    if not tag_id:
        return jsonify({'error': 'Missing requred parameters:'})
    success = remove_tag(tag_id)

    if success:
        return jsonify({'message': 'Tag removed successfully'})
    else:
        return jsonify({'error': 'Tag not found or could not be removed'})

@app.route('get_tag', methods=['GET'])
def get_tag_route():
    tag_id = requests.args.get('tag_id')

    if not tag_id:
        return jsonify({'error': 'Missing requred parameters: tag_id'})
    tag_data = get_tag(tag_id)

    if tag_data:
        return jsonify({'tag_data': tag_data})
    else:
        return jsonify({'error': 'Tag not found'}), 404