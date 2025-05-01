from flask import Flask
from flask import render_template
from flask import request,session, redirect, url_for, send_from_directory,make_response 
from flask_session import Session
from datetime import timedelta
from user import user
from vehicle import vehicle
import time
import datetime

app = Flask(__name__,static_url_path='')

app.config['SECRET_KEY'] = '5sdghsgRTg'
app.config['SESSION_PERMANENT'] = True
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=5)
sess = Session()
sess.init_app(app)

@app.route('/')
def home():
    return redirect('/login')

@app.context_processor
def inject_user():
    return dict(me=session.get('user'))

def format_datetime(value, format='%Y-%m-%d %H:%M:%S'):
    if value is None:
        return ''
    try:
        return value.strftime(format)
    except AttributeError:
        return 'NA'

app.jinja_env.filters['format_datetime'] = format_datetime

@app.route('/login',methods = ['GET','POST'])
def login():
    if request.form.get('name') is not None and request.form.get('password') is not None:
        u = user()
        if u.tryLogin(request.form.get('name'),request.form.get('password')):
            print("Login ok")
            session['user'] = u.data[0]
            session['active'] = time.time()
            return redirect('main')
        else:
            print("Login Failed")
            return render_template('login.html', title='Login', msg='Incorrect username or password.')
    else:   
        if 'msg' not in session.keys() or session['msg'] is None:
            m = 'Type your email and password to continue.'
        else:
            m = session['msg']
            session['msg'] = None
        return render_template('login.html', title='Login', msg=m)    

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    u = user()  # Single user object for this request
    
    if request.method == 'POST':
        d = {
            'fname': request.form.get('fname'),
            'email': request.form.get('email'),
            'height': request.form.get('height'),
            'weight': request.form.get('weight'),
            'DOB': request.form.get('DOB'),
            'gender': request.form.get('gender'),
            'password': request.form.get('password'),
            'password2': request.form.get('password2'),
            'role': request.form.get('role')  # User selects role here
        }

        u.set(d)  # Set data on this user object
        
        if u.verify_new():
            u.insert()
            return render_template('ok_dialog.html', msg="Account created successfully.")
        else:
            return render_template('users/add.html', obj=u, msg=" ".join(u.errors))
    
    u.createBlank()
    return render_template('users/add.html', obj=u)

    
@app.route('/logout',methods = ['GET','POST'])
def logout():
    if session.get('user') is not None:
        del session['user']
        del session['active']
    return render_template('login.html', title='Login', msg='You have logged out.')
@app.route('/main')
def main():
    if checkSession() == False: 
        return redirect('/login')
    
    if session['user']['role'] == 'admin':
        return render_template('main.html', title='Main menu') 
    else:
        return render_template('main.html', title='Main menu') 

@app.route('/users/manage',methods=['GET','POST'])
def manage_user():
    if checkSession() == False or session['user']['role'] != 'admin': 
        return redirect('/login')
    o = user()
    action = request.args.get('action')
    pkval = request.args.get('pkval')
    if action is not None and action == 'delete': #action=delete&pkval=123
        o.deleteById(request.args.get('pkval'))
        return render_template('ok_dialog.html',msg= "Deleted.")
    if action is not None and action == 'insert':
        d = {}
        d['fname'] = request.form.get('fname')
        d['email'] = request.form.get('email')
        d['role'] = request.form.get('role')
        d['password'] = request.form.get('password')
        d['password2'] = request.form.get('password2')
        o.set(d)
        if o.verify_new():
            #print(o.data)
            o.insert()
            return render_template('ok_dialog.html',msg= "User added.")
        else:
            return render_template('users/add.html',obj = o)
    if action is not None and action == 'update':
        o.getById(pkval)
        o.data[0]['fname'] = request.form.get('fname')
        o.data[0]['email'] = request.form.get('email')
        o.data[0]['role'] = request.form.get('role')
        o.data[0]['password'] = request.form.get('password')
        o.data[0]['password2'] = request.form.get('password2')
        if o.verify_update():
            o.update()
            return render_template('ok_dialog.html',msg= "User updated. ")
        else:
            return render_template('users/manage.html',obj = o)
    if pkval is None:
        o.getAll()
        return render_template('users/list.html',obj = o)
    if pkval == 'new':
        o.createBlank()
        return render_template('users/add.html',obj = o)
    else:
        print(pkval)
        o.getById(pkval)
        return render_template('users/manage.html',obj = o)
    
##############################################################################
###################             Profile:
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if not checkSession():
        return redirect('/login')

    u = user()
    uid = session['user']['uid']
    u.getById(uid)

    if request.method == 'POST':
        # Get form inputs (can be empty)
        dob = request.form.get('DOB')
        height = request.form.get('height')
        weight = request.form.get('weight')
        gender = request.form.get('gender')

        # Update the user object
        u.data[0]['DOB'] = dob if dob else None
        u.data[0]['height'] = height if height else None
        u.data[0]['weight'] = weight if weight else None
        u.data[0]['gender'] = gender if gender else None

        u.update()
        session['user'] = u.data[0]  # Refresh session data
        msg = "Profile updated successfully."
        return render_template('profile.html', me=u.data[0], msg=msg)

    return render_template('profile.html', me=u.data[0])


##############################################################################
###################           Workouts:
#Admin Managing Workouts
@app.route('/workouts/manage', methods=['GET', 'POST'])
def manage_workouts():
    if not checkSession() or session['user']['role'] != 'admin':
        return redirect('/login')

    from workout import workout
    o = workout()
    action = request.args.get('action')
    pkval = request.args.get('pkval')

    if action == 'delete' and pkval:
        o.delete_workout(pkval)
        return render_template('ok_dialog.html', msg="Workout deleted.")

    if action == 'insert' and request.method == 'POST':
        o.add_workout(request.form.get('workoutname'), request.form.get('category'))
        return render_template('ok_dialog.html', msg="Workout added.")

    if action == 'update' and pkval and request.method == 'POST':
        o.update_workout(pkval, request.form.get('workoutname'), request.form.get('category'))
        return render_template('ok_dialog.html', msg="Workout updated.")

    if pkval is None:
        workouts = o.get_all_workouts()
        return render_template('workouts/list.html', workouts=workouts)

    if pkval == 'new':
        return render_template('workouts/add.html')

    else:
        workout_data = o.get_workout_by_id(pkval)
        if workout_data:  # Check if workout exists
            return render_template('workouts/manage.html', workout=workout_data)
        else:
            # Show message or empty form when no data
            return render_template('workouts/manage.html', workout=None)

#Customer Viewing and Starting/Completing workouts
@app.route('/workouts', methods=['GET'])
def customer_workouts():
    if not checkSession() or session['user']['role'] != 'customer':
        return redirect('/login')

    from workout import workout
    o = workout()
    workouts = o.get_all_workouts()
    return render_template('workouts/customer_list.html', workouts=workouts)


@app.route('/workouts/start/<int:workoutid>', methods=['POST'])
def start_workout(workoutid):
    if not checkSession() or session['user']['role'] != 'customer':
        return redirect('/login')

    from activitylog import activitylog
    a = activitylog()
    a.start_workout(session['user']['uid'], workoutid)

        # Redirect or display activityid for ending
    msg = f"Workout started! Your session ID is {activityid}. Don't forget to end it."
    return render_template('ok_dialog.html', msg=msg)


@app.route('/workouts/end/<int:activityid>', methods=['POST'])
def end_workout(activityid):
    if not checkSession() or session['user']['role'] != 'customer':
        return redirect('/login')

    from workout import activitylog
    a = activitylog()
    if a.end_workout(activityid):
        return render_template('ok_dialog.html', msg="Workout ended and logged!")
    else:
        return render_template('error_dialog.html', msg="Workout session not found.")
    
###################               plans:
############################################################################
#Admin Managing Plans
@app.route('/plans/manage', methods=['GET', 'POST'])
def manage_plans():
    if not checkSession() or session['user']['role'] != 'admin':
        return redirect('/login')

    from plan import plan
    o = plan()
    action = request.args.get('action')
    pkval = request.args.get('pkval')

    if action == 'delete' and pkval:
        o.delete_plan(pkval)
        return render_template('ok_dialog.html', msg="Plan deleted.")

    if action == 'insert' and request.method == 'POST':
        o.add_plan(request.form.get('planname'))
        return render_template('ok_dialog.html', msg="Plan added.")

    if action == 'update' and pkval and request.method == 'POST':
        o.update_plan(pkval, request.form.get('planname'))
        return render_template('ok_dialog.html', msg="Plan updated.")

    if pkval is None:
        plans = o.get_all_plans()
        return render_template('plans/list.html', plans=plans)

    if pkval == 'new':
        return render_template('plans/add.html')

    else:
        plan_data = o.get_plan_by_id(pkval)
        if plan_data:
            return render_template('plans/manage.html', plan=plan_data)
        else:
            return render_template('plans/manage.html', plan=None)
        
#Customer Viewing and Starting/Completing Plans
@app.route('/plans', methods=['GET'])
def customer_plans():
    if not checkSession() or session['user']['role'] != 'customer':
        return redirect('/login')

    from plan import plan
    o = plan()
    plans = o.get_all_plans()
    return render_template('plans/customer_list.html', plans=plans)

@app.route('/plans/start/<int:planid>', methods=['POST'])
def start_plan(planid):
    if not checkSession() or session['user']['role'] != 'customer':
        return redirect('/login')

    from plan import plan
    o = plan()
    if o.start_plan(planid):
        return render_template('ok_dialog.html', msg="Plan started successfully!")
    else:
        return render_template('error_dialog.html', msg="Cannot start this plan.")

@app.route('/plans/complete/<int:planid>', methods=['POST'])
def complete_plan(planid):
    if not checkSession() or session['user']['role'] != 'customer':
        return redirect('/login')

    from plan import plan
    o = plan()
    if o.complete_plan(planid):
        return render_template('ok_dialog.html', msg="Plan completed successfully!")
    else:
        return render_template('error_dialog.html', msg="Cannot complete this plan.")



if __name__ == '__main__':
   app.run(host='127.0.0.1',debug=True)   