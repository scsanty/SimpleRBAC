import hashlib
import sqlite3
import dummy_data_init
import getpass
import os, sys
from tabulate import tabulate
import pandas as pd
from SimpleRBAC import SimpleRBAC
from UserManagement import UserManagement
import Resources

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
		self.simplerbac.add_user_role_map(1, 0)

		wronginputcounter = 0
		while wronginputcounter < 3:
			self.uname = input("User Name: ")
			self.passw = getpass.getpass("Password: ")
			if self.uman.validate_login(self.uname, self.passw):
				break
			else:
				print("Wrong User Name/Password Combination, Please try again")
				wronginputcounter += 1

		if wronginputcounter == 3:
			print("Try limit exceeded")
			sys.exit(0)

		self.question_dummy_data_load()
		# elements, headers = self.simplerbac.view_users_accesses(view_type=2)
		# self.users_auth_map = pd.DataFrame(elements, columns=headers)
		self.clear()
		self.banner()
		if self.simplerbac.if_admin(self.uname):
			self.admin_session()
		else:
			self.user_session()

	def question_dummy_data_load(self):
		if self.conn.execute("select count(*) from USER_MASTER").fetchone()[0] == 1:
			answer = input("Do you want load Dummy Data? [Y/n]: ")
			if answer.upper() in ['Y', '']:
				dummy_data_init.dummy_data_init(self.conn)
		return

	def accessresource(self):
		def call_resource(resource_name):
			obj = None
			exec("obj = Resources."+resource_name+"()")
			obj.access_validator(self.uname)

		resource_table = self.simplerbac.get_from_masters('RESOURCE')
		resource_table = [[i+1, resource_table[i][0], resource_table[i][1]] for i in range(len(resource_table))]
		print(tabulate(resource_table, tablefmt='pretty', headers=['Sl.No.', 'Resource Name', 'Description']))
		print("Please type the Sl.No. of the resource you want to access\nType < to go back")
		choice_dict = {f'{i[0]}': f"{i[1]}" for i in resource_table}
		choice_dict['<'] = "Go Back"
		ret = dicti.get(
			input(
				"App>"
				), lambda:print("Invalid option\nTry Again"))

		if ret == "Go Back":
			return
		elif ret != None:
			call_resource(ret)
		self.call_accessresource()

	def viewmyaccesses(self):
		elements, headers = self.simplerbac.view_users_accesses(self.uname)
		print(tabulate(elements, tablefmt='pretty', headers=headers))

	def admin_session(self):
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
					return\
				print(self.simplerbac.delete_user_role_map(user_id = uname, resolve_pk=True))
				print(self.uman.delete_user(uname))

			def call_assignroles():
				uname = input("Input User Name of the user: ")
				if not self.uman.validate_user(uname):
					print("User doesn't exist")
					return
				role_table = get_from_masters('ROLE')
				role_table = [[i+1, role_table[i][0], role_table[i][1]] for i in range(len(role_table))]
				print(tabulate(role_table, tablefmt='pretty', headers=['Sl.No.', 'Role Name', 'Description']))

				choices = input("Enter the serial numbers, separated by commas, e.g.: 1, 2\nApp>")
				try:
					choices = set(int(i.strip())-1 for i in choices.split(sep=','))
					if not choices.issubset(set(range(len(role_table)))):
						print("Sl.No. from the given table is only accepted")
						return
				except ValueError:
					print("Invalid literal, only numbers separated by commas are accepted")
					return
				except Exception as e:
					print(str(e))
					return
				choices = [role_table[i][0] for i in choices]
				print(self.simplerbac.add_user_role_map(self, uname, role_name, resolve_pk=True))

			def call_removeroles():
				uname = input("Input User Name of the user: ")
				if not self.uman.validate_user(uname):
					print("User doesn't exist")
					return
				role_table = get_roles_assigned_to_user()
				role_table = [[i+1, role_table[i][0], role_table[i][1]] for i in range(len(role_table))]
				print(tabulate(role_table, tablefmt='pretty', headers=['Sl.No.', 'Role Name', 'Description']))

				choices = input("Enter the serial numbers, separated by commas, e.g.: 1, 2\nApp>")
				try:
					choices = set(int(i.strip())-1 for i in choices.split(sep=','))
					if not choices.issubset(set(range(len(role_table)))):
						print("Sl.No. from the given table is only accepted")
						return
				except ValueError:
					print("Invalid literal, only numbers separated by commas are accepted")
					return
				except Exception as e:
					print(str(e))
					return
				choices = [role_table[i][0] for i in choices]
				print(self.simplerbac.add_user_role_map(self, uname, role_name, resolve_pk=True))

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
			def call_createrole():
				role_name = input("Input Name of the role: ")
				description = input("Input Description for the role: ")
				print(self.simplerbac.add_in_masters('ROLE', role_name, description))

			def call_editrole():
				role_name = input("Input Name of the role: ")
				if input("Do you want to edit the Name of the role: ").upper() == 'Y':
					resource_name = input("Input Name of the role: ")
				description = None
				if input("Do you want to edit the Description of the role: ").upper() == 'Y':
					description = input("Input Description for the role: ")
				print(self.simplerbac.edit_in_masters('ROLE', role_name, description))

			def call_deleterole():
				role_name = input("Input Name of the role: ")
				print(self.simplerbac.delete_role_auth_map(role_id=role_name, resolve_pk=True))
				print(self.simplerbac.delete_user_role_map(role_id=role_name, resolve_pk=True))
				print(self.simplerbac.delete_in_masters('ROLE', role_name))

			def call_setuprole():
				def call_addrolemap():
					role_name = input("Input Name of the role: ")
					resource_table = self.simplerbac.get_from_masters('RESOURCE')
					resource_table = [[i+1, resource_table[i][0], resource_table[i][1]] for i in range(len(resource_table))]
					print(tabulate(resource_table, tablefmt='pretty', headers=['Sl.No.', 'Resource Name', 'Description']))
					resource_choice = input("Please type the Sl.No. of the resource you want to add to the role\nApp>")

					try:
						resource_choice = int(resource_choice) #set(int(i.strip())-1 for i in choices.split(sep=','))
						if not {resource_choice}.issubset(set(range(len(resource_table)))):
							print("Sl.No. from the given table is only accepted")
							return
					except ValueError:
						print("Invalid literal, only numbers separated by commas are accepted")
						return
					except Exception as e:
						print(str(e))
						return
					resource_choice = resource_table[resource_choice][0]

					auth_table = self.simplerbac.get_auth_for_resource(resource_choice)
					auth_table = [[i+1, auth_table[i][0], auth_table[i][1]] for i in range(len(auth_table))]
					print(tabulate(auth_table, tablefmt='pretty', headers=['Sl.No.', 'Auth Name', 'Description']))
					auth_choices = input("Enter the serial numbers, separated by commas, e.g.: 1, 2\nApp>")

					try:
						auth_choices = set(int(i.strip())-1 for i in auth_choices.split(sep=','))
						if not auth_choices.issubset(set(range(len(auth_table)))):
							print("Sl.No. from the given table is only accepted")
							return
					except ValueError:
						print("Invalid literal, only numbers separated by commas are accepted")
						return
					except Exception as e:
						print(str(e))
						return
					auth_choices = [auth_table[i][0] for i in auth_choices]

					print(self.simplerbac.add_role_resource_auth_map(role_name, resource_choice, auth_choices, resolve_pk=True))

				def call_deleterolemap():
					map_table = self.simplerbac.get_role_resource_auth_map()
					pk = [map_table[i][0] for i in range(len(map_table))]
					map_table = [[i+1, map_table[i][1], map_table[i][2], map_table[i][3]] for i in range(len(map_table))]
					print(tabulate(map_table, tablefmt='pretty', headers=['Sl.No.', 'Role Name', 'Resource Name', 'Auth Name']))
					choices = input("Enter the serial numbers, separated by commas, e.g.: 1, 2\nApp>")

					try:
						choices = set(int(i.strip())-1 for i in choices.split(sep=','))
						if not choices.issubset(set(range(len(map_table)))):
							print("Sl.No. from the given table is only accepted")
							return
					except ValueError:
						print("Invalid literal, only numbers separated by commas are accepted")
						return
					except Exception as e:
						print(str(e))
						return
					choices = [pk[i] for i in choices]

					print(self.simplerbac.delete_role_resource_auth_map(pk_id=choices))

				print(
					"Type 1 to Map Role to Authorisations\n" \
					"Type 2 to Delete a Role Mapping\n" \
					"Type < to Go Back\n"
				)
				ret = {
					'1': call_addrolemap,
					'2': call_deleterolemap,
					'<': lambda:"Go Back"
				}.get(
					input(
						"App>"
						), lambda:print("Invalid option\nTry Again"))()

				if ret == "Go Back":
					return
				else:
					call_setuprole()

			print(
				"Type 1 to Add Role\n" \
				"Type 2 to Edit Role\n" \
				"Type 3 to Delete Role\n" \
				"Type 4 to Setup a Role\n" \
				"Type < to Go Back\n"
			)
			ret = {
				'1': call_createrole,
				'2': call_editrole,
				'3': call_deleterole,
				'4': call_setuprole,
				'<': lambda:"Go Back"
			}.get(
				input(
					"App>"
					), lambda:print("Invalid option\nTry Again"))()

			if ret == "Go Back":
				return
			else:
				call_roleman()

		def call_resourceman():
			def call_createresource():
				resource_name = input("Input Name of the resource: ")
				description = input("Input Description for the resource: ")
				print(self.simplerbac.add_in_masters('RESOURCE', resource_name, description))

			def call_editresource():
				resource_name = input("Input Name of the resource: ")
				if input("Do you want to edit the Name of the resource: ").upper() == 'Y':
					resource_name = input("Input Name of the resource: ")
				description = None
				if input("Do you want to edit the Description of the resource: ").upper() == 'Y':
					description = input("Input Description for the resource: ")
				print(self.simplerbac.edit_in_masters('RESOURCE', resource_name, description))

			def call_deleteresource():
				resource_name = input("Input Name of the resource: ")
				self.simplerbac.delete_resource_auth_map(resource_id=resource_name, resolve_pk=True)
				self.simplerbac.delete_role_resource_auth_map(resource_id=resource_name, resolve_pk=True)
				print(self.simplerbac.delete_in_masters('RESOURCE', resource_name))

			print(
				"Type 1 to Register Resource\n" \
				"Type 2 to Edit Resource\n" \
				"Type 3 to Delete Resource\n" \
				"Type < to Go Back\n"
			)
			ret = {
				'1': call_createresource,
				'2': call_editresource,
				'3': call_deleteresource,
				'<': lambda:"Go Back"
			}.get(
				input(
					"App>"
					), lambda:print("Invalid option\nTry Again"))()

			if ret == "Go Back":
				return
			else:
				call_resourceman()


		print(
			"Type 1 to Manage Users\n" \
			"Type 2 to Manage Roles\n" \
			"Type 3 to Manage Resources\n" \
			"Type 4 to Access Resources\n" \
			"Type 5 to View my Accesses\n" \
			"Type x to Exit"
		)
		ret = {
			'1': call_userman,
			'2': call_roleman,
			'3': call_resourceman,
			'4': self.accessresource,
			'5': self.viewmyaccesses,
			'x': lambda:"Exit"
		}.get(
			input(
				"App>"
				), lambda:print("Invalid option\nTry Again"))()

		if ret == "Exit":
			print('Bye')
			return
		else:
			self.admin_session ()

	def user_session(self):
		print(
			"Type 1 to Access Resources\n" \
			"Type 2 to View my Accesses\n" \
			"Type x to Exit"
		)
		ret = {
			'1': self.accessresource,
			'2': self.viewmyaccesses,
			'x': lambda:"Exit"
		}.get(
			input(
				"App>"
				), lambda:print("Invalid option\nTry Again"))()

		if ret == "Exit":
			print('Bye')
			return
		else:
			self.user_session()

if __name__ == "__main__":
	MainAppCLI()
