from system.core.controller import *

class Users(Controller):
    def __init__(self, action):
        super(Users, self).__init__(action)

        self.load_model('User')
        self.db = self._app.db

    def index(self):
        return self.load_view('index.html')

    def create(self):
        info = {
             "first_name" : request.form['first_name'],
             "last_name" : request.form['last_name'],
             "email" : request.form['email'],
             "password" : request.form['password'],
             "pw_confirmation" : request.form['pw_confirmation']
        }

        create_status = self.models['User'].create_user(info)

        if create_status['status'] == True:
            session['id'] = create_status['user']['id'] 
            session['name'] = create_status['user']['first_name']
            session['message'] = 'Successfully registered!'

            return self.load_view('success.html')
        else:
            for message in create_status['errors']:
                flash(message, 'regis_errors')
            
            return redirect('/')

    def login(self):
        info = {
            "email" : request.form['email'],
            "password" : request.form['password']
        }
        userlogin = self.models['User'].login_user(info)
        print userlogin
        if userlogin:
            session['message'] = 'Successfully logged in!'
            session['name'] = userlogin
            return self.load_view('success.html') 

        elif not userlogin:
            flash('Please enter a valid email and password', 'login_errors')
            return redirect('/')