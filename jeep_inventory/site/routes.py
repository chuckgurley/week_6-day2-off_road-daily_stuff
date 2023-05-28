from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from jeep_inventory.forms import JeepForm
from jeep_inventory.models import Jeep, db
from jeep_inventory.helpers import random_joke_generator

site = Blueprint('site', __name__, template_folder='site_templates')



@site.route('/')
def home():
    print("It's Magic time!")
    return render_template('index.html')

@site.route('/profile', methods = ['GET','POST'])
@login_required 
def profile():
    # random_joke_generator()
    my_jeep = JeepForm()

    try:
        if request.method == "POST" and my_jeep.validate_on_submit():
            name = my_jeep.name.data
            description = my_jeep.description.data
            price = my_jeep.price.data
            tire_quality = my_jeep.tire_quality.data
            drive_time = my_jeep.drive_time.data
            max_speed = my_jeep.max_speed.data
            height = my_jeep.height.data
            weight = my_jeep.weight.data
            cost_of_production = my_jeep.cost_of_production.data
            series = my_jeep.series.data
            if my_jeep.dad_joke.data:
                random_joke = my_jeep.dad_joke.data
            else:
                random_joke = random_joke_generator()          
            user_token = current_user.token

            jeep = Jeep(name, description, price, tire_quality, drive_time, max_speed, height, weight, cost_of_production, series, random_joke, user_token)

            db.session.add(jeep)
            db.session.commit()

            return redirect(url_for('site.profile'))
    except:
        raise Exception("Jeep not created, please check your form and try again!")
    
    current_user_token = current_user.token

    jeeps = Jeep.query.filter_by(user_token=current_user_token)

    
    return render_template('profile.html', form=my_jeep, jeeps = jeeps )


