from flask import Flask, render_template, redirect, url_for, request, session, flash
from models import db, Product, User, Cart, CartItem, ProductSpecification
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from auth import auth
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Đường dẫn thư mục lưu ảnh
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../instance/data.sqlite'
app.config['SECRET_KEY'] = 'secretkey'

db.init_app(app)

# Cấu hình Flask-Login
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app.register_blueprint(auth)

# Tài khoản người dùng
@app.route('/account')
@login_required
def account():
    return render_template('account.html')

# Trang chủ - Giới thiệu về trang web
@app.route('/')
def home():
    return render_template('index.html')

# Trang sản phẩm
@app.route('/products')
def products():
    page = request.args.get('page', 1, type=int)
    per_page = 8  # Số sản phẩm trên mỗi trang

    # Lấy sản phẩm cho trang hiện tại
    products = Product.query.paginate(page=page, per_page=per_page)

    # Kiểm tra xem có trang tiếp theo hay không
    has_next_page = products.has_next

    return render_template(
        'products.html',
        products=products.items,
        page=page,
        has_next_page=has_next_page
    )    

# Xem thông tin chi tiết của sản phẩm
@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    specifications = ProductSpecification.query.filter_by(productID=product.productID).all()  # Lấy thông số kỹ thuật
    return render_template('product_detail.html', product=product, specifications=specifications)

# Thêm sản phẩm vào giỏ hàng
@app.route('/add_to_cart/<int:product_id>')
@login_required
def add_to_cart(product_id):
    cart = Cart.query.filter_by(userID=current_user.userID).first()
    if not cart:
        cart = Cart(userID=current_user.userID)
        db.session.add(cart)
        db.session.commit()

    cart_item = CartItem.query.filter_by(cartID=cart.id, productID=product_id).first()
    if cart_item:
        cart_item.quantity += 1
    else:
        new_item = CartItem(cartID=cart.id, productID=product_id, quantity=1)
        db.session.add(new_item)

    db.session.commit()
    flash("Product added to cart!")
    return redirect(url_for('products'))

# Hiển thị giỏ hàng
@app.route('/cart')
@login_required
def cart():
    cart = Cart.query.filter_by(userID=current_user.userID).first()
    items = CartItem.query.filter_by(cartID=cart.id).all() if cart else []
    total = sum(item.product.price * item.quantity for item in items)
    return render_template('cart.html', items=items, total=total)

# Xóa sản phẩm khỏi giỏ hàng
@app.route('/remove_from_cart/<int:item_id>')
@login_required
def remove_from_cart(item_id):
    cart_item = CartItem.query.get(item_id)
    if cart_item and cart_item.cart.userID == current_user.userID:
        db.session.delete(cart_item)
        db.session.commit()
        flash("Item removed from cart!")
    return redirect(url_for('cart'))

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    page = request.args.get('page', 1, type=int)
    products = Product.query.filter(
        (Product.name.ilike(f'%{query}%')) |
        (Product.brand.ilike(f'%{query}%')) |
        (Product.category.ilike(f'%{query}%'))
    ).paginate(page=page, per_page=8)
    has_next_page = products.has_next

    return render_template(
        'products.html',
        products=products.items,
        page=page,
        has_next_page=has_next_page,
        query=query
    )

# Trang đặt hàng
@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    cart = Cart.query.filter_by(userID=current_user.userID).first()
    items = CartItem.query.filter_by(cartID=cart.id).all() if cart else []
    total = sum(item.product.price * item.quantity for item in items)

    if request.method == 'POST':
        selected_item_ids = request.form.getlist('selected_items')
        full_name = request.form.get('full_name')
        phone = request.form.get('phone')
        address = request.form.get('address')

        for item_id in selected_item_ids:
            cart_item = CartItem.query.get(item_id)
            if cart_item and cart_item.cart.userID == current_user.userID:
                db.session.delete(cart_item)

        db.session.commit()
        flash("Đặt hàng thành công!")
        return redirect(url_for('order_success'))

    return render_template('checkout.html', items=items, total=total)

# Trang thành công sau khi đặt hàng
@app.route('/order_success')
@login_required
def order_success():
    return render_template('order_success.html')


@app.route('/upload_image/<int:product_id>', methods=['POST'])
def upload_image(product_id):
    product = Product.query.get_or_404(product_id)
    image_file = request.files['image']

    if image_file:
        # Đảm bảo tên file an toàn
        filename = secure_filename(image_file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        # Lưu ảnh vào thư mục static/uploads
        image_file.save(file_path)

        # Cập nhật đường dẫn ảnh trong cơ sở dữ liệu
        product.image = f"uploads/{filename}"  # Chỉ lưu phần đường dẫn con
        db.session.commit()

        flash("Ảnh sản phẩm đã được cập nhật!")
        return redirect(url_for('product_detail', product_id=product_id))
    else:
        flash("Không có ảnh nào được tải lên.")
        return redirect(url_for('product_detail', product_id=product_id))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
