import hashlib
import sqlite3

def dummy_data_init(conn):
	conn.execute("insert into USER_MASTER (FNAME, LNAME, USER_NAME, PASSWORD) values " \
		f"('Basic', 'USER', 'BUSER00', '{hashlib.sha256('pass'.encode()).hexdigest()}')," \
		f"('DUMMY', 'USER1', 'DUSER01', '{hashlib.sha256('dummypass'.encode()).hexdigest()}')," \
		f"('DUMMY', 'USER2', 'DUSER02', '{hashlib.sha256('dummypass'.encode()).hexdigest()}')," \
		f"('DUMMY', 'USER3', 'DUSER03', '{hashlib.sha256('dummypass'.encode()).hexdigest()}')," \
		f"('DUMMY', 'USER4', 'DUSER04', '{hashlib.sha256('dummypass'.encode()).hexdigest()}')," \
		f"('DUMMY', 'USER5', 'DUSER05', '{hashlib.sha256('dummypass'.encode()).hexdigest()}')," \
		f"('DUMMY', 'USER6', 'DUSER06', '{hashlib.sha256('dummypass'.encode()).hexdigest()}')," \
		f"('DUMMY', 'USER7', 'DUSER07', '{hashlib.sha256('dummypass'.encode()).hexdigest()}')," \
		f"('DUMMY', 'USER8', 'DUSER08', '{hashlib.sha256('dummypass'.encode()).hexdigest()}');")

	conn.execute("insert into ROLE_MASTER (ROLE_NAME, DESCRIPTION) values " \
		"('ROLE_1', 'Dummy Role 1')," \
		"('ROLE_2', 'Dummy Role 2')," \
		"('ROLE_3', 'Dummy Role 3');")

	conn.execute("insert into RESOURCE_MASTER (RESOURCE_NAME, DESCRIPTION) values " \
		"('RESOURCE_1', 'Dummy Resource 1')," \
		"('RESOURCE_2', 'Dummy Resource 1')," \
		"('RESOURCE_3', 'Dummy Resource 1');")

	conn.execute("insert into AUTH_MASTER (AUTH_NAME, DESCRIPTION) values " \
		"('READ', 'Read Access to a resource')," \
		"('MODIFY', 'Modify Access to a resource (Text, fields)')," \
		"('EXECUTE', 'Access to Execute a resource(scripts/functions)')," \
		"('MODIFY_9', 'Developer defined Custom authorisation')," \
		"('PARTIAL_READ_1', 'Developer defined Custom authorisation')," \
		"('PARTIAL_READ_2', 'Developer defined Custom authorisation');")

	conn.execute("insert into USER_ROLE_MAP (USER_ID, ROLE_ID) values " \
		"(2, 1)," \
		"(2, 2)," \
		"(3, 1)," \
		"(4, 3)," \
		"(5, 1)," \
		"(5, 2)," \
		"(5, 3)," \
		"(6, 2)," \
		"(7, 2)," \
		"(8, 1)," \
		"(9, 3)," \
		"(10, 2);")

	conn.execute("insert into ROLE_RESOURCE_AUTH_MAP (ROLE_ID, RESOURCE_ID, AUTH_ID) values " \
		"(1, 1, 1)," \
		"(1, 1, 2)," \
		"(1, 1, 3)," \
		"(1, 3, 3)," \
		"(1, 3, 5)," \
		"(1, 3, 6)," \
		"(2, 3, 3)," \
		"(2, 3, 5)," \
		"(2, 2, 1)," \
		"(2, 2, 3)," \
		"(3, 3, 5)," \
		"(3, 1, 1)," \
		"(3, 2, 1)," \
		"(3, 3, 3);")

	conn.execute("insert into RESOURCE_AUTH_MAP (RESOURCE_ID, AUTH_ID) values " \
		"(1, 1)," \
		"(1, 2)," \
		"(1, 3)," \
		"(1, 4)," \
		"(2, 1)," \
		"(2, 3)," \
		"(3, 3)," \
		"(3, 5)," \
		"(3, 6);")

	conn.commit()
