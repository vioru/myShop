from flask import render_template, redirect, session, request, flash 
from flask_app import app
from flask_app.models.users import User
from flask_app.models.products import Product
from flask_app.models.shops import Shop
from flask_app.controllers import  users_controller , products_controller , shops_controller
from flask_app.models.favs import Favorite
from flask_app.models.proposals import Proposal
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename
import os 
import uuid

bcrypt = Bcrypt(app)
app.config["UPLOAD_FOLDER"] = "flask_app\\static\\img\\upload"

ALLOWED_EXTENSIONS = set(["png","jpg","jpeg"])



def allowed_file(file):
    file = file.split('.')
    if file[1] in ALLOWED_EXTENSIONS:
        return True
    else:
        return False

@app.route('/form/shop')
def formshop():
    return render_template('form_shop.html')


@app.route('/register/shop', methods=['POST'])
def registershop():
    
    if not Shop.valid_shop(request.form):
        return redirect('/form/shop')
    

    pwd = bcrypt.generate_password_hash(request.form['password']) 
    formulario = {
        "name": request.form['name'],
        "email_shop": request.form['email_shop'],
        "category": request.form['category'],
        "description_shop": request.form['description_shop'],
        "color" : '#6d40f6' ,
        "password": pwd
        
    }
    
    id = Shop.save(formulario) 

    session['shop_id'] = id

    return redirect('/')


@app.route('/myshop')
def dashboardshop():


    if 'shop_id' not in session:
        
        return redirect('/')

    formulario = {
        "id": session['shop_id'],
        "user_id" : 0
        
    }

    shop = Shop.get_by_id(formulario) 
    products = Product.get_products_shops(formulario)
    


    return render_template('myshop.html', shop = shop, products=products)


@app.route('/upload/logo', methods=['POST'])
def uploadShopLogo():

    
    file = request.files["uploadfile"]
    
    extension = secure_filename(file.filename).split('.')
    extension=extension[len(extension)-1]
    filename = str(uuid.uuid4()) + '.' + extension
    



    if file and allowed_file(filename):

        formulario ={
            "logo_img" : filename ,
            "id": session['shop_id']
        }

        file.save(os.path.join(app.config["UPLOAD_FOLDER"],filename))
        Shop.update_logo(formulario)
        
    else:
        flash("Archivo no permitido", 'uploadlogo')
    
    return redirect('/myshop')

@app.route('/shop/<int:id>')
def user_view_shop(id):

    if 'usuario_id' not in session: 
        return redirect('/')
    
    formulario = {
        "id": id,
        "user_id":session['usuario_id']
    }
        
    formulario_user = {
        "id": session['usuario_id'],
        "user_id" : 0
    }



    user = User.get_by_id(formulario_user) 
    shop = Shop.get_by_id(formulario) 
    products = Product.get_products_shops(formulario)
    


    return render_template('shops.html', shop = shop, products=products,user = user)

@app.route('/view/proposals/<int:id_shop>')
def view_proposal_shop(id_shop):

    user ={}

    if 'usuario_id' in session:
        
        formulario = {
        "id": session['usuario_id']
        }

        user = User.get_by_id(formulario)
        
        formulario = {
        "id": id_shop
        
        }

        shop = Shop.get_by_id(formulario) 
        proposals = Proposal.view_proposal_ShopId(formulario)
    else:
        if 'shop_id' not in session:
            
            return redirect('/')

        formulario_shop = {
            "id": id_shop
            
        }
        
        shop = Shop.get_by_id(formulario_shop) 
        proposals = Proposal.view_proposal_ShopId(formulario_shop)
        


    return render_template('proposals.html', shop = shop, proposals=proposals, user = user)


@app.route('/deleteshop/<int:id>')
def deleteshop(id):
    if 'shop_id' not in session: 
        return redirect('/')
    
    formulario = {"id": id}
    Shop.delete_shop(formulario)

    return redirect('/')

