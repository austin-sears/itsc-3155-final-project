import firebase_admin
from firebase_admin import credentials, firestore, auth

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

currentUser = {}

#
#TODO - FRONT END TEAM
#TRANSFER ALL VARIABLES TO MATCH THE NAMES USED IN THESE FUNCTIONS
#

#sets all the data in repository, returning the id for the document that contains all of the information
def create_account(Username, Email, AboutMe, Password):
    user = auth.create_user(email = Email, password = Password)
    new_account_ref = db.collection('Users').document(user.uid)
    new_account_data = {'Username': Username, 'Email': Email, 'AboutMe': AboutMe, 'Password': Password}
    new_account_ref.set(new_account_data)
    new_account_id = new_account_ref.id
    return new_account_id

def get_all_posts():
    all_posts = []
    post_ref = db.collection('Post')
    docs = post_ref.get()
    for doc in docs:
        post_data = doc.to_dict()
        all_posts.append(post_data)
    return all_posts

def get_one_post(post_id):
    single_post = db.collection('Post').document(post_id)
    doc = single_post.get()
    if doc:
        post_data = doc.to_dict()
        return post_data
    else:
        return None

#TODO
#Create a function that gets all comments from database
def get_comments(post_id):
    comments = []
    comment_ref = db.collection('Comments').where('post_id', '==', post_id)
    docs = comment_ref.get()
    for doc in docs:
        comment_data = doc.to_dict()
        comments.append(comment_data)
    return comments


#TODO
#Create a function that adds a comment to a given post
def add_comment(post_id, commenter_username, comment_text):
    new_comment_ref = db.collection('Comments').document()
    new_comment_data = {'post_id': post_id,'commenter_username': commenter_username, 'comment_text': comment_text}
    new_comment_ref.set(new_comment_ref.id)
    return new_comment_id


def create_post(Name, Link, Description, CreatedBy, Code):
    new_post_ref = db.collection('Post').document()
    new_post_data = {'Name': Name, 'Link': Link, 'Description': Description, 'CreatedBy': CreatedBy, 'Code': Code}
    new_post_ref.set(new_post_data)
    new_post_id = new_post_ref.id
    return new_post_id



def delete_account(acct_id):
    acct_ref = db.collection('Users').document(acct_id)
    acct_ref.delete()
    return None



def get_account(acct_id):
    acct_ref = db.collection('Users').document(acct_id)
    doc = acct_ref.get()
    if doc:
        acct_data = doc.to_dict()
        return acct_data
    else:
        return None

def verify(email, password):
    try:
        user = auth.get_user_by_email(email)
        print (user)
        print (user.email)
        print (user.uid)
        ref = db.collection('Users').document(user.uid).get().to_dict()
        print (ref)
        if ref['Email'] == email and ref['Password'] == password:
            print("Login Successful")
            currentUser['uid'] = user.uid
            currentUser['Username'] = ref['Username']
            currentUser['Email'] = ref['Email']
            currentUser['Password'] = ref['Password']
            currentUser['AboutMe'] = ref['AboutMe']
            return currentUser
        else: 
            print("Invalid Email or Password")
    except Exception as e:
        print("Authentication Failed: ", str(e))
        return None

