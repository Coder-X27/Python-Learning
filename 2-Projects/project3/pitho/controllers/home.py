from pitho.autoload import *

@app.route('/')
def home():
	if session.get('logged_in') is not None:
		return redirect('/myaccount') 
	base = configuration('base_theme')
	return render_template(base+"/home.html")

@app.route('/login_submit', methods = ['GET','POST'])
def login_submit():
	data = request.form
	user = Users()
	user.where_dict(data)
	#user.where("email", "=", data.get("email"))
	#user.where("password", '=', data.get('password'))
	dataobj = user.find()
	print(user.last_query())
	user.clear()
	if dataobj is None :
		flash("invalid username or password")
		return redirect('/')
	else :
		session['logged_in'] = dataobj
		return redirect('/myaccount')
		return "yes"
