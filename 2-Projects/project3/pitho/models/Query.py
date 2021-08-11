from pitho.Config import conn

class Query:
	def select(self, sqlquery, tuple=()):
		db = conn.connection.cursor()
		db.execute(sqlquery, tuple)
		data = db.fetchall()
		return data

	def select_row(self, sqlquery, tuple=()):
		db = conn.connection.cursor()
		db.execute(sqlquery, tuple)
		data = db.fetchone()
		return data

	def insert(self, sqlquery, tuple=()):
		db = conn.connection.cursor()
		db.execute(sqlquery, tuple)
		conn.connection.commit()
		return True

	def update(self, sqlquery, tuple=()):
		db = conn.connection.cursor()
		db.execute(sqlquery, tuple)
		conn.connection.commit()
		return True