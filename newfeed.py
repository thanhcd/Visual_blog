from flask import Flask, request, redirect, url_for, render_template, flash, session
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin
import time


app = Flask(__name__)
class User(UserMixin):
    def __init__(self, username, password):
        self.username = username
        self.password = password

users = {'user': User('user', 'password')}


def get_feed(mysql):
    cur = mysql.connection.cursor()
    cur.execute("SELECT blog.blogid, blog.accid, blog.content, blog.image, user.username FROM blog INNER JOIN user ON blog.accid = user.accid")
    rows = cur.fetchall()
    cur.close()

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
            'blogid' : blogid,
            'username' : row[4]
        }
        posts.append(post)
        
    # print(posts)

    # Return the populated 'posts' list for template rendering
    # return render_template('OnePage/blog.html', posts=posts)
    return posts




#hàm bình luận
def comment(mysql):
    if not session.get('logged_in'):
        return redirect(url_for('login_page'))
    
    acc_id = session.get('AccID')  # Lấy AccID từ phiên làm việc
    # print(acc_id)   
    blog_id = request.form.get('blogid')
    # account_id = request.form.get('accid')
    if request.method == "POST":
        details = request.form
        comment = details['comment']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO comment(AccID, Comment) VALUES (%s, %s)", (acc_id, comment))
        cur.execute("SELECT LAST_INSERT_ID()")
        comment_id = cur.fetchone()[0]

        cur.execute("INSERT INTO blog_comment(BlogID, CommentID) VALUES (%s, %s)",(blog_id, comment_id))
        mysql.connection.commit()
        cur.close()
        return "Bình luận của bạn đã được lưu"
    return "Bình luận như đb"


#hàm show comment
def show_comment_details(mysql):
    cur = mysql.connection.cursor()
    cur.execute("SELECT comment.comment, blog_comment.blogID, user.Username, comment.commentID, comment.accID FROM comment INNER JOIN blog_comment ON comment.CommentID = blog_comment.CommentID INNER JOIN user ON user.AccID = comment.AccID")
    comments = cur.fetchall()
    cur.close()

    comment_details = []

    # Loop through fetched rows and populate 'comment_details' list
    for comment in comments:
        comment_text = comment[0]
        blogid = comment[1]
        username = comment[2]
        commentid = comment[3]
        accid = comment[4]
        
        comment_detail = {
            'comment' : comment_text,
            'blogid' : blogid,
            'username' : username,
            'commentid' : commentid,
            'accid' : accid
            
        }
        comment_details.append(comment_detail)
        
    # return render_template('Onepage/blog.html', posts = posts, comment=comment_details)
    return comment_details



#hàm xóa bình luận
def del_comment_details(mysql):
    if not session.get('logged_in'):
        return redirect(url_for('login_page'))
    
    blogid = request.form.get('blogid')
    commentid = request.form.get('commentid')
    # print(blogid)
    # print(commentid)
    try:
        with mysql.connection.cursor() as cur:
            # Xóa bình luận từ bảng comment
            cur.execute("DELETE FROM comment WHERE CommentID = %s", (commentid,))
            # Xóa cặp (blogid, commentid) từ bảng blog_comment
            cur.execute("DELETE FROM blog_comment WHERE BlogID = %s AND CommentID = %s", (blogid, commentid))
            
            mysql.connection.commit()
            return "Bình luận đã được xóa thành công"
    except Exception:
        return "Đã xảy ra lỗi khi xóa bình luận"


#hàm sửa bình luận 
def update_comment(mysql):
    if not session.get('logged_in'):
        return redirect(url_for('login_page'))
   
    commentid = request.form.get('commentid')
    # print(commentid)
    comment = request.form.get('comment')
    # print(comment)


    if request.method == "POST":
        cur = mysql.connection.cursor()
        cur.execute("UPDATE comment SET Comment = %s WHERE CommentID = %s", (comment, commentid))
        mysql.connection.commit()
        cur.close()
        return "Sửa bình luận thành công"
    return "éo sửa được, sai ở đâu rồi"



#hàm like blog
def like(mysql):
    if not session.get('logged_in'):
        return redirect(url_for('login_page'))
    
    acc_id = session.get('AccID')
    blogid = request.form.get('blogid')

    if request.method == "POST":
        # likes = request.form['like']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO blog_like_test(BlogID, AccID, Likes) VALUES (%s, %s, %s)", (blogid, acc_id, True))
        # cur.execute("SELECT LAST_INSERT_ID()")
        # likes_id = cur.fetchone()[0]

        # cur.execute("INSERT INTO blog_likes(BlogID, LikeID) VALUES (%s, %s)", (blogid, likes_id))
        mysql.connection.commit()
        cur.close()
        return "like thành công"


#hàm like set false
def del_like(mysql):
    if not session.get('logged_in'):
        return redirect(url_for('login_page'))
    
    acc_id = session.get('AccID')
    blogid = request.form.get('blogid')
    # likeid = request.form.get('likeid')
    try:
        with mysql.connection.cursor() as cur:
            # Xóa bình luận từ bảng comment
            cur.execute("DELETE FROM blog_like_test WHERE BlogID = %s AND AccID = %s", (blogid, acc_id))
            # Xóa cặp (blogid, commentid) từ bảng blog_comment
            # cur.execute("DELETE FROM blog_comment WHERE BlogID = %s AND CommentID = %s", (blogid, commentid))
            
            mysql.connection.commit()
            cur.close()
            return "oke ddaasy con giai"
    except Exception:
        return "false thất bại"
    

def count_like(mysql):
    blogid = request.form.get('blogid')
    # print(blogid)
    cur = mysql.connection.cursor()
    cur.execute("SELECT COUNT(BlogID) FROM blog_like_test WHERE BlogID = %s", (blogid,))
    row = cur.fetchone()
    count = row[0]
    mysql.connection.commit()
    cur.close()
    print(count)
    return count

# #hàm like set True
# def use_like(mysql):
#     if not session.get('logged_in'):
#         return redirect(url_for('login_page'))
    
#     acc_id = session.get('AccID')
#     blogid = request.form.get('blogid')
#     likeid = request.form.get('likeid')
#     try:
#         with mysql.connection.cursor() as cur:
#             # Xóa bình luận từ bảng comment
#             cur.execute("UPDATE likes INNER JOIN blog_likes ON likes.id = blog_likes.LikeID SET likes.Likes = 1 WHERE likes.LikeID = %s AND likes.AccID = %s AND blog_like.BlogID = %s", (likeid, acc_id, blogid))
#             # Xóa cặp (blogid, commentid) từ bảng blog_comment
#             # cur.execute("DELETE FROM blog_comment WHERE BlogID = %s AND CommentID = %s", (blogid, commentid))
            
#             mysql.connection.commit()
#             cur.close()
#             return "true like"
#     except Exception:
#         return "true like thất bại"




#hàm kiểm tra like
def show_like(mysql):
    cur = mysql.connection.cursor()
    cur.execute("SELECT BlogID, AccID, Likes FROM blog_like_test")
    likes = cur.fetchall()
    cur.close()

    like_details = []

    for like in likes:
        blogid = like[0]
        accid = like[1]
        like = like[2]

        blog_like_aa = {
            'blogid' : blogid,
            'accid' : accid,
            'like' : like
            
        }
        like_details.append(blog_like_aa)
        
        # print(like_details)    
    return like_details
        

    # if like: 
    #     like_details = True
    # return like_details

# def process_like(mysql):
#     if not session.get('logged_in'):
#         return redirect(url_for('login_page'))
    
#     acc_id = session.get('AccID')
#     blogid = request.form.get('blogid')
#     print(acc_id)
#     print(blogid)

#     if request.method == "POST":
#         cur = mysql.connection.cursor()
#         cur.execute("INSERT INTO likes(AccID, Likes) VALUES (%s, %s)", (acc_id, True))
#         cur.execute("SELECT LAST_INSERT_ID()")
#         likes_id = cur.fetchone()[0]

#         cur.execute("INSERT INTO blog_likes(BlogID, LikeID) VALUES (%s, %s)", (blogid, likes_id))
#         mysql.connection.commit()
#         cur.close()
#         like_status = "Thích thành công"
#     else:
#         cur = mysql.connection.cursor()
#         cur.execute("SELECT blog_likes.BlogID, likes.LikeID, likes.AcID, likes.likes FROM blog_likes INNER JOIN likes ON blog_likes.LikeID = likes.LikeID WHERE blog_likes.BlogID = %s AND likes.AccID = %s", (blogid, acc_id))
#         like = cur.fetchall()
#         cur.close()

#         like_details = []

#         for row in like:
#             likes = row[0]
#             accid = row[1]
#             blogid = row[2]
#             likeid = row[3]

#             like_de = {
#                 'like': likes,
#                 'accid': accid,
#                 'blogid': blogid,
#                 'likeid': likeid
#             }

#             like_details.append(like_de)

#         print(like_details)
#         like_status = like_details

#     return like_status