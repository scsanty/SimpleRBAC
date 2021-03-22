import hashlib
import sqlite3
import dummy_data_init
import getpass
import os, sys

class SimpleRBAC():
	def __init__(self, conn):
		self.conn = conn
		self.db_init()

	def db_init(self):
		self.conn.execute("CREATE TABLE IF NOT EXISTS ROLE_MAPPING(" \
			"ID INTEGER PRIMARY KEY AUTOINCREMENT," \
			"ROLE_ID INTEGER," \
			"AUTH_ID INTEGER);")

		self.conn.execute("CREATE TABLE IF NOT EXISTS ROLE_MASTER(" \
			"ID INTEGER PRIMARY KEY AUTOINCREMENT," \
			"ROLE_NAME TEXT);")

		self.conn.execute("CREATE TABLE IF NOT EXISTS RESOURCE_MASTER(" \
			"ID INTEGER PRIMARY KEY AUTOINCREMENT," \
			"RESOURCE_NAME TEXT);")

		self.conn.execute("CREATE TABLE IF NOT EXISTS AUTH_MASTER(" \
			"ID INTEGER PRIMARY KEY AUTOINCREMENT," \
			"AUTH_NAME TEXT," \
			"DESCRIPTION TEXT);")

		self.conn.commit()
		return self.conn

	def add_role(self):
		pass

	def add_resource(self):
		pass

	def add_auth(self):
		pass

	def validate_access(self, uname, auth_name):
		pass

class UserManagement():
	def __init__(self, conn):
		self.conn = conn
		self.conn.execute("CREATE TABLE IF NOT EXISTS USER_MASTER(" \
			"ID INTEGER PRIMARY KEY AUTOINCREMENT," \
			"FNAME TEXT," \
			"LNAME TEXT NOT NULL," \
			"UNAME TEXT NOT NULL UNIQUE," \
			"PASSWORD TEXT NOT NULL," \
			"ROLE_ID INTEGER);")

			self.add_user('ADMIN', 'ADMIN', 'ADMIN', 'ADMIN', 0)

	def add_user(self, fname, lname, uname, passw, role_id=None):
		try:
			if role_id:
				self.conn.execute("insert into USER_MASTER (FNAME, LNAME, UNAME, PASSWORD, ROLE_ID) values " \
					f"('{fname}', '{lname}', '{uname}', '{hashlib.sha256(passw.encode()).hexdigest()}', {role_id});")
			else:
				self.conn.execute("insert into USER_MASTER (FNAME, LNAME, UNAME, PASSWORD, ROLE_ID) values " \
					f"('{fname}', '{lname}', '{uname}', '{hashlib.sha256(passw.encode()).hexdigest()}', NULL);")
			self.conn.commit()
		except sqlite3.IntegrityError as e:
			print(str(e))

	def edit_user(self, uname, editdict):
		query = "UPDATE USER_MASTER SET " +
			", ".join([f"{k} = '{v}'" if k != 'PASSWORD' else f"{k} = '{hashlib.sha256(v.encode()).hexdigest()}'" for k, v in editdict.items()]) +
			" WHERE uname = '" + uname + "';"
		self.conn.execute(query)
		self.conn.commit()

	def delete_user(self, uname):
		self.conn.execute("DELETE FROM USER_MASTER WHERE uname = '" + uname + "';")
		self.conn.commit()

	def validate_user(self, uname, passw):
		passw = hashlib.sha256(passw.encode()).hexdigest()
		return self.conn.execute(f"select (case when count(*) > 0 then True else False end) AS RESULT from USER_MASTER where uname = '{uname}' and password = '{passw}'").fetchone()[0]

class MainAppCLI():
	prompt = 'App>'
	banner = ("#"*50).ljust(50)+"\n"+ \
		"#".ljust(49)+"#\n" + \
		"#"+"MainApp with RBAC".center(48)+"#\n"+ \
		"#".ljust(49)+"#\n"+ \
		("#"*50).ljust(50)

	clear = lambda self: os.system('cls') if os.name == 'nt' else os.system('clear')

	def __init__(self):
		self.clear()
		self.conn = sqlite3.connect('temp.db')
		# self.conn = sqlite3.connect(':memory:')
		self.simplerbac = SimpleRBAC(self.conn)
		self.uman = UserManagement(self.conn)

		wronginputcounter = 0
		while wronginputcounter < 3:
			uname = input("User Name: ")
			passw = getpass.getpass("Password: ")
			if self.uman.validate_user(uname, passw):
				break
			else:
				print("Wrong User Name/Password Combination, Please try again")
				wronginputcounter += 1

		if wronginputcounter == 3:
			print("Try limit exceeded")
			sys.exit(0)

		self.question_dummy_data_load()
		print(self.banner)
		self.clear()

	def question_dummy_data_load(self):
		if self.simplerbac.conn.execute("select count(*) from USER_MASTER").fetchone()[0] == 1:
			answer = input("Do you want load Dummy Data? [Y/n]: ")
			if answer.upper() == 'Y':
				dummy_data_init.dummy_data_init(self.conn)
		return

	def admin_screen(self):
		def invalid():
			print("Invalid option\nTry Again")
			self.admin_screen()
		def call_userman():
			def call_createuser():
				fname = input("Input First Name of the user: ")
				lname = input("Input Last Name of the user: ")
				uname = input("Input User Name of the user: ")
				passw = input("Input Password of the user: ")
				self.uman.add_user(fname, lname, uname, passw, role_id=None)
			def call_edituser():
				pass
			def call_deleteuser():
				uname = input("Input User Name of the user: ")
				self.uman.delete_user(uname)
			print(
				"Type 1 to Create User\n" \
				"Type 2 to Edit User\n" \
				"Type 3 to Delete User\n"
			)
			{
				'1': call_createuser,
				'2': call_edituser,
				'3': call_deleteuser
			}.get(
				input(
					"App>"
					), invalid)()
			pass
		def call_roleman():
			pass
		def call_resourceman():
			pass
		def call_authman():
			pass

		print(
			"Type 1 to Manage Users\n" \
			"Type 2 to Manage Roles\n" \
			"Type 3 to Manage Resources\n" \
			"Type 4 to Manage Authorisations\n"
		)
		{
			'1': call_userman,
			'2': call_roleman,
			'3': call_resourceman,
			'4' : call_authman
		}.get(
			input(
				"App>"
				), invalid)()




if __name__ == "__main__":
	MainAppCLI()
#
#
#
# while inputx != 'x':
# 	print("")
# 	inputx = input("Enter your choice: ")
#
#
# ## TESTING
#
# class testclass():
# 	testvar = 1
# 	def __init__(self):
# 		print(self.testvar)
#
# 	def nothing(self):
# 		print(self.testvar)
#
# testobj = testclass()
#
#
# conn.execute("insert into USER_MASTER (FNAME, LNAME, UNAME, PASSWORD, ROLE_ID) values " \
# 	f"('test', 'test', 'test', '{hashlib.sha256('ADMIN'.encode()).hexdigest()}', NULL);")

# conn = sqlite3.connect('temp.db')
# if conn.execute(f"select (case when count(*) > 0 then True else False end) AS RESULT from USER_MASTER where uname = 'ADMIN0' and password = '{hashlib.sha256('ADMIN'.encode()).hexdigest()}'").fetchone()[0]:
# 	print("T")



query =


for k, v in {'FNAME' : 'LOL', 'PASSWORD' : 'NEWPASS'}.items():
	if k == 'PASSWORD':
		v = hashlib.sha256(v.encode()).hexdigest()
	query += k + "=" + v ", "

uname = 'SANTY'
editdict = {'FNAME' : 'LOL', 'PASSWORD' : 'NEWPASS'}

editdict.get('FNAME')

a = 15
test = 10 if a < 10
test
print
