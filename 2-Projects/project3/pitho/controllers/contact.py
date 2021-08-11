from pitho.autoload import *


@app.route('/contact')
def contact():
	base = configuration('base_theme')
	return render_template(base+'/contact.html')