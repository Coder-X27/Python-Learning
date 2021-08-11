from pitho.autoload import *

@app.route('/signup')
def signup():
	base = configuration('base_theme')
	return render_template(base+'/signup.html')

@app.route('/signup_submit', methods = ['GET', 'POST'])
def signup_submit():
	if request.method != "POST":
		return redirect ("/")
	data = request.form
	user = Users()
	user.where("email","=", data.get('email'))
	dataobj = user.find()
	print(user.last_query())
	user.clear()
	if dataobj  is not None :
		flash("email already exist")
		return redirect('/signup')
	user.save(data,"yes")
	user.clear()
	flash("successfully created account")
	return redirect ('/')
	return "yes"