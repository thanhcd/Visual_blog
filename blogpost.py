from flask import Flask, request, redirect, url_for, render_template, flash, session
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin
import time


app = Flask(__name__)
class User(UserMixin):
    def __init__(self, username, password):
        self.username = username
        self.password = password

users = {'user': User('user', 'password')}


def post(mysql):
    if not session.get('logged_in'):
        return redirect(url_for('login_page'))
    
    acc_id = session.get('AccID')  # Lấy AccID từ phiên làm việc
    print(acc_id)
    
    if request.method == "POST":
        details = request.form
        content = details["content"]
        image = request.files["image"]
        image.save(f'static/assets/img/uploads/{image.filename}')
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO blog(AccID, Content, Image) VALUES (%s, %s, %s)", (acc_id, content, image.filename))
        mysql.connection.commit()
        cur.close()
        return "Đăng bài thành công"
    return "đăng không thành công "


def show_post_details(mysql):
    acc_id = session.get('AccID') 
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM blog WHERE AccID = %s", (acc_id,))
    rows = cur.fetchall()  # Fetch all rows
    cur.close() 

    # Create an empty list to store post data
    posts = []

    # Loop through fetched rows and populate 'posts' list
    for row in rows:
        blogid = row[0]
        accid = row[1]
        content = row[2]  
        image = row[3]  
        image_path = url_for('static', filename=f'assets/img/uploads/{image}')
        post = {
            'content': content,
            'image': image_path,
            'accid': accid,
            'blogid' : blogid
        }
        posts.append(post)
        
    print(posts)

    # Return the populated 'posts' list for template rendering
    # return render_template('OnePage/inner-page.html', posts=posts)
    return posts
       
def del_post(mysql):
  # Check if user is logged in, redirect to login if not
  if not session.get('logged_in'):
    return redirect(url_for('login_page'))

  # Extract blog ID and account ID from the form data
  blog_id = request.form.get('blogid')
  account_id = request.form.get('accid')

  try:
    # Connect to the database
    with mysql.connection.cursor() as cur:

      print(f"Deleting blog with ID: {blog_id} and account ID: {account_id}")  # Log for debugging

      # Execute the query with the actual blog and account IDs
      cur.execute("DELETE FROM blog WHERE blogid = %s AND accid = %s", (blog_id, account_id))  # Use tuple for parameters

      mysql.connection.commit()

      # Success message if deletion is successful
      return "xóa post thành công"

  except mysql.connection.Error as err:
    # Handle database errors gracefully
    print(f"Error deleting blog post: {err}")
    return "Xóa thất bại. Vui lòng thử lại"  # Or your desired error message



#hàm sửa
def update_post(mysql):
    if not session.get('logged_in'):
        return redirect(url_for('login_page'))

    try:
        blog_id = request.form.get('blogid')
          # Use request.files for image uploads
        image = request.files.get('image')
        content = request.form.get('content')
        account_id = session.get('AccID')

        if image:
            image.save(f'static/assets/img/uploads/{image.filename}')

        with mysql.connection.cursor() as cursor:

            # Update query (image first to potentially handle larger data earlier)
            update_query = "UPDATE blog SET image = %s, content = %s WHERE blogid = %s AND accid = %s"
            cursor.execute(update_query, (image.filename, content, blog_id, account_id))

            mysql.connection.commit()

            # Success message
            return "Cập nhật Post thành công"

    except mysql.connection.Error as err:
        print(f"Error updating blog post: {err}")
        return "Cập nhật không thành công. Vui lòng thử lại hoặc liên hệ quản trị viên."  # More informative message
    


