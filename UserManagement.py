import sqlite3
import hashlib

class UserManagement():
	def __init__(self, conn):
		self.conn = conn
		self.conn.execute("CREATE TABLE IF NOT EXISTS USER_MASTER(" \
			"ID INTEGER PRIMARY KEY AUTOINCREMENT," \
			"FNAME TEXT," \
			"LNAME TEXT NOT NULL," \
			"USER_NAME TEXT NOT NULL UNIQUE," \
			"PASSWORD TEXT NOT NULL);")

	def add_user(self, fname, lname, uname, passw):
		try:
			self.conn.execute("insert into USER_MASTER (FNAME, LNAME, USER_NAME, PASSWORD) values " \
				f"('{fname}', '{lname}', '{uname}', '{hashlib.sha256(passw.encode()).hexdigest()}');")
			self.conn.commit()
			return 'User Created Successfully\n\n'
		except sqlite3.IntegrityError as e:
			return 'User Name already exists\n\n'
		except Exception as e:
			return str(e)+"\n\n"

	def edit_user(self, uname, editdict):
		query = "UPDATE USER_MASTER SET " + \
			", ".join([f"{k} = '{v}'" if k != 'PASSWORD' else f"{k} = '{hashlib.sha256(v.encode()).hexdigest()}'" for k, v in editdict.items()]) + \
			" WHERE USER_NAME = '" + uname + "';"
		try:
			self.conn.execute(query)
			self.conn.commit()
			return 'User Edited Successfully\n\n'
		except Exception as e:
			return str(e)+"\n\n"

	def delete_user(self, uname):
		try:
			self.conn.execute("DELETE FROM USER_MASTER WHERE USER_NAME = '" + uname + "';")
			self.conn.commit()
			return 'User Deleted Successfully\n\n'
		except Exception as e:
			return str(e)

	def validate_user(self, uname):
		return self.conn.execute("select (case when count(*) > 0 then True else False end) from USER_MASTER" \
			" WHERE USER_NAME = '" + uname + "';").fetchone()[0]

	def validate_login(self, uname, passw):
		passw = hashlib.sha256(passw.encode()).hexdigest()
		return self.conn.execute("select (case when count(*) > 0 then True else False end) AS RESULT from USER_MASTER" \
			f" where USER_NAME = '{uname}' and password = '{passw}'").fetchone()[0]

	def view_users_accesses(self, uname, view_type=1):
		query = "SELECT "
		if view_type == 1:
			query += "a.USER_NAME AS USER_NAME, " \
				"d.ROLE_NAME, " \
				"e.RESOURCE_NAME, " \
				"f.AUTH_NAME "

		elif view_type == 2:
			query += "DISTINCT " \
				"e.ID AS RESOURCE_ID, " \
				"e.RESOURCE_NAME, " \
				"f.ID AS AUTH_ID, " \
				"f.AUTH_NAME "

		query += "FROM USER_MASTER a " \
			"LEFT JOIN USER_ROLE_MAP b ON a.ID = b.USER_ID " \
			"LEFT JOIN ROLE_RESOURCE_AUTH_MAP c ON c.ROLE_ID = b.ROLE_ID " \
			"LEFT JOIN ROLE_MASTER d ON d.ID = c.ROLE_ID " \
			"LEFT JOIN RESOURCE_MASTER e ON e.ID = c.RESOURCE_ID " \
			"LEFT JOIN AUTH_MASTER f ON f.ID = c.AUTH_ID " \
			"WHERE a.USER_NAME = '" +uname+ "' " \
			"ORDER BY d.ROLE_NAME;"

		cur = self.conn.execute(query)
		headers = [i[0] for i in cur.description]
		elements = cur.fetchall()
		return elements, headers
