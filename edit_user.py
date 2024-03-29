from flask import Flask, request, redirect, url_for, render_template, flash, session
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin



app = Flask(__name__)
class User(UserMixin):
    def __init__(self, username, password):
        self.username = username
        self.password = password

users = {'user': User('user', 'password')}


# Sửa thông tin user
def edit_user(mysql):
    if not session.get('logged_in'):
        return redirect(url_for('login_page'))

    acc_id = session.get('AccID')  # Lấy AccID từ phiên làm việc
    print(acc_id)
    if request.method == "POST":
        details = request.form
        fullname = details['fullname']
        date = details['date']
        phone = details['phone']
        cur = mysql.connection.cursor()
        cur.execute("UPDATE user SET Username = %s, Date = %s, Phone = %s WHERE AccID = %s", (fullname, date, phone, acc_id))
        if cur.rowcount > 0:
            print("Cập nhật thành công")
        else:
            print("Không tìm thấy tài khoản để cập nhật")
        mysql.connection.commit()
        cur.close()
        print(acc_id)
        return "Sửa thành công"

    return render_template('Onepage/user.html')


def show_user_details(mysql):
    if not session.get('logged_in'):
        return redirect(url_for('login_page'))
    
    acc_id = session.get('AccID')  # Lấy AccID từ phiên làm việc
    print(acc_id)

    cur = mysql.connection.cursor()
    cur.execute("SELECT username, date, phone FROM user WHERE AccID = %s", (acc_id,))
    user_data = cur.fetchone()
    mysql.connection.commit()
    cur.close()
    print("data",user_data)

    return render_template('Onepage/user.html', fullname=user_data[0], date=user_data[1], phone=user_data[2])
    #Giá trị của trường username., date, phone