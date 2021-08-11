"""import pymysql
import pymysql.cursors
import glob,os
def conn_db():
    conn = pymysql.connect(host='localhost', user='root', passwd='dots@909',db='dbchat',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
    return conn
	
conn =conn_db()"""
import pymysql
from pymysql import cursors
from flask import _app_ctx_stack, current_app,Flask

class MySQL(object):

	def __init__(self, app=None):
		self.app = app
		if app is not None:
			self.init_app(app)

	def init_app(self, app):
		if hasattr(app, 'teardown_appcontext'):
			app.teardown_appcontext(self.teardown)

	@property
	def connect(self):
		kwargs = {}
		kwargs['host']='localhost'
		kwargs['user']='root'
		#kwargs['passwd']='dots@909'
		kwargs['passwd']=''
		kwargs['db']='flaskdemo'
		kwargs['cursorclass']=pymysql.cursors.DictCursor
		""" current_app.config['MYSQL_HOST']:
            kwargs['host'] = current_app.config['MYSQL_HOST']

        if current_app.config['MYSQL_USER']:
            kwargs['user'] = current_app.config['MYSQL_USER']

        if current_app.config['MYSQL_PASSWORD']:
            kwargs['passwd'] = current_app.config['MYSQL_PASSWORD']

        if current_app.config['MYSQL_DB']:
            kwargs['db'] = current_app.config['MYSQL_DB']

        if current_app.config['MYSQL_PORT']:
            kwargs['port'] = current_app.config['MYSQL_PORT']

        if current_app.config['MYSQL_UNIX_SOCKET']:
            kwargs['unix_socket'] = current_app.config['MYSQL_UNIX_SOCKET']

        if current_app.config['MYSQL_CONNECT_TIMEOUT']:
            kwargs['connect_timeout'] = \
                current_app.config['MYSQL_CONNECT_TIMEOUT']

        if current_app.config['MYSQL_READ_DEFAULT_FILE']:
            kwargs['read_default_file'] = \
                current_app.config['MYSQL_READ_DEFAULT_FILE']

        if current_app.config['MYSQL_USE_UNICODE']:
            kwargs['use_unicode'] = current_app.config['MYSQL_USE_UNICODE']

        if current_app.config['MYSQL_CHARSET']:
            kwargs['charset'] = current_app.config['MYSQL_CHARSET']

        if current_app.config['MYSQL_SQL_MODE']:
            kwargs['sql_mode'] = current_app.config['MYSQL_SQL_MODE']

        if current_app.config['MYSQL_CURSORCLASS']:
            kwargs['cursorclass'] = getattr(cursors, current_app.config['MYSQL_CURSORCLASS'])"""

		return pymysql.connect(**kwargs)

	@property
	def connection(self):
		"""Attempts to connect to the MySQL server.

        :return: Bound MySQL connection object if successful or ``None`` if
            unsuccessful.
        """

		ctx = _app_ctx_stack.top
		if ctx is not None:
			if not hasattr(ctx, 'mysql_db'):
				ctx.mysql_db = self.connect
			return ctx.mysql_db

	def teardown(self, exception):
		ctx = _app_ctx_stack.top
		if hasattr(ctx, 'mysql_db'):
			ctx.mysql_db.close()

def conn_db():
	app = Flask(__name__)
	mysql = MySQL(app)
	return mysql;
conn = conn_db()