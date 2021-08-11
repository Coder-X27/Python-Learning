from pitho import app
from pitho.libraries.XJData import XJData
class Users(XJData):
	#fillable=['name','email','password']
	#table=users
	def __init__(self):
		#super(Users, self).__init__(self.__class__.__name__,self.fillable);
		#super(Users, self).__init__(self.table,self.fillable);
		super(Users, self).__init__(self.__class__.__name__);
		super(Users, self).set_relation('user_id');