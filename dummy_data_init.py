import hashlib
import sqlite3

def dummy_data_init(conn):
	conn.execute("insert into USER_MASTER (FNAME, LNAME, UNAME, PASSWORD, ROLE_ID) values " \
		f"('Basic', 'USER', 'BUSER00', '{hashlib.sha256('pass'.encode()).hexdigest()}', 1)," \
		f"('DUMMY', 'USER1', 'DUSER01', '{hashlib.sha256('dummypass'.encode()).hexdigest()}', 1)," \
		f"('DUMMY', 'USER2', 'DUSER02', '{hashlib.sha256('dummypass'.encode()).hexdigest()}', 3)," \
		f"('DUMMY', 'USER3', 'DUSER03', '{hashlib.sha256('dummypass'.encode()).hexdigest()}', 2)," \
		f"('DUMMY', 'USER4', 'DUSER04', '{hashlib.sha256('dummypass'.encode()).hexdigest()}', 2)," \
		f"('DUMMY', 'USER5', 'DUSER05', '{hashlib.sha256('dummypass'.encode()).hexdigest()}', 3)," \
		f"('DUMMY', 'USER6', 'DUSER06', '{hashlib.sha256('dummypass'.encode()).hexdigest()}', 3)," \
		f"('DUMMY', 'USER7', 'DUSER07', '{hashlib.sha256('dummypass'.encode()).hexdigest()}', 3)," \
		f"('DUMMY', 'USER8', 'DUSER08', '{hashlib.sha256('dummypass'.encode()).hexdigest()}', 2);")

	conn.execute("insert into ROLE_MASTER (ROLE_NAME) values " \
		f"('ROLE_1')," \
		f"('ROLE_2')," \
		f"('ROLE_3');")

	conn.execute("insert into RESOURCE_MASTER (RESOURCE_NAME) values " \
		f"('RESOURCE_1')," \
		f"('RESOURCE_2')," \
		f"('RESOURCE_3');")

	conn.execute("insert into AUTH_MASTER (AUTH_NAME, DESCRIPTION) values " \
		f"('READ', 'Read Access to a resource')," \
		f"('READ', 'Read Access to a resource')," \
		f"('MODIFY', 'Modify Access to a resource (Text, fields)')," \
		f"('EXECUTE', 'Access to Execute a resource(scripts/functions)')," \
		f"('MODIFY_9', 'Developer defined Custom authorisation')," \
		f"('PARTIAL_READ_1', 'Developer defined Custom authorisation')," \
		f"('PARTIAL_READ_2', 'Developer defined Custom authorisation');")

	conn.commit()
