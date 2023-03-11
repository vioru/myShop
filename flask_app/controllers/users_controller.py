from flask import render_template, redirect, session, request, flash 
from flask_app import app
from flask_app.models.users import User
from flask_app.models.products import Product
from flask_app.models.shops import Shop
from flask_app.models.favs import Favorite
from flask_app.models.proposals import Proposal
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

from werkzeug.utils import secure_filename
import os 
import uuid


ALLOWED_EXTENSIONS = set(["png","jpg","jpeg"])



def allowed_file(file):
    file = file.split('.')
    if file[1] in ALLOWED_EXTENSIONS:
        return True
    else:
        return False

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register/user', methods=['POST'])
def registeruser():

    if not User.valida_usuario(request.form):
        return redirect('/form/user')

    pwd = bcrypt.generate_password_hash(request.form['password']) 
    formulario = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "direction": request.form['direction'],
        "password": pwd
    }

    id = User.save(formulario) 

    session['usuario_id'] = id

    return redirect('/')

@app.route('/form/user')
def formuser():
    return render_template('form_user.html')



@app.route('/login', methods=['POST'])
def login():

    user = User.get_by_email(request.form)
    shop = []
    

    if not user  : 
        shop = Shop.get_by_email_shop(request.form)
        if not shop  : 
            flash("E-mail no encontrado", 'login')
            return redirect('/')
    
    if user :
        if not bcrypt.check_password_hash(user.password, request.form['password']):
            flash("Password incorrecto", 'login')
            return redirect('/')
        else:
            session['usuario_id'] = user.id
    elif  shop:
        if not bcrypt.check_password_hash(shop.password, request.form['password']):
            flash("Password incorrecto", 'login')
            return redirect('/')
        else:
            session['shop_id'] = shop.id

    if 'usuario_id'  in session:
        return redirect('/mywalluser/0')
    elif 'shop_id' in session:
        return redirect('/myshop')


@app.route('/mywalluser/<int:category>')
def dashboarduser(category):
    shops = []

    if 'usuario_id' not in session:
        return redirect('/')

    formulario = {
        "id": session['usuario_id']
    }

    user = User.get_by_id(formulario)
    
    #products = Product.get_all_products()
    
    if category == 0:
        shops = Shop.show_shops()

    else:
        form_category = {
            "category" : category
        }
        shops = Shop.show_shops_category(form_category)


    return render_template('user_wall.html', user=user, shops = shops)



@app.route('/myacount')
def useracount():
    if 'usuario_id' not in session:
        return redirect('/')

    formulario = {
        "id": session['usuario_id']
    }

    user = User.get_by_id(formulario)
    favs = Product.favorites_by_user(formulario)
    proposals = Proposal.view_proposal_userid(formulario)

    return render_template('user_acount.html', user = user, favs = favs, proposals = proposals)

    


@app.route('/upload/logo/user', methods=['POST'])
def uploaduserLogo():

    
    file = request.files["uploadprofile"]
    
    extension = secure_filename(file.filename).split('.')
    extension=extension[len(extension)-1]
    filename = str(uuid.uuid4()) + '.' + extension

    if file and allowed_file(filename):

        formulario = {
                "profile_img" : filename ,
                "id": session['usuario_id']
            }

        file.save(os.path.join(app.config["UPLOAD_FOLDER"],filename))
        User.update_logouser(formulario)
            
    else:
        flash("Archivo no permitido", 'uploadprofile')
    
    return redirect('/mywalluser/0')
    

@app.route('/cart/construction/<int:shop_id>/<int:product_id>')
def cart(shop_id,product_id):
    shop_id = str(shop_id)
    product_id = str(product_id)

    formulario = {
        "id": session['usuario_id']
    }

    user = User.get_by_id(formulario)
#
    return render_template ('construction.html', shop_id = shop_id, product_id = product_id,user = user)




@app.route('/favorite/product/<int:product_id>/<int:shop_id>')
def favorites(product_id, shop_id):
    
    if 'usuario_id' not in session:
        return redirect('/')
    
    formulario ={
        'product_id' : product_id,
        'user_id': session['usuario_id'],
        
    }

    if Favorite.consult_fav(formulario) :
        Favorite.delete_fav(formulario)
        return redirect ('/shop/'+ str(shop_id) +'#card'+ str(product_id))
    else:
        Favorite.save_fav(formulario)
        return redirect ('/shop/'+ str(shop_id) +'#card'+ str(product_id))
    

@app.route('/new/proposal/<int:shop_id>')
def new_proposal_user(shop_id):

    if 'usuario_id' not in session:
        return redirect('/')
    
    formulario = {
        "id": shop_id
        
    }
        
    formulario_user = {
        "id": session['usuario_id']
    }

    user = User.get_by_id(formulario_user) 
    shop = Shop.get_by_id(formulario) 

    return render_template('new_proposal.html', user = user, shop = shop)


@app.route ('/create/proposal', methods=['POST'])
def create_proposal():
    print(request.form)
    if 'usuario_id' not in session: 
        return redirect('/')

    if not Proposal.valid_proposal(request.form):
        return redirect('/new/proposal/'+str(request.form['shop_id']))

    Proposal.save_proposal(request.form)
    return redirect('/shop/'+ str(request.form['shop_id']))



@app.route('/logout')
def logout():
    session.clear() 
    return redirect('/')


@app.route('/deleteuser/<int:id>')
def deleteuser(id):
    if 'usuario_id' not in session: 
        return redirect('/')
    
    formulario = {"id": id}
    User.delete_user(formulario)

    return redirect('/')