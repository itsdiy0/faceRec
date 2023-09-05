# @app.route('/login',methods=('POST','GET'))
# def login():
#     if request.method =='POST':
#         username = request.form['userName']
#         password = request.form['passWord']
#         if not username:
#             flash('Username is required !')
#         elif not password:
#             flash('Password is required !')
#         else:
#             if username=="kafle.nirmal" and password=="1234":
#                 session['username'] = username
#                 return redirect(url_for('home'))
#             else:
#                 flash('Username and Password not matching !')
#     return render_template('login.html')

# @app.route('/')
# def home():
#     # if 'username' in session:
#     #     return render_template('home.html')
#     # else:
#     #     flash('You need to login in order to use !')
#     #     return redirect(url_for('login'))
#     return render_template('home.html')

# @app.route('/help')
# def help():
#     return render_template('help.html')

# @app.route('/logout')
# def logout():
#     session.pop('username', None)
#     return redirect(url_for('login'))