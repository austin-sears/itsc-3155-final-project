#import statements
import firebase_admin
from firebase_admin import credentials, firestore, auth

#declares credentials to access firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

#sets up firebase client
db = firestore.client()


#############################################################################################################################################################################################################################################
#ACCOUNT RELATED FUNCTIONS
##########################

#sets all the data in repository, returning the id for the document that contains all of the information
def create_account(Username, Email, AboutMe, Password):
    user = auth.create_user(email = Email, password = Password)
    new_account_ref = db.collection('Users').document(user.uid)
    new_account_data = {'Username': Username, 'Email': Email, 'AboutMe': AboutMe, 'Password': Password}
    new_account_ref.set(new_account_data)
    new_account_id = new_account_ref.id
    return new_account_id

#returns the data from a user account from recieving the acct_id
def get_account(acct_id):
    acct_ref = db.collection('Users').document(acct_id)
    doc = acct_ref.get()
    if doc:
        acct_data = doc.to_dict()
        return acct_data
    else:
        return None

#logs out the active user
def logout_user(uid):
    auth.revoke_refresh_tokens(uid)
    return None

#deletes the current user
def delete_user(uid):
    auth.revoke_refresh_tokens(uid)
    db.collection('Users').document(uid).delete(uid).delete()
    auth.delete_user(uid)
    return None

#verify's that login is valid and sets the session token
def verify(email, password):
    try:
        user = auth.get_user_by_email(email)
        print (user)
        print (user.email)
        print (user.uid)
        ref = db.collection('Users').document(user.uid).get().to_dict()
        print (ref)
        if user and ref['Password'] == password:
            print("Login Successful")
            sessionToken = auth.create_custom_token(user.uid)
            print(sessionToken)
            return user.uid
        else: 
            print("Invalid Email or Password")
    except Exception as e:
        print("Authentication Failed: ", str(e))
        return None


#############################################################################################################################################################################################################################################
#POST RELATED FUNCTIONS
#######################

#gets all posts in database
def get_all_posts():
    all_posts = []
    post_ref = db.collection('Post')
    docs = post_ref.get()
    for doc in docs:
        post_data = doc.to_dict()
        all_posts.append(post_data)
    return all_posts

#gets a single post with post_id
def get_one_post(post_id):
    single_post = db.collection('Post').document(post_id)
    doc = single_post.get()
    if doc:
        post_data = doc.to_dict()
        return post_data
    else:
        return None

#uploads post to database
def create_post(Name, Link, Description, CreatedBy, Code):
    new_post_ref = db.collection('Post').document()
    new_post_data = {'Name': Name, 'Link': Link, 'Description': Description, 'CreatedBy': CreatedBy, 'Code': Code, 'post_id' : new_post_ref.id}
    new_post_ref.set(new_post_data)
    new_post_id = new_post_ref.id
    return new_post_id

#gets all posts from a selected user
def get_user_posts(username):
    users_posts = []
    posts_docs = db.collection('Post').where('CreatedBy', '==', username).get()
    for doc in posts_docs:
        post_data = doc.to_dict()
        users_posts.append(post_data)
    return users_posts

#deletes post from database
def delete_post(post_id):
    post_doc = db.collection('Post').document(post_id)
    print(post_doc)
    post_doc.delete()
    return None


#############################################################################################################################################################################################################################################
#COMMENT RELATED FUNCTIONS
##########################

#
def get_comments(post_id):
    comments = []
    comment_ref = db.collection('Comments').where('post_id', '==', post_id)
    docs = comment_ref.get()
    for doc in docs:
        comment_data = doc.to_dict()
        comments.append(comment_data)
    return comments

#
def add_comment(post_id, commenter_username, comment_text):
    new_comment_ref = db.collection('Comments').document()
    new_comment_data = {'post_id': post_id,'commenter_username': commenter_username, 'comment_text': comment_text}
    new_comment_ref.set(new_comment_ref.id)
    return new_comment_id

#
def remove_comment(comment_id):
    comment_ref = db.collection('Comments').document(comment_id)
    if comment_ref.get().exists:
        comment_ref.delete()
        return True
    else:
        return False



#############################################################################################################################################################################################################################################
#Task RELATED FUNCTIONS
##########################

#
def add_tag(tag_id, tag_name):
    tag_ref = db.colelction('Tags').docuemt(tag_id)
    if not tag.ref.get().exists:
        tag_data = {'tag_name': tag_name}
        tag_ref.set(tag_data)
        return True
    else:
        return False

def remove_tag(tag_id):
    tag_ref = db.colelction('Tags').docuemt(tag_id)
    if  tag_ref.get().exists:
        tag_ref.delete()
        return True
    else:
        return False

def get_tag(tag_id):
    tag_ref = db.collection('Tags').docuemt(tag_id)
    tag_data = tag.ref.get().to_dict()
    return tag_data if tag_data else None