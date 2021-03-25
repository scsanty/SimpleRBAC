import hashlib
import sqlite3
import dummy_data_init
import getpass
import os, sys
from tabulate import tabulate
from SimpleRBAC import SimpleRBAC

class MainAppCLI():
	banner = lambda self: print(("#"*50).ljust(50)+"\n"+ \
		"#".ljust(49)+"#\n" + \
		"#"+"MainApp with RBAC".center(48)+"#\n"+ \
		"#".ljust(49)+"#\n"+ \
		("#"*50).ljust(50))

	clear = lambda self: os.system('cls') if os.name == 'nt' else os.system('clear')

	def __init__(self):
		self.clear()
		self.conn = sqlite3.connect('temp.db')
		# self.conn = sqlite3.connect(':memory:')
		self.simplerbac = SimpleRBAC(self.conn)
		self.uman = UserManagement(self.conn)

		self.uman.add_user('ADMIN', 'ADMIN', 'ADMIN', 'ADMIN')
		self.simplerbac.add_user_role_map(1, 0):
		# self.simplerbac.map_role()

		wronginputcounter = 0
		while wronginputcounter < 3:
			uname = input("User Name: ")
			passw = getpass.getpass("Password: ")
			if self.uman.validate_login(uname, passw):
				break
			else:
				print("Wrong User Name/Password Combination, Please try again")
				wronginputcounter += 1

		if wronginputcounter == 3:
			print("Try limit exceeded")
			sys.exit(0)

		self.question_dummy_data_load()
		self.clear()
		self.banner()

	def question_dummy_data_load(self):
		if self.conn.execute("select count(*) from USER_MASTER").fetchone()[0] == 1:
			answer = input("Do you want load Dummy Data? [Y/n]: ")
			if answer.upper() in ['Y', '']:
				dummy_data_init.dummy_data_init(self.conn)
		return

	def admin_screen(self):
		def call_userman():
			def call_createuser():
				fname = input("Input First Name of the user: ")
				lname = input("Input Last Name of the user: ")
				uname = input("Input User Name of the user: ")
				passw = input("Input Password of the user: ")

				print(self.uman.add_user(fname, lname, uname, passw))

			def call_edituser():
				uname = input("Input User Name of the user: ")
				if not self.uman.validate_user(uname):
					print("User doesn't exist")
					return

				editdict = {'FNAME': None, 'LNAME': None, 'PASSWORD': None}

				if input("Do you want to edit the First Name of the user: ").upper() == 'Y':
					editdict['FNAME'] = input("Input First Name of the user: ")

				if input("Do you want to edit the Last Name of the user: ").upper() == 'Y':
					editdict['LNAME'] = input("Input Last Name of the user: ")

				if input("Do you want to update the password of the user: ").upper() == 'Y':
					editdict['PASSWORD'] = input("Input Password of the user: ")

				editdict={k:v for k,v in editdict.items() if v}
				print(self.uman.edit_user(uname, editdict))

			def call_deleteuser():
				uname = input("Input User Name of the user: ")
				if not self.uman.validate_user(uname):
					print("User doesn't exist")
					return
				self.uman.delete_user(uname)

			def call_assignroles():
				uname = input("Input User Name of the user: ")
				if not self.uman.validate_user(uname):
					print("User doesn't exist")
					return
				role_table = get_available_roles()
				role_table = [[i+1, role_table[i][0], role_table[i][1]] for i in range(len(role_table))]
				print(tabulate(role_table, tablefmt='pretty', headers=['Sl.No.', 'Role Name', 'Description']))

				choices = input("Enter the serial numbers, separated by commas, e.g.: 1, 2\nApp>")
				try:
					choices = set(int(i.strip())-1 for i in choices.split(sep=','))
					if not choices.issubset(set(range(len(table)))):
						print("Sl.No. from the given table is only accepted")
						return
				except ValueError:
					print("Invalid literal, only numbers separated by commas are accepted")
					return
				except Exception as e:
					print(str(e))
					return
				choices = [role_table[i][0] for i in choices]
				self.simplerbac.add_user_role_map(self, uname, role_name, resolve_pk=True)

			def call_removeroles():
				uname = input("Input User Name of the user: ")
				if not self.uman.validate_user(uname):
					print("User doesn't exist")
					return



			print(
				"Type 1 to Create User\n" \
				"Type 2 to Edit User\n" \
				"Type 3 to Delete User\n" \
				"Type 4 to Assign Roles to User\n" \
				"Type 5 to Remove Roles from User\n" \
				"Type < to Go Back\n"
			)
			ret = {
				'1': call_createuser,
				'2': call_edituser,
				'3': call_deleteuser,
				'4': call_assignroles,
				'5': call_removeroles,
				'<': lambda:"Go Back"
			}.get(
				input(
					"App>"
					), lambda:print("Invalid option\nTry Again"))()

			if ret == "Go Back":
				return
			else:
				call_userman()

		def call_roleman():

			call_roleman()

		def call_resourceman():

			call_resourceman()

		def call_authman():

			call_authman()

		print(
			"Type 1 to Manage Users\n" \
			"Type 2 to Manage Roles\n" \
			"Type 3 to Manage Resources\n" \
			"Type 4 to Manage Authorisations\n" \
			"Type x to Exit"
		)
		ret = {
			'1': call_userman,
			'2': call_roleman,
			'3': call_resourceman,
			'4': call_authman,
			'x': lambda:"Exit"
		}.get(
			input(
				"App>"
				), lambda:print("Invalid option\nTry Again"))()

		if ret == "Exit":
			print('Bye')
			return
		else:
			self.admin_screen()

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


# query =
#
#
# for k, v in {'FNAME' : 'LOL', 'PASSWORD' : 'NEWPASS'}.items():
# 	if k == 'PASSWORD':
# 		v = hashlib.sha256(v.encode()).hexdigest()
# 	query += k + "=" + v ", "
#
# uname = 'SANTY'
# editdict = {'FNAME' : 'LOL', 'PASSWORD' : 'NEWPASS'}
#
# editdict.get('FNAME')
#
# a = 15
# test = 10 if a < 10
# test
# print
#
#
# def blah():
# 	a = 15
# 	t = lambda: exec("global a\na = 16")
# 	t()
# 	print(a)
# blah()
#
#
#
# t = lambda:"go_back"
# t()
#
# editdict = {'FNAME': None, 'LNAME': 'ervafc', 'PASSWORD': None}
# editdict = {k:v for k,v in editdict.items() if v}
# editdict

conn = sqlite3.connect("temp.db")
uname = "BUSER00"
table = conn.execute("select * from ROLE_MASTER").fetchall()
table


role_table = [[i+1, table[i][1], table[i][2]] for i in range(len(table))]
primary_keys = [table[i][0] for i in range(len(table))]
role_table
primary_keys
print(tabulate(table, tablefmt='pretty', headers=[' ', 'Role Name', 'Description']))


t = '1, 2, "9'
t = set(int(i.strip())-1 for i in t.split(sep=','))
t.issubset(set(range(len(table))))
t
set(range(len(table)))


try:
	t = set(int(i.strip())-1 for i in t.split(sep=','))
	if not t.issubset(set(range(len(table)))):
		print("Please Enter Sl.No. from the given table only")
except ValueError:
	print("Invalid literal, Please enter numbers separated by commas only")
except Exception as e:
	print(str(e))



user_id = '12'
role_id = ['1', '2']
strx = ", ".join([f"({user_id}, {id})" for id in role_id])
strx
