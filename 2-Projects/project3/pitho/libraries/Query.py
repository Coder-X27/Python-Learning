from pitho.Config import conn
class Query(object):
	def query(self,SQLQuery,tuple=(),id=0):
		try:
			db=conn.connection.cursor()
			sql=SQLQuery
			db.execute(sql,tuple)
			conn.connection.commit()
			db.close()
			if id==0:
				db=conn.connection.cursor()
				db.execute("SELECT last_insert_id() as id")
				last_id = db.fetchone()
				db.close()
				return str(last_id['id'])
			else:
				return id	
		except:
			return None		
	"""def update(self,SQLQuery,tuple=(),id=0):
		db=conn.connection.cursor()
		sql=SQLQuery
		db.execute(sql,tuple)
		conn.connection.commit()
		db.close()
		return str(id)"""
	def select(self,SQLQuery,tuple=()):
		try:
			db=conn.connection.cursor()
			sql=SQLQuery
			db.execute(sql,tuple)
			data=db.fetchall()
			db.close()
			return data
		except:
			return None
	def delete(self,SQLQuery,tuple=(),id=0):
		try:
			db=conn.connection.cursor()
			sql=SQLQuery
			db.execute(sql,tuple)
			conn.connection.commit()
			db.close()
			return str(id)
		except:
			return None
	def select_row(self,SQLQuery,tuple=()):
		try:
			db=conn.connection.cursor()
			sql=SQLQuery
			db.execute(sql,tuple)
			data=db.fetchone()
			db.close()
			return data	
		except:
			return None