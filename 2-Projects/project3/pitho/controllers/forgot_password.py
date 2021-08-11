from pitho.autoload import *

@app.route('/forgot_password')
def forgot_pwd():
	base = configuration('base_theme')
	return render_template(base+'/forgot_password.html')

@app.route("/forgot_password_submit", methods = ["GET","POST"])
def forgot_pwd_submit():
	if request.method != "POST":
		return redirect('/')
	data = request.form
	return "yes"