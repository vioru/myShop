from flask_app import app 
from flask_app.controllers import  users_controller , products_controller , shops_controller
from flask import flash

if __name__=="__main__":
    app.run(debug=True)