from pitho.autoload import *

@app.route('/about')
def about():
	base = configuration('base_theme')
	return render_template(base+'/about.html')