from flask import Flask, request, render_template, g
from flask_restful import Resource, Api
from flask import jsonify
import load
import json


app = Flask(__name__, template_folder='./')
app.config['JSON_SORT_KEYS'] = False
api = Api(app)

with app.app_context():
    users = load.get_documents()

@app.route('/' )
def display():
    return render_template('bike.html')

@app.route('/infoTable' )
def display_info():
    return render_template('info.html')

@app.route('/add')
def display_add():
    return render_template('add.html')

@app.route('/update')
def display_update():
    return render_template('update.html')

@app.route('/delete')
def display_delete():
    return render_template('delete.html')

users = load.get_documents()

class UserResource(Resource):
    def get(self, user_id=None, attribute=None):
        if user_id is None:
            orderBy = request.args.get('orderBy', None)
            limitToLast = request.args.get('limitToLast', None)
            limitToFirst = request.args.get('limitToFirst', None)
            equalTo = request.args.get('equalTo', None)
            startAt = request.args.get('startAt', None)
            endAt = request.args.get('endAt', None)

            stringified_users = {int(k): v for k, v in users.items()}

            if orderBy:
                orderBy = orderBy.strip('"')
                if orderBy == '$key':
                    ordered_users = sorted(stringified_users.items(), key=lambda x: x[0])
                    orderBy = 'station_id_int'
                elif orderBy == '$value':
                    ordered_users = sorted(stringified_users.items(), key=lambda x: x[1].get('num_bikes_available'))
                    orderBy = 'num_bikes_available'
                else: 
                    #import ipdb; ipdb.set_trace()
                    attributes = list(stringified_users.values())[0].keys()
                    if orderBy not in attributes:
                        return {"error": "Attribute does not exist"}, 400
                    #import ipdb; ipdb.set_trace()
                    ordered_users = sorted(stringified_users.items(), key=lambda x: (str(x[1].get(orderBy, '')) if orderBy=='street_name' else int(x[1].get(orderBy, 0))))
                    
                stringified_users = dict(ordered_users)
                
                
                if equalTo:
                    #import ipdb; ipdb.set_trace()
                    equalTo = equalTo.strip('"')
                    if orderBy != 'street_name': equalTo = int(equalTo) #convert equalTo input to int since default inputs are all string type
                    filtered_users = {k: v for k, v in stringified_users.items() if v.get(orderBy) == equalTo}
                    
                    stringified_users = filtered_users
                
                if startAt:
                    try:
                        startAt = float(startAt)
                    except ValueError:
                        try:
                            orderBy = float(orderBy)
                        except ValueError:
                                return {"error": "Invalid comparison dtype"}, 400
                    filtered_users = {k: v for k, v in stringified_users.items() if float(v.get(orderBy, 0)) >= float(startAt)}
                    stringified_users = filtered_users
                if endAt:
                    try:
                        endAt = float(endAt)
                    except ValueError:
                        return {"error": "Invalid comparison dtype"}, 400
                    #import ipdb; ipdb.set_trace()
                    filtered_users = {k: v for k, v in stringified_users.items() if float(v.get(orderBy, 0)) <= float(endAt)}
                    stringified_users = filtered_users
                
                if limitToFirst and limitToLast:
                    return {"error": "limitToLast and limitToFirst both exist"}, 400
                
                if limitToFirst:
                    try:
                        limitToFirst = int(limitToFirst)
                    except ValueError:
                        return {"error": "Invalid limitToFirst value"}, 400
                    limited_users = dict(list(stringified_users.items())[:limitToFirst])
                    #import ipdb; ipdb.set_trace()
                    stringified_users = limited_users

                if limitToLast:
                    try:
                        limitToLast = int(limitToLast)
                    except ValueError:
                        return {"error": "Invalid limitToLast value"}, 400
                    
                    limited_users = dict(list(stringified_users.items())[-limitToLast:])
                    stringified_users = limited_users

            #import ipdb; ipdb.set_trace()
            return jsonify(stringified_users)
        
        else: #user_id is given
            if user_id not in users:
                return {"error": "Station not found"}, 404
            if attribute is not None:
                if attribute not in users[user_id]:
                    return {"error": f"Attribute '{attribute}' not found"}, 404
                return jsonify(users[user_id])
            return jsonify(users[user_id])
        
  
    def put(self, user_id=None, attribute=None):
        #import ipdb; ipdb.set_trace()
        if user_id == None:
            return {"error": "Need to specify user_id"}, 400 #Or it will potentially erase or overwrite the entire database
        else:
            if attribute: # with specified attribute, input should be value not json
                if attribute != 'station_id_int':
                    return {"error": "Cannot define the station_id value"}, 400
                value = request.get_data(as_text=True)
                if value[0] == '{':
                    return {"error": "Invalid input value"}, 400
                if user_id not in users: 
                    users[user_id] = {}
                #value = request.get_data()
                users[user_id]['station_id_int'] = user_id
                users[user_id][attribute] = value
                
            else: # No attribute, input_data should be json
                try:
                    user_data = json.loads(request.get_data().decode("utf-8"))
                except json.JSONDecodeError:
                    return {"error": 'Invalid JSON data'}, 400
                
                users[user_id] = {} #Need to initiate new user node
                users[user_id]['station_id_int'] = user_id
                for k, v in user_data.items():
                    if k == 'station_id_int': continue
                    #import ipdb; ipdb.set_trace()
                    if isinstance(v, dict): # v should not be json(dict)
                        return {"error": "Invalid input value"}, 400
                    users[user_id][k] = v

            load.update_documents(users)    
            return jsonify(users[user_id])

    def post(self):
        user_id = 0 if users.keys() is None else max(users.keys()) + 1
        try:
            user_data = json.loads(request.get_data().decode("utf-8"))
        except json.JSONDecodeError:
            return {"error": 'Invalid JSON data'}, 400
        
        users[user_id] = {} #Need to initiate new user node
        users[user_id]['station_id_int'] = user_id
        for k, v in user_data.items():
            if k == 'station_id_int': continue
            if isinstance(v, dict): # v should not be json(dict)
                return {"error": "Invalid input value"}, 400
            users[user_id][k] = v

        load.update_documents(users) 
        return jsonify(users[user_id])
        
    def patch(self, user_id=None):
        if user_id == None: # Not specified ID, input will be json containing specified ID, not attribute:value
                            # in order to maintain the database structure: ID: {attibute: value}
            res = [] # To store potential multiple station info updates
           # import ipdb; ipdb.set_trace()
            try:
                user_data = json.loads(request.get_data().decode("utf-8"))
            except json.JSONDecodeError:
                return {"error": 'Invalid JSON data'}, 400
            
            #check all key:val's vals are dict
            for _, v in user_data.items():
                if not isinstance(v, dict):
                    return {"error": 'Invalid JSON data'}, 400

            for k, v in user_data.items(): #Potentially, it would be multiple user_id given to update
                k = int(k)
                users[k] = {}
                users[k]['station_id_int'] = k
                for k1, v1 in v.items():
                    if k1 == 'station_id_int': continue
                    users[k][k1] = v1
                res.append(users[k])
            
            load.update_documents(users)
            return jsonify(res)

        else: #With specified ID, input will be json but only contains attribute:value, not key:dict
            try:
                user_data = json.loads(request.get_data().decode("utf-8"))
            except json.JSONDecodeError:
                return {"error": 'Invalid JSON data'}, 400
            for k, v in user_data.items():
               # import ipdb; ipdb.set_trace()
                if k == 'station_id_int': continue
                if isinstance(v, dict): # v should not be json(dict)
                    return {"error": "Invalid input value"}, 400
                users[user_id][k] = v

            load.update_documents(users)
            return jsonify(users[user_id])
                

    def delete(self, user_id, attribute=None):
        if user_id not in users.keys():
            return {"error": 'Station_id not found'}, 400
        if attribute == None:
            del users[user_id]
            load.update_documents(users)
            return {"msg": f"Station {user_id} deleted"}
        else:
            if attribute not in users[user_id]:
                return {"error": f"Attribute '{attribute}' not found"}, 404
            del users[user_id][attribute]
            load.update_documents(users)
            return {"msg": f"Station {user_id} attribute '{attribute}' deleted"}


api.add_resource(UserResource, '/users.json', '/users/<int:user_id>.json', '/users/<int:user_id>/<attribute>.json')

if __name__ == '__main__':
    app.run(debug=True)
    