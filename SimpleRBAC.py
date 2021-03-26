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
			f" WHERE {type}_NAME = '" + type_name + "';").fetchone()[0]

	def add_in_masters(self, type, type_name, description):
		type = type.upper()
		try:
			self.conn.execute(f"INSERT INTO {type}_MASTER ({type}_NAME, DESCRIPTION) VALUES ('{type_name}', '{description}');")
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
				self.conn.execute(f"UPDATE {type}_MASTER SET {type}_NAME = '{type_name}', DESCRIPTION = '{description}';")
			else:
				self.conn.execute(f"UPDATE {type}_MASTER SET {type}_NAME = '{type_name}';")
			self.conn.commit()
			return f'{type} Name updated Successfully'
		except sqlite3.IntegrityError as e:
			return f'{type} Name already exists'
		except Exception as e:
			return str(e)

	def delete_in_masters(self, type, type_name):
		type = type.upper()
		try:
			if not self.if_exists_in_master(type, type_name):
				return f"{type} Name doesn't exists"
			self.conn.execute(f"DELETE FROM {type}_MASTER WHERE {type}_NAME = '{type_name}';")
			self.conn.commit()
			return 'Role Name Updated Successfully'
		except sqlite3.IntegrityError as e:
			return 'Role Name already exists'
		except Exception as e:
			return str(e)

	def get_from_masters(self, type):
		elements = self.conn.execute("select {type}_NAME, DESCRIPTION from {type}_MASTER").fetchall()
		return elements

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
		if resolve_pk:
			user_id = self.resolve_pk('USER', user_id)
			role_id = [self.resolve_pk('ROLE', i) for i in role_id]
		try:
			query = "INSERT INTO USER_ROLE_MAP (USER_ID, ROLE_ID) VALUES "
			query += ", ".join([f"({user_id}, {id})" for id in role_id])
			query += " ON CONFLICT DO NOTHING;"
			self.conn.execute(query)
			self.conn.commit()
		except Exception as e:
			return str(e)

	def delete_user_role_map(self, user_id, role_id=None, resolve_pk=False):
		if user_id and role_id:
			role_id = role_id if isinstance(role_id, list) else [role_id]
			if resolve_pk:
				user_id = self.resolve_pk('USER', user_id)
				role_id = [self.resolve_pk('ROLE', i) for i in role_id]
			try:
				query = "DELETE FROM USER_ROLE_MAP WHERE (USER_ID ||','|| ROLE_ID) in "
				query += str(tuple(f"{user_id},{id}" for id in role_id))
				self.conn.execute(query)
				self.conn.commit()
			except Exception as e:
				return str(e)
		if not user_id and role_id:
			try:
				role_id = self.resolve_pk('ROLE', role_id) if resolve_pk == True else role_id
				query = "DELETE FROM USER_ROLE_MAP WHERE ROLE_ID = " + role_id
				self.conn.execute(query)
				self.conn.commit()
			except Exception as e:
				return str(e)
		else:
			try:
				user_id = self.resolve_pk('USER', user_id) if resolve_pk == True else user_id
				query = "DELETE FROM USER_ROLE_MAP WHERE USER_ID = " + user_id
				self.conn.execute(query)
				self.conn.commit()
			except Exception as e:
				return str(e)

	def get_roles_assigned_to_user(self, uname):
		query = "SELECT " \
			"c.ROLE_NAME, " \
			"c.DESCRIPTION " \
			"FROM USER_MASTER a " \
			"LEFT JOIN USER_ROLE_MAP b ON a.ID = b.USER_ID " \
			"LEFT JOIN ROLE_MASTER c ON c.ID = b.ROLE_ID " \
			"WHERE a.uname = '" + uname + "';"
		elements = self.conn.execute(query).fetchall()
		return elements

	def get_auth_for_resource(self, resource_name):
		query = "SELECT " \
			"c.AUTH_NAME, " \
			"c.DESCRIPTION " \
			"FROM RESOURCE_MASTER a " \
			"LEFT JOIN RESOURCE_AUTH_MAP b ON b.RESOURCE_ID = a.ID " \
			"LEFT JOIN AUTH_MASTER c ON c.ID = b.AUTH_ID " \
			"WHERE a.RESOURCE_NAME = '" +resource_name+ "';"

		elements = self.conn.execute(query).fetchall()
		return elements

	def add_role_resource_auth_map(self, role_id, resource_id, auth_id, resolve_pk=False):
		auth_id = auth_id if isinstance(auth_id, list) else [auth_id]
		if resolve_pk:
			role_id = self.resolve_pk('ROLE', role_id)
			resource_id = self.resolve_pk('RESOURCE', resource_id)
			auth_id = [self.resolve_pk('ROLE', i) for i in auth_id]
		try:
			query = "INSERT INTO ROLE_RESOURCE_AUTH_MAP (ROLE_ID, RESOURCE_ID, AUTH_ID) VALUES "
			query += ", ".join([f"({role_id}, {resource_id}, {id})" for id in auth_id])
			query += " ON CONFLICT DO NOTHING;"
			self.conn.execute(query)
			self.conn.commit()
		except Exception as e:
			return str(e)

	def delete_role_resource_auth_map(self, role_id=None, resource_id=None, auth_id=None, pk_id=None, resolve_pk=False):
		if pk_id:
			pk_id = pk_id if isinstance(pk_id, list) else [pk_id]
			try:
				query = "DELETE FROM ROLE_RESOURCE_AUTH_MAP WHERE ID in "
				query += str(tuple(pk_id))
				self.conn.execute(query)
				self.conn.commit()
			except Exception as e:
				return str(e)

		elif role_id and resource_id and auth_id:
			auth_id = auth_id if isinstance(auth_id, list) else [auth_id]
			if resolve_pk:
				role_id = self.resolve_pk('ROLE', role_id)
				resource_id = self.resolve_pk('RESOURCE', resource_id)
				auth_id = [self.resolve_pk('AUTH', i) for i in auth_id]
			try:
				query = "DELETE FROM ROLE_RESOURCE_AUTH_MAP WHERE (ROLE_ID ||','|| RESOURCE_ID ||','|| AUTH_ID) in "
				query += str(tuple(f"{role_id},{resource_id},{id}" for id in auth_id))
				self.conn.execute(query)
				self.conn.commit()
			except Exception as e:
				return str(e)

		elif role_id and resource_id:
			resource_id = resource_id if isinstance(resource_id, list) else [resource_id]
			if resolve_pk:
				role_id = self.resolve_pk('ROLE', resource_id)
				resource_id = [self.resolve_pk('RESOURCE', i) for i in resource_id]
			try:
				query = "DELETE FROM ROLE_RESOURCE_AUTH_MAP WHERE (ROLE_ID ||','|| RESOURCE_ID) in "
				query += str(tuple(f"{role_id},{id}" for id in resource_id))
				self.conn.execute(query)
				self.conn.commit()
			except Exception as e:
				return str(e)

		elif role_id:
			if resolve_pk:
				role_id = self.resolve_pk('ROLE', role_id)
			try:
				query = f"DELETE FROM ROLE_RESOURCE_AUTH_MAP WHERE ROLE_ID = {role_id}"
				self.conn.execute(query)
				self.conn.commit()
			except Exception as e:
				return str(e)

		elif not role_id and resource_id:
			try:
				resource_id = self.resolve_pk('RESOURCE', resource_id) if resolve_pk == True else resource_id
				query = "DELETE FROM RESOURCE_AUTH_MAP WHERE RESOURCE_ID = " + resource_id
				self.conn.execute(query)
				self.conn.commit()
			except Exception as e:
				return str(e)

	def get_role_resource_auth_map(self):
		query = "SELECT " \
			"a.ID, " \
			"b.ROLE_NAME, " \
			"c.RESOURCE_NAME, " \
			"d.AUTH_NAME " \
			"FROM ROLE_RESOURCE_AUTH_MAP a " \
			"LEFT JOIN ROLE_MASTER b ON b.ID = a.ROLE_ID " \
			"LEFT JOIN RESOURCE_MASTER c ON c.ID = a.RESOURCE_ID " \
			"LEFT JOIN AUTH_MASTER d ON d.ID = a.AUTH_ID"

		elements = self.conn.execute(query).fetchall()
		return elements


	def add_resource_auth_map(self, resource_id, auth_id, resolve_pk=False):
		auth_id = auth_id if isinstance(auth_id, list) else [auth_id]
		if resolve:
			resource_id = self.resolve_pk('RESOURCE', resource_id)
			auth_id = [self.resolve_pk('AUTH', i) for i in auth_id]
		try:
			query = "INSERT INTO RESOURCE_AUTH_MAP (RESOURCE_ID, AUTH_ID) VALUES "
			query += ", ".join([f"({resource_id}, {id})" for id in auth_id])
			query += " ON CONFLICT DO NOTHING;"
			self.conn.execute(query)
			self.conn.commit()
		except Exception as e:
			return str(e)

	def delete_resource_auth_map(self, resource_id, auth_id=None, resolve_pk=False):
		if auth_id:
			auth_id = auth_id if isinstance(auth_id, list) else [auth_id]
			if resolve_pk:
				resource_id = self.resolve_pk('RESOURCE', resource_id)
				auth_id = [self.resolve_pk('AUTH', i) for i in auth_id]
			try:
				query = "DELETE FROM RESOURCE_AUTH_MAP WHERE (RESOURCE_ID ||','|| AUTH_ID) in "
				query += str(tuple(f"{resource_id},{id}" for id in auth_id))
				self.conn.execute(query)
				self.conn.commit()
			except Exception as e:
				return str(e)
		else:
			try:
				resource_id = self.resolve_pk('RESOURCE', resource_id) if resolve_pk == True else resource_id
				query = "DELETE FROM RESOURCE_AUTH_MAP WHERE RESOURCE_ID = " + resource_id
				self.conn.execute(query)
				self.conn.commit()
			except Exception as e:
				return str(e)

	def if_admin(self, uname):
		if self.if_exists_in_master('USER', uname):
			uid = self.resolve_pk('USER', uname)
			return self.conn(f"select (case when count(*) > 0 then True else False end) " \
				"from USER_ROLE_MAP " \
				"WHERE USER_ID = " + str(uid) + " AND ROLE_ID = 0;").fetchone()[0]
