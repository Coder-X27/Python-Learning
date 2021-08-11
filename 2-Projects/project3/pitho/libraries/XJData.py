from pitho import app
from pitho.libraries.Query import Query
import json
import math
class XJData(Query):
	limit_query = ""
	offset_query=""
	select_query= ""
	where_query= ""
	where_meta_query= ""
	table= ""
	tablePrefix = "fp_"
	completeQuery= ""
	space= ""
	orderby_query= ""
	groupby_query= ""
	having_query= ""
	delete_query= ""
	update_query= ""
	tableField=[]
	cond=0
	gcond=0
	hcond=0
	ocond=0
	meta_where=0
	query = ""
	whereList={}
	dataValue=[]
	relation_key=''
	join_type=''
	dataColumn={}
	set_meta_relation = ""
	def __init__(self,table,fillable=[]):
		self.dataValue=[]
		self.whereList={}
		self.table=table.lower()
		self.query = Query()
		self.setField(fillable)
		self.relation_key=''
		#print(self.tableField)
		self.join_type = ''
		self.completeQuery = "";
		self.where_query = " where ";
		self.where_meta_query = " ";
		self.space = " ";
		self.orderby_query = " order by ";
		self.groupby_query = " group by ";
		self.having_query = " having ";
		self.select_query = " select ";
		self.delete_query = " delete from ";
		self.update_query = " update ";
		self.cond=0
		self.gcond=0
		self.hcond=0
		self.ocond=0
		self.limit_query = ""
		self.offset_query=""
		set_meta_relation=""
		self.dataColumn={}
	def set_relation(self,key):
		self.relation_key=key
	def setField(self,fillable):
		if self.checkTableExists()==True and not fillable :
			self.tableField= self.tabelSchema()
		else:
			self.tableField=fillable
		return True
	def addColumn(self,key,value):
		self.dataColumn[str(key)]= str(value)
		return self
	def setMeta(self,key="no"):
		self.set_meta_relation= str(key)
		return self
	def requestFieldList(self,dataDict):
		dataList=[]
		#if self.dataColumn:
			#for addColmn in self.dataColumn:
				#dataDict[addColmn] = self.dataColumn[addColmn]
		for field in  self.tableField:
			if field in dataDict:
				data = dataDict[field]
				#print(type(data))
				if type(data) is list:
					data = json.dumps(dataDict[field])
					print(data)
				self.dataValue.append(str(data))
				dataList.append(field)
		return dataList	
	def save(self,dataDict={},meta_relation="no"):
		if self.dataColumn:
			for addColmn in self.dataColumn:
				dataDict[addColmn] = self.dataColumn[addColmn]
		requestField=self.requestFieldList(dataDict)
		sql = " insert into " + str(self.tablePrefix) + str(self.table) + "("
		sql += (",").join(requestField)
		sql += ") values ("
		dataList=[]
		keyList=[]
		for field in  requestField:
			keyList.append("%s")
		sql += ",".join(keyList)+")";
		last_id = self.query.query(sql,tuple(self.dataValue))
		#print(sql)
		if (self.set_meta_relation=="yes" or meta_relation=="yes") and self.checkTableExists('meta')==True:
			self.save_meta(dataDict,last_id)
		return last_id;
	def update(self,dataDict={},meta_relation="no"):
		if self.dataColumn:
			for addColmn in self.dataColumn:
				dataDict[addColmn] = self.dataColumn[addColmn]
		table = self.table
		id=0
		if 'id' in dataDict.keys():
			id = dataDict.get("id")
			del dataDict['id']
		requestField=self.requestFieldList(dataDict)
		datasql = "";
		self.update_query += self.tablePrefix +  table + " set ";
		keyList=[]
		for field in  requestField:
			keyList.append(str(field)+"=%s")
		datasql += ",".join(keyList);
		self.update_query += datasql;
		if self.cond > 0 :
			self.update_query += self.where_query;
		else:
			whr = " where " + self.space + table + ".id" + self.space + "=" + self.space + table + ".id"
			self.update_query += whr;
		if self.dataValue:
			last_id = self.query.query(self.update_query,tuple(self.dataValue),id)
		else:
			last_id=id
		self.completeQuery = self.update_query;
		#print(self.completeQuery)
		#print(self.dataValue)
		if (self.set_meta_relation=="yes" or meta_relation=="yes") and self.checkTableExists('meta')==True:
			self.save_meta(dataDict,last_id)
		#last_id=0
		return last_id;
		#return self.completeQuery
	def where(self,field, op, value):
		table = self.tablePrefix +self.table;
		if self.cond == 0:
			self.where_query += " (" + self.space + table + "." + field + self.space + op + self.space + "'"+str(value)+"')";
		else:
			self.where_query += " and (" + self.space + table + "." + field + self.space + op + self.space + "'"+str(value)+"') ";
		#self.dataValue.append(str(value))
		self.cond = self.cond+1;
		self.completeQuery = self.where_query;
		return self;
	def where_Meta(self,dataList=[],op = 'and'):
		where_QueryList=[]
		if self.meta_where!=0 or self.cond!=0:
			self.where_query += " and "
		if dataList:
			for data in dataList:
				table = "meta"+str(self.meta_where);
				compareop = "="
				if 'compare' in data.keys():
					compareop = data['compare']
				if compareop=='like':
					where_QueryList.append(" (" + self.space + table + ".meta_key='" + data['key'] +"' and "+table+".meta_value"+ self.space + compareop + self.space + "'"+str(data['value'])+"')")
				elif compareop=='like%':
					compareop = 'like'
					where_QueryList.append(" (" + self.space + table + ".meta_key='" + data['key'] +"' and "+table+".meta_value"+ self.space + compareop + self.space + "'"+str(data['value'])+"%%')")
				elif compareop=='%like%':
					compareop = 'like'
					where_QueryList.append(" (" + self.space + table + ".meta_key='" + data['key'] +"' and "+table+".meta_value"+ self.space + compareop + self.space + "'%%"+str(data['value'])+"%%')")
				elif compareop=='not like':
					where_QueryList.append(" (" + self.space + table + ".meta_key='" + data['key'] +"' and "+table+".meta_value"+ self.space + compareop + self.space + "'"+str(data['value'])+"')")
				elif compareop=='not like%':
					compareop = 'not like'
					where_QueryList.append(" (" + self.space + table + ".meta_key='" + data['key'] +"' and "+table+".meta_value"+ self.space + compareop + self.space + "'"+str(data['value'])+"%%')")
				elif compareop=='%not like%':
					compareop = 'not like'
					where_QueryList.append(" (" + self.space + table + ".meta_key='" + data['key'] +"' and "+table+".meta_value"+ self.space + compareop + self.space + "'%%"+str(data['value'])+"%%')")
				elif compareop=='in' or compareop=='not in' or compareop=='between' or compareop=='not between':
					where_QueryList.append(" (" + self.space + table + ".meta_key='" + data['key'] +"' and "+table+".meta_value"+ self.space + compareop + self.space + str(data['value'])+")")
				else:
					where_QueryList.append(" (" + self.space + table + ".meta_key='" + data['key'] +"' and "+table+".meta_value"+ self.space + compareop + self.space + "'"+str(data['value'])+"')")
				if op =='and':
					self.meta_where = self.meta_where+1;
		if op=="or":
			self.meta_where = self.meta_where+1;
		self.cond  = self.cond+1
		self.where_query += "("+(" "+str(op)+" ").join(where_QueryList)+")"
		self.completeQuery = self.where_query;
		return self;
	def where_Meta_Or(self,dataList=[],op = 'and'):
		where_QueryList=[]
		if self.meta_where!=0:
			self.where_query += " or "
		if dataList:
			for data in dataList:
				table = "meta"+str(self.meta_where);
				compareop = "="
				if 'compare' in data.keys():
					compareop = data['compare']
				if compareop=='like':
					where_QueryList.append(" (" + self.space + table + ".meta_key='" + data['key'] +"' and "+table+".meta_value"+ self.space + compareop + self.space + "'"+str(data['value'])+"')")
				elif compareop=='like%':
					compareop = 'like'
					where_QueryList.append(" (" + self.space + table + ".meta_key='" + data['key'] +"' and "+table+".meta_value"+ self.space + compareop + self.space + "'"+str(data['value'])+"%%')")
				elif compareop=='%like%':
					compareop = 'like'
					where_QueryList.append(" (" + self.space + table + ".meta_key='" + data['key'] +"' and "+table+".meta_value"+ self.space + compareop + self.space + "'%%"+str(data['value'])+"%%')")
				elif compareop=='not like':
					where_QueryList.append(" (" + self.space + table + ".meta_key='" + data['key'] +"' and "+table+".meta_value"+ self.space + compareop + self.space + "'"+str(data['value'])+"')")
				elif compareop=='not like%':
					compareop = 'not like'
					where_QueryList.append(" (" + self.space + table + ".meta_key='" + data['key'] +"' and "+table+".meta_value"+ self.space + compareop + self.space + "'"+str(data['value'])+"%%')")
				elif compareop=='%not like%':
					compareop = 'not like'
					where_QueryList.append(" (" + self.space + table + ".meta_key='" + data['key'] +"' and "+table+".meta_value"+ self.space + compareop + self.space + "'%%"+str(data['value'])+"%%')")
				elif compareop=='in' or compareop=='not in' or compareop=='between' or compareop=='not between':
					where_QueryList.append(" (" + self.space + table + ".meta_key='" + data['key'] +"' and "+table+".meta_value"+ self.space + compareop + self.space + str(data['value'])+")")
				else:
					where_QueryList.append(" (" + self.space + table + ".meta_key='" + data['key'] +"' and "+table+".meta_value"+ self.space + compareop + self.space + "'"+str(data['value'])+"')")
				if op =='and':
					self.meta_where = self.meta_where+1;
		if op=="or":
			self.meta_where = self.meta_where+1;
		self.cond  = self.cond+1
		self.where_query += "("+(" "+str(op)+" ").join(where_QueryList)+")"
		self.completeQuery = self.where_query;
		return self;
	def where_dict(self,dictList={}):
		self.whereList = dictList
		table = self.tablePrefix +self.table
		newSql = ""
		dataLits=[]
		for data in dictList:
			#self.dataValue.append(str(dictList[data]))
			dataLits.append(str(table+"."+data) + "= '"+str(dictList.get(data))+"'")
		newSql= (" and ").join(dataLits)
		if self.cond == 0:
			self.where_query += "(" + newSql + ")"
		else:
			self.where_query += " and (" + newSql + ")"
	
		self.cond = self.cond+1
		self.completeQuery = self.where_query;
		return self;
	def where_dict_Or(self,dictList={}):
		self.whereList = dictList
		table = self.tablePrefix +self.table
		newSql = ""
		dataLits=[]
		for data in dictList:
			#self.dataValue.append(str(dictList[data]))
			dataLits.append(str(table+"."+data) + "= '"+str(dictList.get(data))+"'")
		newSql= (" or ").join(dataLits)
		if self.cond == 0:
			self.where_query += "(" + newSql + ")"
		else:
			self.where_query += " or (" + newSql + ")"
	
		self.cond = self.cond+1
		self.completeQuery = self.where_query;
		return self;
	def where_dict_Or_And(self,dictList={}):
		self.whereList = dictList
		table = self.tablePrefix +self.table
		newSql = ""
		dataLits=[]
		for data in dictList:
			#self.dataValue.append(str(dictList[data]))
			dataLits.append(str(table+"."+data) + "= '"+str(dictList.get(data))+"'")
		newSql= (" and ").join(dataLits)
		if self.cond == 0:
			self.where_query += "(" + newSql + ")"
		else:
			self.where_query += " or (" + newSql + ")"
	
		self.cond = self.cond+1
		self.completeQuery = self.where_query;
		return self;	
	
	def where_Or(self,field, op,value):
		table = self.tablePrefix + self.table;
		if self.cond == 0:
			self.where_query += " (" + self.space + table + "." + field + self.space + op + self.space + "'"+str(value)+"')";
		else:
			self.where_query += " or ( " + self.space + table + "." + field + self.space + op + self.space + "'"+str(value)+"') ";
		#self.dataValue.append(str(value))
		self.cond = self.cond+1
		self.completeQuery = self.where_query;
		return self;
	def where_In(self,field,dictList):
		table = self.tablePrefix + self.table
		self.whereList = dictList
		
		dataList=[]
		for data in dictList:
			val = str(dictList.get(data))
			if val.isnumeric()==False:
				val = "'"+val+"'"
			dataList.append(val)
		str_data = "("+(",").join(dataList)+")"
		if self.cond == 0:
			self.where_query += " (" + self.space + table + "." + field + " in " + str_data + ")";
		else:
			self.where_query += " and ( " + self.space + table + "." + field + " in " + str_data + ")";
		self.completeQuery = self.where_query;
		self.cond = self.cond+1
		return self;
	def where_Or_In(self,field,dictList):
		table = self.tablePrefix + self.table
		self.whereList = dictList
		
		dataList=[]
		for data in dictList:
			val = str(dictList.get(data))
			if val.isnumeric()==False:
				val = "'"+val+"'"
			dataList.append(val)
		str_data = "("+(",").join(dataList)+")"
		if self.cond == 0:
			self.where_query += " (" + self.space + table + "." + field + " in " + str_data + ")";
		else:
			self.where_query += " or ( " + self.space + table + "." + field + " in " + str_data + ")";
		self.completeQuery = self.where_query;
		self.cond = self.cond+1
		return self;
	def where_Not_In(self,field,dictList):
		table = self.tablePrefix + self.table
		self.whereList = dictList
		
		dataList=[]
		for data in dictList:
			val = str(dictList.get(data))
			if val.isnumeric()==False:
				val = "'"+val+"'"
			dataList.append(val)
		str_data = "("+(",").join(dataList)+")"
		if self.cond == 0:
			self.where_query += " (" + self.space + table + "." + field + " not in " + str_data + ")";
		else:
			self.where_query += " and ( " + self.space + table + "." + field + " not in " + str_data + ")";
		self.completeQuery = self.where_query;
		self.cond = self.cond+1
		return self;
	def where_Or_Not_In(self,field,dictList):
		table = self.tablePrefix + self.table
		self.whereList = dictList
		
		dataList=[]
		for data in dictList:
			val = str(dictList.get(data))
			if val.isnumeric()==False:
				val = "'"+val+"'"
			dataList.append(val)
		str_data = "("+(",").join(dataList)+")"
		if self.cond == 0:
			self.where_query += " (" + self.space + table + "." + field + " not in " + str_data + ")";
		else:
			self.where_query += " or ( " + self.space + table + "." + field + " not in " + str_data + ")";
		self.completeQuery = self.where_query;
		self.cond = self.cond+1
		return self;
	def where_Between(self, field, value1, value2):
		table = self.tablePrefix + self.table
		if self.cond == 0:
			self.where_query += " (" + self.space + table + "." + field + self.space + "between" + self.space + "'" + str(value1) + "'" + self.space + " and " + self.space + "'" + str(value2) + "')";
		else:
			self.where_query += " and (" + self.space + table + "." + field + self.space + "between" + self.space + "'" + str(value1) + "'" + self.space + " and " + self.space + "'" + str(value2) + "')";
	
		self.cond = self.cond+1
		self.completeQuery = self.where_query;
		return self;

	def where_Or_Between(self, field, value1, value2):
		table = self.tablePrefix + self.table
		if self.cond == 0:
			self.where_query += " (" + self.space + table + "." + field + self.space + "between" + self.space + "'" + str(value1) + "'" + self.space + " and " + self.space + "'" + str(value2) + "')";
		else:
			self.where_query += " or (" + self.space + table + "." + field + self.space + "between" + self.space + "'" + str(value1) + "'" + self.space + " and " + self.space + "'" + str(value2) + "')";
	
		self.cond = self.cond+1
		self.completeQuery = self.where_query;
		return self;	
	def where_Not_Between(self, field, value1, value2):
		table = self.tablePrefix + self.table
		if self.cond == 0:
			self.where_query += " (" + self.space + table + "." + field + self.space + " not between" + self.space + "'" + str(value1) + "'" + self.space + " and " + self.space + "'" + str(value2) + "')";
		else:
			self.where_query += " and (" + self.space + table + "." + field + self.space + " not between" + self.space + "'" + str(value1) + "'" + self.space + " and " + self.space + "'" + str(value2) + "')";
	
		self.cond = self.cond+1
		self.completeQuery = self.where_query;
		return self;

	def where_Or_Not_Between(self, field, value1, value2):
		table = self.tablePrefix + self.table
		if self.cond == 0:
			self.where_query += " (" + self.space + table + "." + field + self.space + " not between" + self.space + "'" + str(value1) + "'" + self.space + " and " + self.space + "'" + str(value2) + "')";
		else:
			self.where_query += " or (" + self.space + table + "." + field + self.space + " not between" + self.space + "'" + str(value1) + "'" + self.space + " and " + self.space + "'" + str(value2) + "')";
	
		self.cond = self.cond+1
		self.completeQuery = self.where_query;
		return self;

	def find(self):
		if self.join_type!='':
			return self.Rfind()
		self.select_query += " * from " + self.tablePrefix + self.table;
		if self.cond > 0 :
			self.select_query += self.where_query;
		if self.gcond > 0:
			self.select_query += self.groupby_query;
		if self.hcond > 0:
			self.select_query += self.having_query;
		if self.ocond > 0:
			self.select_query += self.orderby_query;
		if self.limit_query!="" and  self.offset_query!="":
			start = int(self.offset_query)-1
			start = start*int(self.limit_query)
			self.select_query += " limit" + self.space + str(start) + "," + self.limit_query + "";
			#self.select_query += " limit" + self.space + self.offset_query + "," + self.limit_query + "";
		elif self.limit_query!="":
			self.select_query += " limit " + "" + self.limit_query + "";
		self.completeQuery = self.select_query;
		#print(self.completeQuery)
		#print(self.dataValue)
		data = self.query.select_row(self.completeQuery,tuple(self.dataValue))
		return data
	def Rfind(self):
		if self.checkTableExists('meta')==True:
			
			ftable = self.tablePrefix + self.table
			metatable = ftable+"meta"
			self.select_query += " "+ftable+".id from " + self.tablePrefix + self.table;
			alias = 0
			while alias < 	self.meta_where:
				aliameta = "meta"+str(alias)
				self.select_query += self.space+self.join_type+" join "+metatable+" as "+aliameta+" ON "+ftable+".id = "+aliameta+"."+self.relation_key
				alias = alias+1
			if self.cond > 0 :
				self.select_query += self.where_query;
			if self.meta_where > 0 :
				self.select_query += self.where_meta_query;
			if self.gcond > 0:
				self.select_query += self.groupby_query;
			if self.hcond > 0:
				self.select_query += self.having_query;
			if self.ocond > 0:
				self.select_query += self.orderby_query;
			if self.limit_query!="" and  self.offset_query!="":
				start = int(self.offset_query)-1
				start = start*int(self.limit_query)
				self.select_query += " limit" + self.space + str(start) + "," + self.limit_query + "";
				#self.select_query += " limit" + self.space + self.offset_query + "," + self.limit_query + "";
			elif self.limit_query!="":
				self.select_query += " limit " + "" + self.limit_query + "";
			self.completeQuery = self.select_query;
			#print(self.completeQuery)
			#print(self.dataValue)
			data= {}
			data = self.query.select_row(self.completeQuery,tuple(self.dataValue))
			return data
		else:
			return {}
	def RfindAll(self):
		if self.checkTableExists('meta')==True:
			
			ftable = self.tablePrefix + self.table
			metatable = ftable+"meta"
			self.select_query += " "+ftable+".* from " + self.tablePrefix + self.table;
			alias = 0
			while alias < 	self.meta_where:
				aliameta = "meta"+str(alias)
				self.select_query += self.space+self.join_type+" join "+metatable+" as "+aliameta+" ON "+ftable+".id = "+aliameta+"."+self.relation_key
				alias = alias+1
			if self.cond > 0 :
				self.select_query += self.where_query;
			if self.meta_where > 0 :
				self.select_query += self.where_meta_query;
			if self.gcond > 0:
				self.select_query += self.groupby_query;
			if self.hcond > 0:
				self.select_query += self.having_query;
			if self.ocond > 0:
				self.select_query += self.orderby_query;
			if self.limit_query!="" and  self.offset_query!="":
				start = int(self.offset_query)-1
				start = start*int(self.limit_query)
				self.select_query += " limit" + self.space + str(start) + "," + self.limit_query + "";
				#self.select_query += " limit" + self.space + self.offset_query + "," + self.limit_query + "";
			elif self.limit_query!="":
				self.select_query += " limit " + "" + self.limit_query + "";
			self.completeQuery = self.select_query;
			#print(self.completeQuery)
			#print(self.dataValue)
			data= {}
			data = self.query.select(self.completeQuery,tuple(self.dataValue))
			return data
		else:
			return {}
	def RCount(self):
		if self.checkTableExists('meta')==True:
			
			ftable = self.tablePrefix + self.table
			metatable = ftable+"meta"
			self.select_query += " count(*) as cnt from " + self.tablePrefix + self.table;
			alias = 0
			while alias < 	self.meta_where:
				aliameta = "meta"+str(alias)
				self.select_query += self.space+self.join_type+" join "+metatable+" as "+aliameta+" ON "+ftable+".id = "+aliameta+"."+self.relation_key
				alias = alias+1
			if self.cond > 0 :
				self.select_query += self.where_query;
			if self.meta_where > 0 :
				self.select_query += self.where_meta_query;
			if self.gcond > 0:
				self.select_query += self.groupby_query;
			if self.hcond > 0:
				self.select_query += self.having_query;
			if self.ocond > 0:
				self.select_query += self.orderby_query;
			if self.limit_query!="" and  self.offset_query!="":
				start = int(self.offset_query)-1
				start = start*int(self.limit_query)
				self.select_query += " limit" + self.space + str(start) + "," + self.limit_query + "";
				#self.select_query += " limit" + self.space + self.offset_query + "," + self.limit_query + "";
			elif self.limit_query!="":
				self.select_query += " limit " + "" + self.limit_query + "";
			self.completeQuery = self.select_query;
			#print(self.completeQuery)
			#print(self.dataValue)
			data= {}
			data = self.query.select_row(self.completeQuery,tuple(self.dataValue))
			return data
		else:
			return {"cnt":0}
	def count(self):
		if self.join_type!='':
			return self.RCount()
		self.select_query += " count(*) as cnt from " + self.tablePrefix + self.table;
		if self.cond > 0 :
			self.select_query += self.where_query;
		if self.gcond > 0:
			self.select_query += self.groupby_query;
		if self.hcond > 0:
			self.select_query += self.having_query;
		if self.ocond > 0:
			self.select_query += self.orderby_query;
		if self.limit_query!="" and  self.offset_query!="":
			self.select_query += " limit" + self.space + self.offset_query + "," + self.limit_query + "";
		elif self.limit_query!="":
			self.select_query += " limit " + "" + self.limit_query + "";
		self.completeQuery = self.select_query;
		#print(self.completeQuery)
		#print(self.dataValue)
		data = self.query.select_row(self.completeQuery,tuple(self.dataValue))
		return data
	def sum(self,column):
		if self.join_type!='':
			return self.RCount()
		self.select_query += " sum("+column+") as sum from " + self.tablePrefix + self.table;
		if self.cond > 0 :
			self.select_query += self.where_query;
		if self.gcond > 0:
			self.select_query += self.groupby_query;
		if self.hcond > 0:
			self.select_query += self.having_query;
		if self.ocond > 0:
			self.select_query += self.orderby_query;
		if self.limit_query!="" and  self.offset_query!="":
			self.select_query += " limit" + self.space + self.offset_query + "," + self.limit_query + "";
		elif self.limit_query!="":
			self.select_query += " limit " + "" + self.limit_query + "";
		self.completeQuery = self.select_query;
		#print(self.completeQuery)
		#print(self.dataValue)
		data = self.query.select_row(self.completeQuery,tuple(self.dataValue))
		if data['sum'] is None:
			data = {'sum':0}
		return data
	
	def findAll(self):
		if self.join_type!='':
			return self.RfindAll()
		self.select_query += " * from " + self.tablePrefix + self.table;
		if self.cond > 0 :
			self.select_query += self.where_query;
		if self.gcond > 0:
			self.select_query += self.groupby_query;
		if self.hcond > 0:
			self.select_query += self.having_query;
		if self.ocond > 0:
			self.select_query += self.orderby_query;
		if self.limit_query!="" and  self.offset_query!="":
			start = int(self.offset_query)-1
			start = start*int(self.limit_query)
			self.select_query += " limit" + self.space + str(start) + "," + self.limit_query + "";
		elif self.limit_query!="":
			self.select_query += " limit " + "" + self.limit_query + "";
		self.completeQuery = self.select_query;
		print(self.completeQuery)
		#print(self.dataValue)
		data={}
		data = self.query.select(self.completeQuery,tuple(self.dataValue))
		return data
	def total_record(self,per_page=20):
		if self.join_type!='':
			return self.Rtotal_record(per_page)
		self.select_query += " count(*) as cnt from " + self.tablePrefix + self.table;
		if self.cond > 0 :
			self.select_query += self.where_query;
		if self.gcond > 0:
			self.select_query += self.groupby_query;
		if self.hcond > 0:
			self.select_query += self.having_query;
		if self.ocond > 0:
			self.select_query += self.orderby_query;
		self.completeQuery = self.select_query;
		#print(self.completeQuery)
		#print(self.dataValue)
		#data=""
		data = self.query.select_row(self.completeQuery,tuple(self.dataValue))
		page = 1
		if data['cnt']!=0:
			page =  math.ceil(data['cnt']/per_page)
		return {'total':data['cnt'],'pages':page}
	def count_total_record(self,data={},per_page=20):
		page=0
		if 'cnt' not in data.keys():
			data['cnt']=0
		if  data['cnt']!=0:
			page =  math.ceil(data['cnt']/per_page)
		return {'total':data['cnt'],'pages':page}
	def Rtotal_record(self,per_page):
		if self.checkTableExists('meta')==True:
			
			ftable = self.tablePrefix + self.table
			metatable = ftable+"meta"
			self.select_query += " count(*) as cnt from " + self.tablePrefix + self.table;
			alias = 0
			while alias < 	self.meta_where:
				aliameta = "meta"+str(alias)
				self.select_query += self.space+self.join_type+" join "+metatable+" as "+aliameta+" ON "+ftable+".id = "+aliameta+"."+self.relation_key
				alias = alias+1
			if self.cond > 0 :
				self.select_query += self.where_query;
			if self.meta_where > 0 :
				self.select_query += self.where_meta_query;
			if self.gcond > 0:
				self.select_query += self.groupby_query;
			if self.hcond > 0:
				self.select_query += self.having_query;
			if self.ocond > 0:
				self.select_query += self.orderby_query;
			if self.limit_query!="" and  self.offset_query!="":
				start = int(self.offset_query)-1
				start = start*int(self.limit_query)
				self.select_query += " limit" + self.space + str(start) + "," + self.limit_query + "";
				#self.select_query += " limit" + self.space + self.offset_query + "," + self.limit_query + "";
			elif self.limit_query!="":
				self.select_query += " limit " + "" + self.limit_query + "";
			self.completeQuery = self.select_query;
			#print(self.completeQuery)
			#print(self.dataValue)
			#data= {}
			data = self.query.select_row(self.completeQuery,tuple(self.dataValue))
			page = 1
			if data is not None and  data['cnt']!=0:
				page =  math.ceil(data['cnt']/per_page)
				return {'total':data['cnt'],'pages':page}
			return {'total':0,'pages':page}	
			#return data
		else:
			return {'total':0,'pages':0}
	def last_query(self):
		return self.completeQuery
	def checkTableExists(self,data=''):
		table = self.tablePrefix + self.table+str(data);
		result = self.query.select_row("SHOW TABLES LIKE %s",(table))
		if result:
			return True
		return False
	def tabelSchema(self):
		table = self.tablePrefix + self.table;
		columnList=[]
		result = self.query.select("select column_name from information_schema.columns where table_name= %s",(table))
		#print(result);
		for row in result:
			if row['column_name'] not in columnList:
				columnList.append(row['column_name'])
		return columnList
	def save_meta(self,dataList,id):
		table = self.tablePrefix + self.table+"meta";
		columnList= self.get_meta_field(dataList,self.tableField)
		for field in columnList:
			if isinstance(dataList[field], list)==True :
				data = json.dumps(dataList.get(field))
				#print(data)
			else:
				data = str(dataList.get(field))
			data_record = self.query.select_row("select * from "+table+" where "+self.relation_key+"=%s and meta_key = %s",(str(id),str(field)))
			#sql=""
			if data_record is None:
				sql= "insert into "+table+"(meta_value,"+self.relation_key+",meta_key) values(%s, %s, %s)"
				try:
					self.query.query(sql,(data,str(id),str(field)))
				except:
					print(data)
			elif data!=data_record['meta_value']:
				sql = "update "+table+" set meta_value=%s where "+self.relation_key+"=%s and meta_key=%s"
				try:
					self.query.query(sql,(str(data),str(id),str(field)))
				except:
					print(data)
		return True
	def add_meta(self,id,key,value):
		self.save_meta({key:value},id)
		return self
	def update_meta(self,id,key,value):
		self.save_meta({key:value},id)
		return self
	def get_meta_field(self,data,defaultList):
		fieldList=[]
		for key in data:
			if key in defaultList:
				c=''
			else:
				fieldList.append(key)
		return fieldList;
	def limit(self,num):
		self.limit_query=str(num)
		return self
	def offset(self,num):
		self.offset_query=str(num)
		return self
	def orderby(self,field,type="desc"):
		table = self.tablePrefix + self.table;
		if self.ocond == 0:
			self.orderby_query += self.space + table + "." + field + self.space + type;
		else:
			self.orderby_query += "," + self.space + table + "." + field + self.space + type;
		self.ocond = self.ocond+1;
		self.completeQuery = self.orderby_query;
		return self;

	def groupby(self,field):
		table = self.tablePrefix + self.table;
		if self.gcond == 0:
			self.groupby_query += self.space + table + "." + str(field);
		else:
			self.groupby_query += "," + self.space + table + "." + str(field);
		self.gcond = self.gcond+1;
		self.completeQuery = self.groupby_query;
		return self;

	def having(self,field, op, value):
		table = self.tablePrefix + self.table;
		if self.hcond == 0:
			self.having_query += "(" + self.space + table + "." + field + self.space + op + self.space + "'" + str(value) + "')";
		else:
			self.having_query += " and( " + self.space + table + "." + field + self.space + op + self.space + "'" + str(value) + "')";
		self.hcond = self.hcond+1;
		self.completeQuery = self.having_query;
		return self

	def having_Or(self,field, op, value):
		table = self.tablePrefix + self.table;
		if self.hcond == 0:
			self.having_query += "(" + self.space + table + "." + field + self.space + op + self.space + "'" + str(value) + "')";
		else:
			self.having_query += " or( " + self.space + table + "." + field + self.space + op + self.space + "'" + str(value) + "')";
		self.hcond = self.hcond+1;
		self.completeQuery = self.having_query;
		return self;

	def having_Not(self,field, op, value):
		table = self.tablePrefix + self.table;
		if self.hcond == 0:
			self.having_query += "( not " + self.space + table + "." + field + self.space + op + self.space + "'" + str(value) + "')";
		else:
			self.having_query += " and not ( " + self.space + table + "." + field + self.space + op + self.space + "'" + str(value) + "')";
		self.hcond = self.hcond+1;
		self.completeQuery = self.having_query;
		return self;

	def having_Or_Not(self,field,op, value):
		table = self.tablePrefix + self.table;
		if self.hcond == 0:
			self.having_query += "( not " + self.space + table + "." + field + self.space + op + self.space + "'" + str(value) + "')";
		else:
			self.having_query += " or not ( " + self.space + table + "." + field + self.space + op + self.space + "'" + str(value) + "')";

		self.hcond = self.hcond+1;
		self.completeQuery = self.having_query;
		return self;


	def like(self,field, value,type=""):
		value=self.like_value(value,type)
		table = self.tablePrefix + self.table;
		if self.cond == 0:
			self.where_query += " (" + self.space + table + "." + field + self.space + " like " + self.space + "'" + value + "')";
		else:
			self.where_query += " and ( " + self.space + table + "." + field + self.space + " like " + self.space + "'" + value + "') ";
	
		self.cond = self.cond+1
		self.completeQuery = self.where_query;
		return self;

	def like_Or(self,field, value,type=""):
		value=self.like_value(value,type)
		table = self.tablePrefix + self.table;
		if self.cond == 0:
			self.where_query += " (" + self.space + table + "." + field + self.space + " like " + self.space + "'" + value + "')";
		else:
			self.where_query += " or ( " + self.space + table + "." + field + self.space + " like " + self.space + "'" + value + "') ";
	
		self.cond = self.cond+1
		self.completeQuery = self.where_query;
		return self;

	def like_Not(self,field, value,type=""):
		value=self.like_value(value,type)
		table = self.tablePrefix + self.table;
		if self.cond == 0:
			self.where_query += " (" + self.space + table + "." + field + self.space + " not like " + self.space + "'" + value + "')";
		else:
			self.where_query += " or ( " + self.space + table + "." + field + self.space + " not like " + self.space + "'" + value + "') ";
	
		self.cond = self.cond+1
		self.completeQuery = self.where_query;
		return self;

	def like_Or_Not(self,field, value,type=""):
		value=self.like_value(value,type)
		table = self.tablePrefix + self.table;
		if self.cond == 0:
			self.where_query += " (" + self.space + table + "." + field + self.space + " not like " + self.space + "'" + value + "')";
		else:
			self.where_query += " or ( " + self.space + table + "." + field + self.space + " not like " + self.space + "'" + value + "') ";
	
		self.cond = self.cond+1
		self.completeQuery = self.where_query;
		return self;
	def like_value(self,value,type):
		value=str(value)
		if type=='both':
			value = "%%"+value+"%%"
		elif type=='before':
			value = "%%"+value
		elif type=="after":
			value = "%%"+value
		
		return value
	def get_meta_data(self,id):
		dataDict={}
		table = self.tablePrefix + self.table;
		if self.checkTableExists('meta')==True:
			data = self.query.select("select * from "+table+"meta where "+self.relation_key+"= %s",(str(id)))
			for value in data:
				#print(self.is_json(value['meta_value']))
				try:
					json_object = json.loads(value['meta_value'])
					dataDict[value['meta_key']]=  json_object
				except:
					dataDict[value['meta_key']]=  value['meta_value']
				
			#print("select * from "+table+"meta where "+self.relation_key+"= %s"+str(id))
		return dataDict
	def get_meta(self,id,key):
		if key=='':
			return get_meta_data(id)
		
		dataDict={}
		table = self.tablePrefix + self.table;
		if self.checkTableExists('meta')==True:
			data = self.query.select("select * from "+table+"meta where "+self.relation_key+"= %s and meta_key= %s",(str(id),str(key)))
			for value in data:
				#print(self.is_json(value['meta_value']))
				try:
					json_object = json.loads(value['meta_value'])
					dataDict[value['meta_key']]=  json_object
				except:
					dataDict[value['meta_key']]=  value['meta_value']
				
			#print("select * from "+table+"meta where "+self.relation_key+"= %s"+str(id))
			
		return dataDict
	def get_meta_data_key(self,id):
		dataDict=[]
		table = self.tablePrefix + self.table;
		if self.checkTableExists('meta')==True:
			data = self.query.select("select * from "+table+"meta where "+self.relation_key+"= %s",(str(id)))
			for value in data:
					dataDict.append(value['meta_key'])
			#print("select * from "+table+"meta where "+self.relation_key+"= %s"+str(id))
		return dataDict
	def is_json(self,myjson):
		try:
			json_object = json.loads(myjson)
			return 1
		except:
			return 0
		
	def remove_meta_data(self,id):
		table = self.tablePrefix + self.table;
		if self.checkTableExists('meta')==True:
		#sql = "delete from "
			self.query.delete("delete from "+table+"meta where "+self.relation_key+"= %s",(str(id)))
		#print("delete from "+table+"meta where "+self.relation_key+"= %s")
		return ''
	def remove(self,type="no"):
		table = self.tablePrefix + self.table;
		self.delete_query += table
		if self.cond > 0:
			self.delete_query += self.where_query;
		else:
			whr = " where " + self.space + table + ".id" + self.space + "=" + self.space +  table+ ".id";
			self.delete_query += whr;
		self.completeQuery = self.delete_query;
		self.query.delete(self.completeQuery)
		#if type=="yes":
			#self.remove_meta_data(id)
		return True
	def get_by(self,keyname='',value=''):
		if keyname != '':
			self.where(keyname,"=",value)
		return self.findAll()
	def setJoin(self,jointype= ''):
		self.join_type = jointype
		return self
	def clear(self):
		self.__init__();