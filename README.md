# firebase_emulation_citibike
The project was designed to emulate the Firebase Realtime Database, leveraging Flask, WebSockets, and MongoDB. The core of this system is a RESTful API, tailored for JSON data storage and retrieval within a MongoDB database. Complementary to this, a command-line interface and web application was developed to aid in database queries and updates and was developed, underscoring the capabilities of real-time data synchronization. 

## Dataset
Citi bike station information source(https://www.kaggle.com/datasets/fatihb/citibike-sampled-data-2013-2017)
The original dataset includes 18 columns. We extracted 5 of them: station id, street name, capacity, available bikes, and disabled bikes. The intuition of our product is a bike station search website. Users can search the station by its attributes to know how many available bikes are there. Users can also help to update the station information by changing, adding, and deleting features, which corresponds to the curl PUT/PATCH, POST, and DELETE commands. 

## How to use
1. python app.py. The temporary webpage address will be shown with messsage in forms of 
    * Running on http://127.0.0.1:5000 
2. Copy the address and enter it in a browser. The webpage will show up
![alt text](http://url/to/img.png)
3. Open a new terminal window to run a command-line interface commands. Sample commands below


## Sample command-line interface commands
- Show all: 

    curl -X GET 'http://127.0.0.1:5000/users.json'
- Filter by capacity, last 5: 

    curl -X GET 'http://127.0.0.1:5000/users.json?orderBy="capacity"&limitToLast=5'
- Search by address: 
 
    curl -X GET 'http://127.0.0.1:5000/users.json?orderBy="street_name"&equalTo="Picnic%20Point"'
- Add a new station:

    curl -X POST 'http://127.0.0.1:5000/users.json' -d '{"street_name": "1337 W 36th", "capacity": 20, "num_bikes_available": 5, "num_bikes_disabled": 5}'
- Modify attribute(s):

    curl -X PUT 'http://127.0.0.1:5000/users/6004/capacity.json' -d '30'

    curl -X PATCH 'http://127.0.0.1:5000/users/6004.json' -d '{"capacity": 40, "num_bikes_available": 10}'
- Delete attribute and station: 
    - attribute deletion:
    
        curl -X DELETE 'http://127.0.0.1:5000/users/6004/capacity.json'


    - station deletion:
        
        curl -X DELETE 'http://127.0.0.1:5000/users/6004.json'



        
        
        




