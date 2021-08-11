from pitho.autoload import *

@app.route('/myaccount')
def myaccount():
	if session.get('logged_in') is None:
		return redirect("/")
	base = configuration('base_theme')
	return render_template(base+'/myaccount.html')

@app.route('/logout')
def logout():
	session.clear()
	return redirect('/')