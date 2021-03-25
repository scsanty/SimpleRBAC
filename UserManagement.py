import sqlite3
import hashlib

class UserManagement():
	def __init__(self, conn):
		self.conn = conn
		self.conn.execute("CREATE TABLE IF NOT EXISTS USER_MASTER(" \
			"ID INTEGER PRIMARY KEY AUTOINCREMENT," \
			"FNAME TEXT," \
			"LNAME TEXT NOT NULL," \
			"UNAME TEXT NOT NULL UNIQUE," \
			"PASSWORD TEXT NOT NULL);")

	def add_user(self, fname, lname, uname, passw):
		try:
			self.conn.execute("insert into USER_MASTER (FNAME, LNAME, UNAME, PASSWORD) values " \
				f"('{fname}', '{lname}', '{uname}', '{hashlib.sha256(passw.encode()).hexdigest()}');")
			self.conn.commit()
			return 'User Created Successfully'
		except sqlite3.IntegrityError as e:
			return 'User Name already exists'
		except Exception as e:
			return str(e)

	def edit_user(self, uname, editdict):
		query = "UPDATE USER_MASTER SET " + \
			", ".join([f"{k} = '{v}'" if k != 'PASSWORD' else f"{k} = '{hashlib.sha256(v.encode()).hexdigest()}'" for k, v in editdict.items()]) + \
			" WHERE uname = '" + uname + "';"
		try:
			self.conn.execute(query)
			self.conn.commit()
		except Exception as e:
			return str(e)

	def delete_user(self, uname):
		try:
			self.conn.execute("DELETE FROM USER_MASTER WHERE uname = '" + uname + "';")
			self.conn.commit()
		except Exception as e:
			return str(e)

	def validate_user(self, uname):
		return self.conn.execute("select (case when count(*) > 0 then True else False end) from USER_MASTER" \
			" WHERE uname = '" + uname + "';")

	def validate_login(self, uname, passw):
		passw = hashlib.sha256(passw.encode()).hexdigest()
		return self.conn.execute("select (case when count(*) > 0 then True else False end) AS RESULT from USER_MASTER" \
			f" where uname = '{uname}' and password = '{passw}'").fetchone()[0]

	def view_users_accesses(self, uname):
		query = "SELECT" \
			"a.uname AS USER_NAME," \
			"d.ROLE_NAME," \
			"e.RESOURCE_NAME," \
			"f.AUTH_NAME" \
			"FROM USER_MASTER a" \
			"LEFT JOIN USER_ROLE_MAP b ON a.ID = b.USER_ID" \
			"LEFT JOIN ROLE_RESOURCE_AUTH_MAP c ON c.ROLE_ID = b.ROLE_ID" \
			"LEFT JOIN ROLE_MASTER d ON d.ID = c.ROLE_ID" \
			"LEFT JOIN RESOURCE_MASTER e ON e.ID = c.RESOURCE_ID" \
			"LEFT JOIN AUTH_MASTER f ON f.ID = c.AUTH_ID" \
			"WHERE a.uname = '"uname"';"

		cur = conn.execute(query)
		headers = [i[0] for i in cur.description]
		return cur.fetchall(), headers
		# print(tabulate(cur.fetchall(), headers=headers, tablefmt="pretty"))

	def admin_or_user_session():
		pass
