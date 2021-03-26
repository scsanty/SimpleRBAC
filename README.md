# Bluestacks Assignment

## Master Tables
### USER_MASTER

| ID | FNAME | LNAME | UNAME   | PASSWORD  |                                                                |
|----|-------|-------|---------|-----------|----------------------------------------------------------------|
| 1  | ADMIN | ADMIN | ADMIN   | ADMIN     | <-- Added by MainApp.py Program                                |
| 2  | BASIC | USER  | USER01  | pass      | <-- This and below, Added for Unit test via dummy_data_init.py |
| 3  | DUMMY | USER1 | DUSER01 | dummypass |                                                                |
| 4  | DUMMY | USER2 | DUSER02 | dummypass |                                                                |
| 5  | DUMMY | USER3 | DUSER03 | dummypass |                                                                |
| 6  | DUMMY | USER4 | DUSER04 | dummypass |                                                                |
| 7  | DUMMY | USER5 | DUSER05 | dummypass |                                                                |
| 8  | DUMMY | USER6 | DUSER06 | dummypass |                                                                |
| 9  | DUMMY | USER7 | DUSER07 | dummypass |                                                                |
| 10 | DUMMY | USER8 | DUSER08 | dummypass |                                                                |


### ROLE_MASTER
Added for Unit test via dummy_data_init.py
| ID | ROLE_NAME | DESCRIPTION  |
|----|-----------|--------------|
| 1  | ROLE_1    | Dummy Role 1 |
| 2  | ROLE_2    | Dummy Role 2 |
| 3  | ROLE_3    | Dummy Role 3 |

### RESOURCE_MASTER
Added for Unit test via dummy_data_init.py
| ID | RESOURCE_NAME | DESCRIPTION      |
|----|---------------|------------------|
| 1  | RESOURCE_1    | Dummy Resource 1 |
| 2  | RESOURCE_2    | Dummy Resource 2 |
| 3  | RESOURCE_3    | Dummy Resource 3 |

### AUTH_MASTER
Added for Unit test via dummy_data_init.py
| ID | AUTH_NAME      | DESCRIPTION                                     |
|----|----------------|-------------------------------------------------|
| 1  | READ           | Read Access to a resource                       |
| 2  | MODIFY         | Modify Access to a resource (Text, fields)      |
| 3  | EXECUTE        | Access to Execute a resource(scripts/functions) |
| 4  | MODIFY_9       | Developer defined Custom authorisation          |
| 5  | PARTIAL_READ_1 | Developer defined Custom authorisation          |
| 6  | PARTIAL_READ_2 | Developer defined Custom authorisation          |

## Mapping Tables
### USER_ROLE_MAP
Added for Unit test via dummy_data_init.py
| ID | USER_ID | ROLE_ID |
|----|---------|---------|
| 1  | 1       | 0       |
| 2  | 2       | 1       |
| 3  | 2       | 2       |
| 4  | 3       | 1       |
| 5  | 4       | 3       |
| 6  | 5       | 1       |
| 7  | 5       | 2       |
| 8  | 5       | 3       |
| 9  | 6       | 2       |
| 10 | 7       | 2       |
| 11 | 8       | 1       |
| 12 | 9       | 3       |
| 13 | 10      | 2       |

### ROLE_RESOURCE_AUTH_MAP
| ID | ROLE_ID | RESOURCE_ID | AUTH_ID |
|----|---------|-------------|---------|
| 1  | 1       | 1           | 1       |
| 2  | 1       | 1           | 2       |
| 3  | 1       | 1           | 3       |
| 4  | 1       | 3           | 3       |
| 5  | 1       | 3           | 5       |
| 6  | 1       | 3           | 6       |
| 7  | 2       | 3           | 3       |
| 8  | 2       | 3           | 5       |
| 9  | 2       | 2           | 1       |
| 10 | 2       | 2           | 3       |
| 11 | 3       | 3           | 5       |
| 12 | 3       | 1           | 1       |
| 13 | 3       | 2           | 1       |
| 14 | 3       | 3           | 3       |

### RESOURCE_AUTH_MAP
| ID | RESOURCE_ID | AUTH_ID |
|----|-------------|---------|
| 1  | 1           | 1       |
| 2  | 1           | 2       |
| 3  | 1           | 3       |
| 4  | 1           | 4       |
| 5  | 2           | 1       |
| 6  | 2           | 3       |
| 7  | 3           | 3       |
| 8  | 3           | 5       |
| 9  | 3           | 6       |

## Classes
1) SimpleRBAC - Manages Roles, Authorisation, Resources
2) UserManagement - Manages Users
3) MainAppCLI - CLI of the App
4) Resources - Custom developments on the App (Consider as Unit Test)

## Libraries Used
sqlite3 - to persist the above tables in a RDBMS  
hashlib - to store the password after encrypting it  
getpass - to hide the password when logging in  
os - to run screen clear function  
tabulate - to print the tables in a pretty manner  
  
## Default ID/Pass
ADMIN ADMIN

## How to use:
1) Start at MainApp.py
2) You'll need to log in
3) You can register your resources
4) You can define new role
5) You can map authrisations to your role
6) You can map users to your roles
7) Resources' __init__ handles the possible authorisations it has


