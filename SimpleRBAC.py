import sqlite3

class SimpleRBAC():
	def __init__(self, conn):
		self.conn = conn
		self.db_init()

	def db_init(self):
		#Masters
		self.conn.execute("CREATE TABLE IF NOT EXISTS ROLE_MASTER(" \
			"ID INTEGER PRIMARY KEY AUTOINCREMENT," \
			"ROLE_NAME TEXT UNIQUE," \
			"DESCRIPTION TEXT);")

		self.conn.execute("CREATE TABLE IF NOT EXISTS RESOURCE_MASTER(" \
			"ID INTEGER PRIMARY KEY AUTOINCREMENT," \
			"RESOURCE_NAME TEXT UNIQUE," \
			"DESCRIPTION TEXT);")

		self.conn.execute("CREATE TABLE IF NOT EXISTS AUTH_MASTER(" \
			"ID INTEGER PRIMARY KEY AUTOINCREMENT," \
			"AUTH_NAME TEXT UNIQUE," \
			"DESCRIPTION TEXT);")

		#Maps
		self.conn.execute("CREATE TABLE IF NOT EXISTS USER_ROLE_MAP(" \
			"ID INTEGER," \
			"USER_ID INTEGER," \
			"ROLE_ID INTEGER," \
			"PRIMARY KEY(ID AUTOINCREMENT)," \
			"UNIQUE(USER_ID, ROLE_ID));")

		self.conn.execute("CREATE TABLE IF NOT EXISTS ROLE_RESOURCE_AUTH_MAP(" \
			"ID INTEGER," \
			"ROLE_ID INTEGER," \
			"RESOURCE_ID INTEGER," \
			"AUTH_ID INTEGER," \
			"PRIMARY KEY(ID AUTOINCREMENT)," \
			"UNIQUE(ROLE_ID, RESOURCE_ID, AUTH_ID));")

		self.conn.execute("CREATE TABLE IF NOT EXISTS RESOURCE_AUTH_MAP(" \
			"ID INTEGER," \
			"RESOURCE_ID INTEGER," \
			"AUTH_ID INTEGER," \
			"PRIMARY KEY(ID AUTOINCREMENT)," \
			"UNIQUE(RESOURCE_ID, AUTH_ID));")

		self.conn.commit()

	def if_exists_in_master(self, type, type_name):
		type = type.upper()
		return self.conn.execute(f"select (case when count(*) > 0 then True else False end) from {type}_MASTER" \
			" WHERE {type}_NAME = '" + type_name + "';")

	def add_in_masters(self, type, type_name, description):
		type = type.upper()
		try:
			self.conn.execute(f"insert into {type}_MASTER ({type}_NAME, DESCRIPTION) values ('{type_name}', '{description}');")
			self.conn.commit()
			return f'{type} Created Successfully'
		except sqlite3.IntegrityError as e:
			return f'{type} Name already exists'
		except Exception as e:
			return str(e)

	def edit_in_masters(self, type, type_name, description=None):
		type = type.upper()
		try:
			if not self.if_exists_in_master(type, type_name):
				return f"{type} Name doesn't exists"
			if description:
				self.conn.execute(f"update {type}_MASTER set {type}_NAME = '{type_name}', DESCRIPTION = '{description}';")
			else:
				self.conn.execute(f"update {type}_MASTER set {type}_NAME = '{type_name}';")
			self.conn.commit()
			return f'{type} Name Updated Successfully'
		except sqlite3.IntegrityError as e:
			return f'{type} Name already exists'
		except Exception as e:
			return str(e)

	def delete_in_masters(self, type, type_name):
		type = type.upper()
		try:
			if not self.if_exists_in_master(type, type_name):
				return f"{type} Name doesn't exists"
			self.conn.execute(f"delete {type}_MASTER where {type}_NAME = '{type_name}';")
			self.conn.commit()
			return 'Role Name Updated Successfully'
		except sqlite3.IntegrityError as e:
			return 'Role Name already exists'
		except Exception as e:
			return str(e)

	def resolve_pk(self, type, type_name):
		type = type.upper()
		try:
			if not self.if_exists_in_master(type, type_name):
				return f"{type} Name doesn't exists"
			ret = self.conn.execute(f"select ID from {type}_MASTER where {type}_NAME = '{type_name}';").fetchone()[0]
			return int(ret)
		except Exception as e:
			return str(e)

	def add_user_role_map(self, user_id, role_id, resolve_pk=False):
		role_id = role_id if isinstance(role_id, list) else [role_id]
		if resolve:
			user_id = resolve_pk('USER', user_id)
			role_id = [resolve_pk(i) for i in role_id]
		try:
			query = "INSERT INTO USER_ROLE_MAP (USER_ID, ROLE_ID) VALUES "
			query += ", ".join([f"({user_id}, {id})" for id in role_id])
			query += " ON CONFLICT DO NOTHING;"
			self.conn.execute(query)
			self.conn.commit()
		except Exception as e:
			return str(e)

	def get_available_roles(self):
		elements = self.conn.execute("select ROLE_NAME, DESCRIPTION from ROLE_MASTER").fetchall()
		return elements#pk, role_table

	def add_role_resource_auth_map(self, role_name, resource_name, auth_name):
		pass

	def get_available_resources(self):
		elements = self.conn.execute("select * from RESOURCE_MASTER").fetchall()
		role_table = [[i+1, elements[i][1], elements[i][2]] for i in range(len(elements))]
		primary_keys = [elements[i][0] for i in range(len(elements))]
		return primary_keys, role_table

	def get_available_auth_for_resource(self, resource_name):
		pass



	def add_resource_auth_map(self, resource_name, auth_name, resolve_pk=False):

		pass

	def validate_access(self, uname, auth_name):
		pass
