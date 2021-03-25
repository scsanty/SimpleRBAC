##Unit Tests
from SimpleRBAC import SimpleRBAC
class Resource_1:
	def __init__(self, conn):
		self.conn = conn
		self.simplerbac = SimpleRBAC(self.conn)
		self.simplerbac.add_resource_auth_map(__class__.__name__, ['Read', 'Modify', 'Execute'])

	def access_validator(self, uname):
		query = "SELECT " \
			"f.AUTH_NAME " \
			"FROM USER_MASTER a " \
			"LEFT JOIN USER_ROLE_MAP b ON a.ID = b.USER_ID " \
			"LEFT JOIN ROLE_RESOURCE_AUTH_MAP c ON c.ROLE_ID = b.ROLE_ID " \
			"LEFT JOIN ROLE_MASTER d ON d.ID = c.ROLE_ID " \
			"LEFT JOIN RESOURCE_MASTER e ON e.ID = c.RESOURCE_ID " \
			"LEFT JOIN AUTH_MASTER f ON f.ID = c.AUTH_ID " \
			"WHERE a.uname = '" + uname + "' and e.RESOURCE_NAME = '" + str(__class__.__name__).upper() + "';"
		output = self.conn.execute(query).fetchall()
		if output:
			output = [i[0] for i in output]
			print("You have the following accesses to this resource:", ", ".join(output))
		else:
			print("You don't have any authorisations for", __class__.__name__)
	def do_stuffs(self):
		pass

class Resource_2:
	def __init__(self, conn):
		self.conn = conn
		self.simplerbac = SimpleRBAC(self.conn)
		self.simplerbac.add_in_masters('AUTH', 'MODIFY_9', 'Developer defined Custom authorisation for Resource2')
		self.simplerbac.add_resource_auth_map(__class__.__name__, ['Read', 'Modify', 'Execute'])

	def access_validator(self, uname):
		query = "SELECT " \
			"f.AUTH_NAME " \
			"FROM USER_MASTER a " \
			"LEFT JOIN USER_ROLE_MAP b ON a.ID = b.USER_ID " \
			"LEFT JOIN ROLE_RESOURCE_AUTH_MAP c ON c.ROLE_ID = b.ROLE_ID " \
			"LEFT JOIN ROLE_MASTER d ON d.ID = c.ROLE_ID " \
			"LEFT JOIN RESOURCE_MASTER e ON e.ID = c.RESOURCE_ID " \
			"LEFT JOIN AUTH_MASTER f ON f.ID = c.AUTH_ID " \
			"WHERE a.uname = '" + uname + "' and e.RESOURCE_NAME = '" + str(__class__.__name__).upper() + "';"
		output = self.conn.execute(query).fetchall()
		if output:
			output = [i[0] for i in output]
			print("You have the following accesses to this resource:", ", ".join(output))
		else:
			print("You don't have any authorisations for", __class__.__name__)

	def do_stuffs(self):
		pass

class Resource_3:
	def __init__(self, conn):
		self.conn = conn
		self.simplerbac = SimpleRBAC(self.conn)
		self.simplerbac.add_in_masters('AUTH', 'PARTIAL_READ_1', 'Developer defined Custom authorisation for Resource3')
		self.simplerbac.add_in_masters('AUTH', 'PARTIAL_READ_2', 'Developer defined Custom authorisation for Resource3')
		self.simplerbac.add_resource_auth_map(__class__.__name__, ['Read', 'Modify', 'Execute', 'PARTIAL_READ_1', 'PARTIAL_READ_2'])

	def access_validator(self, uname):
		query = "SELECT " \
			"f.AUTH_NAME " \
			"FROM USER_MASTER a " \
			"LEFT JOIN USER_ROLE_MAP b ON a.ID = b.USER_ID " \
			"LEFT JOIN ROLE_RESOURCE_AUTH_MAP c ON c.ROLE_ID = b.ROLE_ID " \
			"LEFT JOIN ROLE_MASTER d ON d.ID = c.ROLE_ID " \
			"LEFT JOIN RESOURCE_MASTER e ON e.ID = c.RESOURCE_ID " \
			"LEFT JOIN AUTH_MASTER f ON f.ID = c.AUTH_ID " \
			"WHERE a.uname = '" + uname + "' and e.RESOURCE_NAME = '" + str(__class__.__name__).upper() + "';"
		output = self.conn.execute(query).fetchall()
		if output:
			output = [i[0] for i in output]
			print("You have the following accesses to this resource:", ", ".join(output))
		else:
			print("You don't have any authorisations for", __class__.__name__)

	def do_stuffs(self):
		pass
