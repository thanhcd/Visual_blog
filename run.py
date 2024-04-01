from flask import Flask, render_template, request, url_for, redirect,flash, session
# from auth import login_manager, login, logout
from auth import register as auth_register
from auth import login as auth_login
from auth import auth_logout as auth_logout
from edit_user import edit_user as edit
from edit_user import show_user_details as show
from blogpost import post, show_post_details as show_post, del_post as delete, update_post as sua_post
from newfeed import get_feed, comment, show_comment_details, del_comment_details, update_comment, like, show_like, del_like, count_like

from flask_mysqldb import MySQL
from routes import *

import base64

app = Flask(__name__)
# app.config['MONGO_URI'] = 'mongodb://localhost:27017/blogdb'
# mongo = PyMongo(app)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = ""
app.config['MYSQL_DB'] = "blogdb"
app.config['UPLOADED_PHOTOS_DEST'] = 'uploads'

mysql = MySQL(app)

#hàm load trang đầu tiên
@app.route('/')
def index():
    if 'logged_in' in session and session['logged_in']:
        acc_id = session.get('AccID')
        return render_template('Onepage/index.html', data = acc_id)
    return render_template('Onepage/index.html')
    
    
# Hàm kiểm tra login
@app.route('/check_login')
def check_login():
    if 'logged_in' in session and session['logged_in']:
        acc_id = session.get('AccID')  # Lấy giá trị AccID từ phiên làm việc
        return render_template('Onepage/inner-page.html', data=acc_id)
    else:
        return redirect(url_for('login'))

## chức năng tạo tài khoản và đăng nhập
@app.route('/register', methods=["POST", "GET"])
def register():
    return auth_register(mysql)

@app.route('/login', methods=["POST", "GET"])
def login():
   return auth_login(mysql)


## update thông tin user
@app.route('/update', methods =["POST", "GET"])
def update():
    return edit(mysql)

#hàm logout
@app.route('/logout')
def logout():
    return auth_logout()

#hàm đăng bài
@app.route('/blog-post', methods = ["POST", "GET"])
def blog():
    return post(mysql)

#hàm xóa bài
@app.route('/del_blog', methods = ["POST", "GET"])
def del_post():
    return delete(mysql)


#hàm edit blog
@app.route('/update_blog', methods = ["POST", "GET"])
def update_post():
    return sua_post(mysql)


# @app.route('/blog')
# def show_feed():
#     return feed(mysql)

#hàm hiển thị all blog ở trang newfeed, comment
@app.route('/newfeed', methods = ["POST", "GET"])   
def newfeed():
    posts = get_feed(mysql)
    comment_details = show_comment_details(mysql)
    
    like_details = show_like(mysql)
    
    return render_template('Onepage/blog.html',  posts=posts, comment_details=comment_details, like_details = like_details)

@app.route('/like_blog', methods=["POST", "GET"])
def likes():
    return like(mysql)

@app.route('/del_like', methods =["POST", "GET"])
def dis_like():
    return del_like(mysql)


# @app.route('/true_like', methods =["POST", "GET"])
# def true_like():
#     return use_like(mysql)

###Trả về 2 trang
@app.route('/register_page')
def register_page():
    return render_template('Onepage/register.html')

@app.route('/index')
def return_index():
    return render_template('Onepage/index.html')

#hàm load trang login
@app.route('/login_page', methods =["POST", "GET"])
def login_page():
    return render_template('Onepage/login.html')

#hàm comment
@app.route('/comment', methods = ["GET","POST"])
def comment_blog():
    return comment(mysql)

#hàm hiển thị comment
@app.route('/get_comment')
def show_comment():
    return show_comment_details(mysql)

#hàm xóa comment
@app.route('/del_comment', methods = ["GET", "POST"])
def delete_comment():
    return del_comment_details(mysql)

#hàm update comment
@app.route('/update_comment', methods = ["GET", "POST"])
def updated_comment():
    return update_comment(mysql)

#Show thông tin user
@app.route('/user_page')
def user_page():
    return show(mysql)

@app.route('/inner')
def inner_page():
    show_blog = show_post(mysql)
    comment_details = show_comment_details(mysql)
    return render_template('Onepage/inner-page.html',  posts=show_blog, comment_details=comment_details)


# Route cho API


# Run ứng dụng Flask
if __name__ == '__main__':
    app.run(debug = True)
    

# Ví dụ giờ mình code cái mới, đây là các để up code mới lên
# Đầu tiên gõ git add .
# Sau đó là git commit -m "ghi cc gì vô đây cũng đc, chủ yếu là ghi nội dung mình đã code"
# Rồi git push origin master
# OK chưa, code thay đổi ở file nào thì nó sẽ hiện chữ M ở file đó, với cái dấu màu xanh ở đầu dòng
#BlogID     AccID	isLike
#1          1       true
#1          2       true



