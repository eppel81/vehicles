from my_app import app, db
from flask import jsonify, request, redirect, url_for, session, flash, render_template
from my_app.location.models import Users, Objects, Providers, Settings, Location, Object2user
from datetime import datetime, timedelta

from my_app.location.forms import RegistrationForm, LoginForm, ManageUser, ChangePass, UpdateSettings
from flask import g
from flask.ext.login import current_user, login_user, logout_user, login_required
from my_app import login_manager
from werkzeug.security import generate_password_hash



# ==== for Flask-Login
@login_manager.user_loader
def load_user(nid):
    return Users.query.get(int(nid))


@app.before_request
def get_current_user():
    g.user = current_user


# ===== Registration =====
@app.route('/register', methods=['GET', 'POST'])
def register():
    if session.get('login'):
        flash('Your are already logged in.', 'info')
        return redirect(url_for('index'))

    form = RegistrationForm(request.form)

    if request.method == 'POST' and form.validate():
        login = request.form.get('login')
        password = request.form.get('password')
        name = request.form.get('name')
        existing_username = Users.query.filter_by(login=login).first()
        if existing_username:
            flash('This login has been already taken. Try another one.', 'warning')
            return render_template('register.html', form=form)
        user = Users(login, password, name)
        db.session.add(user)
        db.session.commit()
        flash('You are now registered. Please login.', 'success')
        return redirect(url_for('login'))

    if form.errors:
        flash(form.errors, 'danger')

    return render_template('register.html', form=form)


# ===== LOGIN =====
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('You are already logged in.')
        return redirect(url_for('index'))

    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        login = request.form.get('login')
        password = request.form.get('password')
        existing_user = Users.query.filter_by(login=login).first()

        if not (existing_user and existing_user.check_password(password)):
            flash('Invalid username or password. Please try again.', 'danger')
            return render_template('login.html', form=form)

        login_user(existing_user)
        # for update field 'lastlogin'
        # existing_user.lastlogin = datetime.now()
        # db.session.add(existing_user)
        # db.session.commit()

        flash('You have successfully logged in.', 'success')
        return redirect(url_for('index'))

    if form.errors:
        flash(form.errors, 'danger')

    return render_template('login.html', form=form)


# ===== LOGOUT =====
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have successfully logged out.', 'success')
    return redirect(url_for('index'))
# ==================


@app.route('/')
@login_required
def index():

    # define amount of vehicles from DB table 'settings'
    vehicles_amount = Settings.query.first().max_objects

    user_objects_full_attr = []

    # find vehicles, which have locations coords for last 24 hours
    user_objects = Objects.query.join(Location, Objects.nid == Location.object_id)\
        .filter(Location.ts >= (datetime.utcnow()+timedelta(days=-10)))\
        .join(Object2user, Objects.nid == Object2user.object_id)\
        .join(Users, Object2user.user_id == Users.nid).filter(Users.nid == current_user.nid)\
        .order_by('nid').all()[:vehicles_amount]

    for obj in user_objects:
        # from Object2user
        obj_visi_attr = current_user.vehicles.filter(Object2user.object_id == obj.nid).first()
        user_objects_full_attr.append(
            {
                'id': obj.nid,
                'name': obj.name,
                'visible': obj_visi_attr.visible
            }
        )

    return render_template('home.html', vehicles=user_objects_full_attr)


def is_in_list(obj, objlist):
    """
    Find objects in object list. If find - return true
    """
    for item in objlist:
        if obj.nid == item.nid:
            return True
    return False


# for managing users
@app.route('/manage_users', methods=['GET', 'POST'])
@login_required
def manage_user():
    users = Users.query.order_by('login').all()

    form = ManageUser(request.form)
    form.admin.choices = [(0, 'Not admin'), (1, 'Admin')]

    if request.method == 'POST' and form.validate():
        user_id = request.form.get('user_id')
        user = Users.query.get(int(user_id))
        if user is not None:
            user.name = request.form.get('name')
            user.admin = int(request.form.get('admin'))
            user.locked = request.form.get('locked')

            # user's objects from db
            user_veh_list_from_db = [item.object for item in user.vehicles.all()]

            # # parse new list of vehicles form form's multiselect
            user_veh_list_form = [Objects.query.filter_by(name=item).first()
                                  for item in request.form.getlist('uservehicles')]

            for item in user_veh_list_form:
                # obj = Objects.query.filter_by(name=item).first()
                if not is_in_list(item, user_veh_list_from_db):
                    # add vehicle to user
                    user.add_vehicle(item)

            for item in user_veh_list_from_db:
                if not is_in_list(item, user_veh_list_form):
                    user.del_vehicle(item)

            db.session.add(user)
            db.session.commit()

            flash('User %s is changed' % user.name, 'success')
            form = ManageUser()
            form.admin.choices = [(0, 'Not admin'), (1, 'Admin')]

    return render_template('manage_users.html', users=users, form=form)


@app.route('/get_userdata')
@login_required
def get_userdata():
    login = request.args.get('login', None)
    user = Users.query.filter_by(login=login).first()

    if user:
        vehicles = Objects.query.all()
        all_vehicles = []
        for veh in vehicles:
            all_vehicles.append({'id': veh.nid, 'name': veh.name})


        vehicles = user.vehicles
        user_vehicles = []
        for veh in vehicles:
            user_vehicles.append({'id': veh.object.nid, 'name': veh.object.name})

        return jsonify(name=user.name, admin=user.admin,
                       locked=user.locked, id=user.nid,
                       user_vehicles=user_vehicles, all_vehicles=all_vehicles)
    return jsonify(error='does not exist')


@app.route('/get_users')
@login_required
def get_users():
    users = Users.query.all()
    res = {}
    for user in users:
        res[user.nid] = {
            'name': user.name
        }
    return jsonify(res)


@app.route('/get_user_veh_locations')
@login_required
def get_user_veh_locations():
    """
    Return vehicles locations
    """

    # define amount of points from DB table 'settings'
    points_amount = Settings.query.first().max_points
    vehicles_amount =  Settings.query.first().max_objects


    # find vehicles, which have locations coords for last 24 hours
    user_objects = Objects.query.join(Location, Objects.nid == Location.object_id)\
        .filter(Location.ts >= (datetime.utcnow()+timedelta(days=-10)))\
        .join(Object2user, Objects.nid == Object2user.object_id).filter(Object2user.visible == True)\
        .join(Users, Object2user.user_id == Users.nid).filter(Users.nid == current_user.nid)\
        .order_by('nid').all()[:vehicles_amount]

    # user_vehicles = [item.object for item in current_user.vehicles.filter(Object2user.visible == True)
    #     .join(Objects, Object2user.object_id == Objects.nid).join(Location, Objects.nid == Location.object_id)\
    #     .filter(Location.ts >= (datetime.utcnow()+timedelta(days=-10)))\
    #     .order_by('object_id').all()]

    vehicles = []
    for item in user_objects:
        veh_locations = [dict(ts=str(loc.ts), latitude=str(loc.latitude),
                              longitude=str(loc.longitude), other=loc.other)
                         for loc in item.locations.filter(Location.ts >= (datetime.utcnow()+timedelta(days=-10)))
                             .order_by('ts').all()[:points_amount]]
        vehicles.append({
            'id': item.nid,
            'name': item.name,
            'locations': veh_locations
        })
    return jsonify(vehicles=vehicles)


@app.route('/hide_show/<vehicle>')
@login_required
def hide_show(vehicle):
    obj = Objects.query.get(int(vehicle))
    current_user.hide_show_vehicle(obj)
    db.session.add(current_user)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    """
    Change user's password view
    """
    form = ChangePass(request.form)
    if request.method == 'POST' and form.validate():
        old_password = request.form.get('old_pass')
        new_password = request.form.get('new_pass')
        if current_user.check_password(old_password):
            current_user.change_password(new_password)
            db.session.add(current_user)
            db.session.commit()
            flash('Your password successfully changed', 'success')
            return redirect(url_for('index'))
    return render_template('change_pass.html', form=form)


@app.route('/change_settings', methods=['GET', 'POST'])
def change_settings():
    """
    Change system settings
    """
    set_obj = Settings.query.first()

    form = UpdateSettings(request.form)

    form.name.data = str(set_obj.name)
    form.description.data = str(set_obj.description)
    form.max_objects.data = str(set_obj.max_objects)
    form.max_points.data = str(set_obj.max_points)

    if request.method == 'POST' and form.validate():
        set_obj.name = request.form.get('name')
        set_obj.description = request.form.get('description')
        set_obj.max_objects = request.form.get('max_objects')
        set_obj.max_points = request.form.get('max_points')

        db.session.add(set_obj)
        db.session.commit()
        flash('Settings successfully changed', 'success')
        return redirect('change_settings')

    return render_template('change_settings.html', form=form)


@app.route('/get_report/<vehicle>')
def get_report(vehicle):
    pass