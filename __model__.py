sql_list = [
	'DROP TABLE IF EXISTS id_source',
	f'CREATE TABLE id_source( \
		row_id		INTEGER PRIMARY KEY AUTOINCREMENT, \
		version 	TEXT, \
		batch_key 	BOOLEAN, \
		created_on 	TEXT, \
		created_at 	TEXT \
	)',

	'DROP TABLE IF EXISTS batch_audit',
	f'CREATE TABLE batch_audit( \
		row_id		INTEGER PRIMARY KEY, \
		created_on 	TEXT, \
		created_at 	TEXT \
	)',

	'DROP TABLE IF EXISTS proc_audit',
	f'CREATE TABLE proc_audit( \
		row_id 		INTEGER PRIMARY KEY, \
		batch_id 	INTEGER, \
		proc_action	INTEGER, \
		created_on 	TEXT, \
		created_at 	TEXT \
	)',

	'DROP TABLE IF EXISTS proc_action',
	f'CREATE TABLE proc_action( \
		row_id		INTEGER PRIMARY KEY AUTOINCREMENT, \
		action 		TEXT \
	)',

	'DROP TABLE IF EXISTS proc_status',
	f'CREATE TABLE proc_status( \
		row_id		INTEGER PRIMARY KEY AUTOINCREMENT, \
		status 		TEXT \
	)',

	'DROP TABLE IF EXISTS etl_audit',
	f'CREATE TABLE etl_audit( \
		row_id		INTEGER PRIMARY KEY AUTOINCREMENT, \
		batch_id 	INTEGER, \
		proc_id 	INTEGER, \
		line_id		INTEGER, \
		status_id 	INTEGER, \
		updated_on 	TEXT, \
		updated_at 	TEXT \
	)',

	'DROP TABLE IF EXISTS etl_outcome',
	f'CREATE TABLE etl_outcome( \
		row_id		INTEGER PRIMARY KEY AUTOINCREMENT, \
		etl_id 		INTEGER, \
		message 	INTEGER, \
		created_on 	TEXT, \
		created_at 	TEXT \
	)',

	'DROP TABLE IF EXISTS outcome_messages',
	f'CREATE TABLE outcome_messages( \
		row_id		INTEGER PRIMARY KEY AUTOINCREMENT, \
		message 	TEXT \
	)',

	f'INSERT INTO proc_status(status) VALUES \
	(\'PENDING\'), \
	(\'ERROR\'), \
	(\'SKIPPED\'), \
	(\'COMPLETE\')',

	f'INSERT INTO outcome_messages(message) VALUES \
	(\'MATCH\'), \
	(\'NO MATCH\'), \
	(\'SUGGEST A CORRECTION\')',
]