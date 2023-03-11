from flask import render_template, redirect, session, request, flash 
from flask_app import app
from flask_app.models.users import User
from flask_app.models.products import Product
from flask_app.models.shops import Shop
from flask_app.controllers import  users_controller , products_controller , shops_controller, proposals_controller


@app.route('/new/product')
def newproduct():

    
    if 'shop_id' not in session: 
        return redirect('/')
    
    formulario = {
        "id": session['shop_id']
    }

    shop = Shop.get_by_id(formulario)

    return render_template('new_product.html', shop = shop)


@app.route ('/create/product', methods=['POST'])
def create_product():
    if 'shop_id' not in session: 
        return redirect('/')

    if not Product.valid_product(request.form):

        return redirect('/new/product')

    Product.save_product(request.form)
    return redirect('/myshop')





@app.route('/edit/product/<int:id>') 
def edit_task(id):
    if 'shop_id' not in session: 
        return redirect('/')
    
    formulario = {
        "id": session['shop_id']
    }

    shop = Shop.get_by_id(formulario) 

    formulario_producto = { "id": id }
    
    product = Product.get_by_id(formulario_producto)

    return render_template('edit_product.html', shop = shop , product = product)




@app.route('/edit/product', methods=['POST'])
def update_product():
    if 'shop_id' not in session: 
        return redirect('/')

    
    if not Product.valid_product(request.form):
        return redirect('/edit/product/'+ request.form['product_id'])

    Product.update_product(request.form)

    return redirect('/myshop')


@app.route('/delete/product/<int:id>')
def delete_product(id):
    if 'shop_id' not in session: 
        return redirect('/')
    
    formulario = {"id": id}
    Product.delete_product(formulario)

    return redirect('/myshop')






