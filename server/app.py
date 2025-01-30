#!/usr/bin/env python3

import os
import requests
from experience_study import FateStudy, PriorStudy, PredictStudy
from models import Queen, Hive, Inspection, User, Event, Signup
from config import app, db, api
from datetime import datetime
# from flask_migrate import Migrate
from flask import request, session
from flask_restful import  Resource

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.before_request
def check_if_logged_in():
    if not session.get('user_id') \
    and request.endpoint in ['spongebob']:
    # and request.endpoint in ['hives', 'inspections', 'queens']:
        return {'error': 'Unauthorized'}, 401
    
class ClearSession(Resource):

    def delete(self):
    
        session['user_id'] = None

        return {}, 204

class AccountSignup(Resource):
    def post(self):
        try:
            json = request.get_json()

            # Check if the username already exists in the database
            existing_user = User.query.filter_by(username=json['username']).first()

            # Check if the email already exists in the database
            existing_email = User.query.filter_by(email=json['email']).first()        

            error_dict = {}

            if existing_user:
                error_dict['username'] = 'Username already taken.'

            if existing_email:
                error_dict['email'] = 'Email already registered.'

            if existing_user or existing_email:
                return {'error': error_dict}, 400                

            user = User(
                username=json['username'],
                first_name=json['first_name'],
                last_name=json['last_name'],
                email=json['email'],
                zipcode=json['zipcode']
                )
            
            user.password_hash = json['password']
            db.session.add(user)
            db.session.commit()

            session['user_id'] = user.id

            return user.to_dict(), 201
        except Exception as e:
            db.session.rollback()  # Rollback any changes made in the transaction
            return {'error': f'An error occurred: {str(e)}'}, 500
    

class CheckSession(Resource):

    def get(self):
        
        user_id = session.get('user_id', 0)
        if user_id:
            user = User.query.filter(User.id == user_id).first()
            return user.to_dict(), 200
        
        return {}, 204

class Login(Resource):
    def post(self):
        try:
            json = request.get_json()

            username = json['username']
            user = User.query.filter_by(username=username).first()

            if not user:
                return {'error': 'Invalid username or password'}, 401

            password = json['password']

            if user.authenticate(password):
                session['user_id'] = user.id
                return user.to_dict(), 200

            return {'error': 'Invalid username or password'}, 401
        except Exception as e:
            return {'error': f'An error occurred: {str(e)}'}, 500

class Logout(Resource):
    
    def delete(self):
        session['user_id'] = None
        return {}, 204

class UserById(Resource):

    def get(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return user.to_dict(), 200
    
    def patch(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        
        data = request.get_json()

        for attr in data:
            setattr(user, attr, data.get(attr))

        db.session.commit()
        return user.to_dict(), 200
    
class Hives(Resource):
    def get(self):
        hives = [hive.to_dict() for hive in Hive.query.all()]
        return hives, 200

    def post(self):
        try:
            # Get data from the request
            data = request.get_json()

            # Create new hive
            new_hive = Hive(
                user_id=data['user_id'],  # Link the hive to the user
                date_added=data['date_added'],
                material=data['material'],
                location_lat=data['location_lat'],
                location_long=data['location_long']
            )

            # Add the new hive to the database and commit
            db.session.add(new_hive)
            db.session.commit()

            # Return the created hive as a response
            return new_hive.to_dict(), 201
        except Exception as e:
            db.session.rollback()
            return {'error': f'An error occurred: {str(e)}'}, 500
        
class HivesByUser(Resource):
    def get(self):
        user_id = session['user_id']
        hives = [hive.to_dict() for hive in Hive.query.filter_by(user_id=user_id)]
        return hives, 200
    
class HiveById(Resource):
    def get(self, hive_id):
        hive = Hive.query.get(hive_id)
        if not hive:
            return {'error': 'Hive not found'}, 404
        return hive.to_dict(), 200

    def patch(self, hive_id):
        hive = Hive.query.get(hive_id)
        if not hive:
            return {'error': 'Hive not found'}, 404
        data = request.get_json()

        for attr in data:
            setattr(hive, attr, data.get(attr))

        db.session.commit()
        return hive.to_dict(), 200

    def delete(self, hive_id):
        hive = Hive.query.get(hive_id)
        if not hive:
            return {'error': 'Hive not found'}, 404
        db.session.delete(hive)
        db.session.commit()
        return {}, 204

class Inspections(Resource):
    def post(self):
        try:
            # Get data from the request
            data = request.get_json()

            # Create new inspection
            new_inspection = Inspection(
                hive_id=data['hive_id'],  # Link the inspection to a hive
                date_checked=data['date_checked'],
                temp=data.get('temp'),
                activity_surrounding_hive=data.get('activity_surrounding_hive'),
                super_count=data.get('super_count'),
                hive_body_count=data.get('hive_body_count'),
                egg_count=data.get('egg_count'),
                larvae_count=data.get('larvae_count'),
                capped_brood=data.get('capped_brood'),
                twisted_larvae=data.get('twisted_larvae'),
                pests_surrounding=data.get('pests_surrounding'),
                stability_in_hive=data.get('stability_in_hive'),
                feeding=data.get('feeding'),
                treatment=data.get('treatment'),
                stores=data.get('stores'),
                fate=data.get('fate'),
                local_bloom=data.get('local_bloom'),
                weather_conditions=data.get('weather_conditions'),
                humidity=data.get('humidity'),
                chalkbrood_presence=data.get('chalkbrood_presence'),
                varroa_mites=data.get('varroa_mites')
            )

            # Add the new inspection to the database and commit
            db.session.add(new_inspection)
            db.session.commit()

            # Return the created inspection as a response
            return new_inspection.to_dict(), 201
        except Exception as e:
            db.session.rollback()
            return {'error': f'An error occurred: {str(e)}'}, 500

class InspectionById(Resource):
    def patch(self, inspection_id):
        inspection = Inspection.query.get(inspection_id)
        if not inspection:
            return {'error': 'Inspection not found'}, 404
        data = request.get_json()

        for attr in data:
            setattr(inspection, attr, data.get(attr))

        db.session.commit()
        return inspection.to_dict(), 200

    def delete(self, inspection_id):
        inspection = Inspection.query.get(inspection_id)
        if not inspection:
            return {'error': 'Inspection not found'}, 404
        db.session.delete(inspection)
        db.session.commit()
        return {}, 204

class Queens(Resource):
    def post(self):
        try:
            # Get data from the request
            data = request.get_json()

            # Create new queen
            new_queen = Queen(
                hive_id=data['hive_id'],  # Link the queen to a hive
                status=data['status'],
                origin=data['origin'],
                species=data['species'],
                date_introduced=data['date_introduced'],
                replacement_cause=data.get('replacement_cause')  # Optional field
            )

            # Add the new queen to the database and commit
            db.session.add(new_queen)
            db.session.commit()

            # Return the created queen as a response
            return new_queen.to_dict(), 201
        except Exception as e:
            db.session.rollback()
            return {'error': f'An error occurred: {str(e)}'}, 500

class QueenById(Resource):
    def patch(self, queen_id):
        queen = Queen.query.get(queen_id)
        if not queen:
            return {'error': 'Queen not found'}, 404
        data = request.get_json()

        for attr in data:
            setattr(queen, attr, data.get(attr))

        db.session.commit()
        return queen.to_dict(), 200

    def delete(self, queen_id):
        queen = Queen.query.get(queen_id)
        if not queen:
            return {'error': 'Queen not found'}, 404
        db.session.delete(queen)
        db.session.commit()
        return {}, 204
    
class Events(Resource):
    def get(self):
        events = [event.to_dict() for event in Event.query.all()]
        return events, 200

    def post(self):
        try:
            # Get data from the request
            data = request.get_json()

            # Create new hive
            new_event = Event(
                user_id=data['user_id'],  # Link the hive to the user
                title=data['title'],
                event_date=data['event_date'],
                descr=data['descr'],
                zipcode=data['zipcode']
            )

            # Add the new hive to the database and commit
            db.session.add(new_event)
            db.session.commit()

            # Return the created hive as a response
            return new_event.to_dict(), 201
        except Exception as e:
            db.session.rollback()
            return {'error': f'An error occurred: {str(e)}'}, 500
    
class EventById(Resource):
    def get(self, event_id):
        event = Event.query.get(event_id)
        if not event:
            return {'error': 'Hive not found'}, 404
        return event.to_dict(), 200

    def patch(self, event_id):
        event = Event.query.get(event_id)
        if not event:
            return {'error': 'Event not found'}, 404
        data = request.get_json()

        for attr in data:
            setattr(event, attr, data.get(attr))

        db.session.commit()
        return event.to_dict(), 200

    def delete(self, event_id):
        event = Event.query.get(event_id)
        if not event:
            return {'error': 'Event not found'}, 404
        db.session.delete(event)
        db.session.commit()
        return {}, 204
    
class Signups(Resource):

    def post(self):
        try:
            # Get data from the request
            data = request.get_json()

            # Create new hive
            new_signup = Signup(
                user_id=data['user_id'],  # Link the hive to the user
                event_id=data['event_id']
            )

            # Add the new hive to the database and commit
            db.session.add(new_signup)
            db.session.commit()

            # Return the created hive as a response
            return new_signup.to_dict(), 201
        except Exception as e:
            db.session.rollback()
            return {'error': f'An error occurred: {str(e)}'}, 500
    
class SignupById(Resource):

    def delete(self, signup_id):
        signup = Signup.query.get(signup_id)
        if not signup:
            return {'error': 'Signup not found'}, 404
        db.session.delete(signup)
        db.session.commit()
        return {}, 204

class GetNearbyZipcodes(Resource):

    def get(self):
        print('got response!')
        API_KEY = os.getenv("ZIPCODE_API_KEY")

        zip_code = request.args.get("zip")
        radius = request.args.get("radius", 5)

        print(zip_code)

        if not zip_code:
            return {'error': 'ZIP code is required'}, 400

        url = f'https://www.zipcodeapi.com/rest/{API_KEY}/radius.json/{zip_code}/{radius}/mile'
        print(url)

        response = requests.get(url)

        if response.status_code == 200:
            return response.json()
        else:
            return {'error': 'Failed to fetch ZIP codes'}, 500
    
api.add_resource(ClearSession, '/clear', endpoint='clear')
api.add_resource(AccountSignup, '/account_signup', endpoint='account_signup')
api.add_resource(CheckSession, '/check_session')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(UserById, '/users/<int:user_id>')
api.add_resource(Hives, '/hives', endpoint='hives')
api.add_resource(HivesByUser, '/user_hives', endpoint='user_hives')
api.add_resource(HiveById, '/hives/<int:hive_id>')
api.add_resource(Inspections, '/inspections', endpoint='inspections')
api.add_resource(InspectionById, '/inspections/<int:inspection_id>')
api.add_resource(Queens, '/queens', endpoint='queens')
api.add_resource(QueenById, '/queens/<int:queen_id>')
api.add_resource(FateStudy, '/fate_study', endpoint='fate_study')
api.add_resource(PriorStudy, '/prior_study', endpoint='prior_study')
api.add_resource(PredictStudy, '/predict_study', endpoint='predict_study')
api.add_resource(Events, '/events', endpoint='events')
api.add_resource(EventById, '/events/<int:event_id>')
api.add_resource(Signups, '/signups', endpoint='signups')
api.add_resource(SignupById, '/signups/<int:signup_id>')
api.add_resource(GetNearbyZipcodes, '/zipcodes')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
