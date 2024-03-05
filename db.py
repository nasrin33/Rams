# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------
# AppConfig configuration made easy. Look inside private/appconfig.ini
# Auth is for authenticaiton and access control
# -------------------------------------------------------------------------
from gluon.contrib.appconfig import AppConfig
from gluon.tools import Auth

# -------------------------------------------------------------------------
# This scaffolding model makes your app work on Google App Engine too
# File is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

if request.global_settings.web2py_version < "2.15.5":
    raise HTTP(500, "Requires web2py 2.15.5 or newer")

# -------------------------------------------------------------------------
# if SSL/HTTPS is properly configured and you want all HTTP requests to
# be redirected to HTTPS, uncomment the line below:
# -------------------------------------------------------------------------
# request.requires_https()

# -------------------------------------------------------------------------
# once in production, remove reload=True to gain full speed
# -------------------------------------------------------------------------
configuration = AppConfig(reload=True)

if not request.env.web2py_runtime_gae:
    # ---------------------------------------------------------------------
    # if NOT running on Google App Engine use SQLite or other DB
    # ---------------------------------------------------------------------
#     db = DAL(configuration.get('db.uri'),
#              pool_size=configuration.get('db.pool_size'),
#              migrate_enabled=configuration.get('db.migrate'),
#              check_reserved=['all'])
    db = DAL('mysql://root:@localhost/payroll', fake_migrate = True)
#     db = DAL('mysql://root:@localhost/payroll_new', migrate_enabled= True)

else:
    # ---------------------------------------------------------------------
    # connect to Google BigTable (optional 'google:datastore://namespace')
    # ---------------------------------------------------------------------
    db = DAL('google:datastore+ndb')
    # ---------------------------------------------------------------------
    # store sessions and tickets there
    # ---------------------------------------------------------------------
    session.connect(request, response, db=db)
    # ---------------------------------------------------------------------
    # or store session in Memcache, Redis, etc.
    # from gluon.contrib.memdb import MEMDB
    # from google.appengine.api.memcache import Client
    # session.connect(request, response, db = MEMDB(Client()))
    # ---------------------------------------------------------------------

# -------------------------------------------------------------------------
# by default give a view/generic.extension to all actions from localhost
# none otherwise. a pattern can be 'controller/function.extension'
# -------------------------------------------------------------------------
response.generic_patterns = [] 
if request.is_local and not configuration.get('app.production'):
    response.generic_patterns.append('*')

# -------------------------------------------------------------------------
# choose a style for forms
# -------------------------------------------------------------------------
response.formstyle = 'bootstrap4_inline'
response.form_label_separator = ''

# -------------------------------------------------------------------------
# (optional) optimize handling of static files
# -------------------------------------------------------------------------
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

# -------------------------------------------------------------------------
# (optional) static assets folder versioning
# -------------------------------------------------------------------------
# response.static_version = '0.0.0'

# -------------------------------------------------------------------------
# Here is sample code if you need for
# - email capabilities
# - authentication (registration, login, logout, ... )
# - authorization (role based authorization)
# - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
# - old style crud actions
# (more options discussed in gluon/tools.py)
# -------------------------------------------------------------------------

# host names must be a list of allowed host names (glob syntax allowed)
auth = Auth(db, host_names=configuration.get('host.names'))

# -------------------------------------------------------------------------
# create all tables needed by auth, maybe add a list of extra fields
# -------------------------------------------------------------------------
# auth.settings.extra_fields['auth_user'] = []
# auth.define_tables(username=False, signature=False)

# -------------------------------------------------------------------------
# configure email
# -------------------------------------------------------------------------
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else configuration.get('smtp.server')
mail.settings.sender = configuration.get('smtp.sender')
mail.settings.login = configuration.get('smtp.login')
mail.settings.tls = configuration.get('smtp.tls') or False
mail.settings.ssl = configuration.get('smtp.ssl') or False

# -------------------------------------------------------------------------
# configure auth policy
# -------------------------------------------------------------------------
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

# -------------------------------------------------------------------------  
# read more at http://dev.w3.org/html5/markup/meta.name.html               
# -------------------------------------------------------------------------
response.meta.author = configuration.get('app.author')
response.meta.description = configuration.get('app.description')
response.meta.keywords = configuration.get('app.keywords')
response.meta.generator = configuration.get('app.generator')
response.show_toolbar = configuration.get('app.toolbar')

# -------------------------------------------------------------------------
# your http://google.com/analytics id                                      
# -------------------------------------------------------------------------
response.google_analytics_id = configuration.get('google.analytics_id')

# -------------------------------------------------------------------------
# maybe use the scheduler
# -------------------------------------------------------------------------
if configuration.get('scheduler.enabled'):
    from gluon.scheduler import Scheduler
    scheduler = Scheduler(db, heartbeat=configuration.get('scheduler.heartbeat'))

# -------------------------------------------------------------------------
# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.
#
# More API examples for controllers:
#
# >>> db.mytable.insert(myfield='value')
# >>> rows = db(db.mytable.myfield == 'value').select(db.mytable.ALL)
# >>> for row in rows: print row.id, row.myfield
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
# after defining tables, uncomment below to enable auditing
# -------------------------------------------------------------------------
# auth.enable_record_versioning(db)



db.define_table('Client_Type',
                Field('client_type'),
                format="%(client_type)s")

auth = Auth(db)
auth.settings.extra_fields['auth_user'] = [
    Field('client_type', 'reference Client_Type', requires=IS_IN_DB(
        db, db.Client_Type.id, '%(client_type)s')),
    Field('institution_name'),
    Field('email', requires=[IS_NOT_EMPTY(),
                             IS_NOT_IN_DB(db, 'auth_user.email')]),
    Field('phone'),
    Field('address'),
    Field('city'),
    Field('vendor_name'),
    Field('admin', 'integer', default=0),
    Field('url', 'string', default=0),
    Field('parent', 'integer'),
    Field('roles_ref_id', 'integer'),
    Field('block_client', 'string'),
    Field('ext8')]

auth.define_tables(username=True, signature=False)

db.define_table('Units',
                Field('unit_id', 'string'),
                Field('unit_name', 'string'),
                Field('dev_type', 'string'),
                Field('model', 'string'),
                Field('vendor', 'string'),
                Field('latitude', 'string'),
                Field('longitude', 'string'),
                Field('template_capacity', 'integer', default=0),
                Field('login_capacity', 'integer', default=0),
                Field('device_location', 'string'),
                Field('commissioned_date', 'datetime'),
                Field('status', 'integer', default=1),
                Field('message', 'text'),
                Field('no_of_att_log', 'integer'),
                Field('ssid1', 'string'),
                Field('password1', 'string'),
                Field('ssid2', 'string'),
                Field('password2', 'string'),
                Field('sd_date', 'date'),
                Field('ip_type', 'string'),
                Field('ip_address', 'string'),
                Field('gateway', 'string'),
                Field('subnet_mask', 'string'),
                Field('dns_server', 'string')
                )

db.Units.unit_id.requires = [IS_NOT_EMPTY(), IS_NOT_IN_DB(db, 'Units.unit_id')]
db.Units.unit_name.requires = IS_NOT_EMPTY()
db.Units.dev_type.requires = IS_NOT_EMPTY()

db.define_table('Client_Unit',
                Field('client_ref_id', 'reference auth_user'),
                Field('unit_ref_id', 'reference Units')
                )


db.define_table('Users',
                Field('registration_id', 'string', requires=IS_NOT_EMPTY()),
                Field('reg_without_zero', 'integer'),
                Field('user_name', 'string', requires=IS_NOT_EMPTY()),
                Field('department', 'string'),
                Field('fp0', 'text'),
                Field('gender','string'),
                Field('fp0_size', 'integer', default=0),
                Field('fp1', 'text'),
                Field('fp1_size', 'integer', default=0),
                Field('face', 'text'),
                Field('retina', 'string'),
                Field('password', 'string'),
                Field('group_no'),
                Field('card', 'string'),
                Field('phone', 'string'),
                Field('email', 'string'),
                Field('fathers_name', 'string'),
                Field('mothers_name', 'string'),
                Field('parents_email', 'string'),
                Field('parents_phone', 'string'),
                Field('address', 'string'),
                Field('class_session', 'string'),
                Field('class_roll', 'text'),
                Field('privilege', 'integer', default=0),
                Field('status', 'string'),
                Field('class_', 'integer', default=1),
                Field('department', 'string'),
                Field('card_mifare_1', 'string'),
                Field('un_assigned', 'integer', default=0),
                Field('deleted', 'integer', default=0),
                Field('assigned_date', 'date'),
                Field('birth_date', 'date'),
                Field('minfp1', 'text'),
                Field('minfp2', 'text'),
                Field('mobile_id', 'string')
                )


db.define_table('Client_Users',
                Field('client_ref_id', 'reference auth_user'),
                Field('user_ref_id', 'reference Users')
                )

db.define_table('Unit_Users',
                Field('unit_ref_id', 'reference Units'),
                Field('user_ref_id', 'reference Users'),
                Field('access_type', 'string',
                      requires=IS_NOT_EMPTY(), notnull=True)
                )
"""
                Field('unit_ref_id', 'reference Units'),
                Field('user_ref_id', 'reference Users'),
"""
db.define_table('temp_fifty_buffer',
                Field('unit_ref_id', 'reference Units'),
                Field('user_ref_id', 'reference Users'))

db.define_table('Access_Log',
                Field('unit_ref_id', 'reference Units'),
                Field('user_ref_id', 'reference Users'),
                Field('access_date', 'date', requires=IS_NOT_EMPTY()),
                Field('access_time', 'time', requires=IS_NOT_EMPTY()),
                Field('verified', 'integer', default=0),
                Field('status', 'integer', default=0),
                Field('workcode', 'integer', default=0),
                Field('in_out','string'),
                Field('info', 'string'),
                Field('note', 'string'),
                Field('access_datetime', 'datetime'),
                Field('ext4'),
                Field('ext5'),
                Field('ext6'),
                Field('ext7'),
                Field('ext8'),
                Field('ext12'),
                Field('ext13'),
                Field('ext14'),
                Field('ext15'),
                Field('ext16'),
                Field('sms_status', 'string')
                )
db.define_table('Last_Attended',
                Field('user_ref_id', 'reference Users'),
                Field('attend_date', 'date', requires=IS_NOT_EMPTY()),
                Field('attend_time', 'time', requires=IS_NOT_EMPTY()),
                Field('in_out','string'),
                Field('ext1')
                )




db.define_table('Student_Holidays',
               Field('user_ref_id', 'reference Users'),
               Field('holiday', 'date', requires=IS_NOT_EMPTY()),
               Field('description', 'string'),
               Field('client_ref_id', 'reference auth_user'),
               Field('pay_status', 'integer', default=0),
               Field('leave_type', 'string'),
               Field('leave_status', 'string')
                )

db.define_table('Government_Holiday',
                Field('holiday', 'date', requires=IS_NOT_EMPTY()),
                Field('description', 'string'),
                Field('client_ref_id', 'reference auth_user')
                )

db.define_table('Variables',
                Field('leave_id', 'integer', default=1),
                Field('absent_id', 'integer', default=1),
                Field('ext1'),
                Field('ext2'),
                Field('ext3'),
                Field('ext4'),
                Field('ext5'),
                Field('ext6'),
                Field('ext7'),
                Field('ext8'))

db.define_table('Leave_Granted',
                Field('client_ref_id', 'reference auth_user'),
                Field('user_ref_id', 'reference Users'),
                Field('leave_id', 'integer', requires=IS_NOT_EMPTY()),
                Field('start_date', 'date', requires=IS_NOT_EMPTY()),
                Field('end_date', 'date', requires=IS_NOT_EMPTY()),
                Field('grant_date', 'date', requires=IS_NOT_EMPTY()),
                Field('grant_time', 'time', requires=IS_NOT_EMPTY()),
                Field('ext3'),
                Field('ext4'),
                Field('ext5'),
                Field('ext6'),
                Field('ext7'),
                Field('ext8')
                )
# db.executesql("CREATE INDEX IF NOT EXISTS leaveIndex ON Leave_Granted (client_ref_id, user_ref_id)")

db.define_table('Leave_User',
                Field('client_ref_id', 'reference auth_user'),
                Field('user_ref_id', 'reference Users'),
                Field('leave_id', 'integer', requires=IS_NOT_EMPTY()),
                Field('leave_date', 'date', requires=IS_NOT_EMPTY()),
                Field('grant_date', 'date', requires=IS_NOT_EMPTY()),
                Field('grant_time', 'time', requires=IS_NOT_EMPTY()),
                Field('ext3'),
                Field('ext4'),
                Field('ext5'),
                Field('ext6'),
                Field('ext7'),
                Field('ext8')
                )
# db.executesql("CREATE INDEX IF NOT EXISTS leaveUserIndex ON Leave_User (client_ref_id, user_ref_id)")

db.define_table('Absent_Count',
                Field('absent_id', 'integer', requires=IS_NOT_EMPTY()),
                Field('user_ref_id', 'reference Users'),
                Field('absent_days', 'date', requires=IS_NOT_EMPTY()),
                Field('consecutive_count', 'integer', default=0),
                Field('ext1'),
                Field('ext2'),
                Field('ext3'),
                Field('ext4'),
                Field('ext5'),
                Field('ext6'),
                Field('ext7'),
                Field('ext8'))

# db.executesql("CREATE INDEX IF NOT EXISTS abCountIndex ON Absent_Count (absent_id, user_ref_id)")

db.define_table('Absent_Query',
                Field('client_ref_id', 'reference auth_user'),
                Field('user_ref_id', 'reference Users'),
                Field('absent_date', 'date', requires=IS_NOT_EMPTY()),
                Field('consecutive_days', 'integer', requires=IS_NOT_EMPTY()),
                Field('ext1'),
                Field('ext2'),
                Field('ext3'),
                Field('ext4'),
                Field('ext5'),
                Field('ext6'),
                Field('ext7'),
                Field('ext8'))
# db.executesql("CREATE INDEX IF NOT EXISTS abQueryIndex ON Absent_Query (client_ref_id, user_ref_id)")


db.define_table('semester',
                Field('client_ref_id', 'reference auth_user', ondelete='CASCADE'),
                Field('semester_name', 'string', requires=IS_NOT_EMPTY()),
                Field('start_date', 'date', requires=IS_NOT_EMPTY()),
                Field('end_date', 'date', requires=IS_NOT_EMPTY()),
                Field('description', 'string')
                )

db.define_table('semester_students',
                Field('semester_ref_id', 'reference semester', ondelete='CASCADE'),
                Field('user_ref_id', 'reference Users', ondelete='CASCADE'))

db.define_table('courses',
                Field('client_ref_id', 'reference auth_user', ondelete='CASCADE'),
                Field('course_name', 'string', requires=IS_NOT_EMPTY()),
                Field('course_code', 'string', default=''),
                Field('course_credit', 'string', default='0'))

# db.define_table('semester_courses',
#                 Field('semester_ref_id', 'reference semester', ondelete='CASCADE'),
#                 Field('course_ref_id', 'reference courses', ondelete='CASCADE'))


db.define_table('course_assoc_students',
                Field('course_ref_id', 'reference courses', ondelete='CASCADE'),
                Field('user_ref_id', 'reference Users', ondelete='CASCADE'))


db.define_table('routine',
                Field('client_ref_id', 'reference auth_user', ondelete='CASCADE'),
                Field('unit_ref_id', 'reference Units', ondelete='CASCADE'),
                Field('semester_ref_id', 'reference semester', ondelete='CASCADE'),
                Field('course_ref_id', 'reference courses', ondelete='CASCADE'),
                Field('week_day', 'string'),
                Field('time_in', 'time'),
                Field('time_out', 'time'))

db.define_table('students_attendance',
                Field('user_ref_id', 'reference Users', ondelete='CASCADE'),
                Field('semester_ref_id', 'reference semester', ondelete='CASCADE'),
                Field('course_ref_id', 'reference courses', ondelete='CASCADE'),
                Field('year', 'string'),
                Field('date', 'date', requires=IS_NOT_EMPTY()))

db.define_table('cron_job',
                Field('request_date', 'date', requires=IS_NOT_EMPTY()),
                Field('request_time', 'time', requires=IS_NOT_EMPTY()),
                Field('job', 'string'),
                Field('ext2'),
                Field('ext3'),
                Field('ext4'),
                Field('ext5'),
                Field('ext6'),
                Field('ext7'),
                Field('ext8'))


db.define_table('Json_data',
                Field('json_data', 'text'))

db.define_table('User_Info',
                Field('user_id', 'string', requires=IS_NOT_EMPTY()),
                Field('user_name', 'string', requires=IS_NOT_EMPTY()),
                Field('department', 'string'),
                Field('fp0', 'text', requires=IS_NOT_EMPTY()),
                Field('fp0_size', 'integer'),
                Field('fp1', 'text', requires=IS_NOT_EMPTY()),
                Field('fp1_size', 'integer'),
                Field('face', 'string'),
                Field('retina', 'string'),
                Field('password', 'string'),
                Field('group_no'),
                Field('card', 'string'),
                Field('phone'),
                Field('email'),
                Field('fathers_name'),
                Field('mothers_name'),
                Field('parents_email'),
                Field('parents_phone'),
                Field('address'),
                Field('class_session'),
                Field('classroll'),
                Field('privilege', 'integer'),
                Field('status'))


db.define_table('Users_Log',
                Field('unit_id', 'string', requires=IS_NOT_EMPTY()),
                Field('user_id', 'string', requires=IS_NOT_EMPTY()),
                Field('access_date', 'string', requires=IS_NOT_EMPTY()),
                Field('access_time', 'string', requires=IS_NOT_EMPTY()),
                Field('verified'),
                Field('status'),
                Field('workcode')
                )


db.define_table('third_party',
                Field('user_name', 'string'),
                Field('auth', 'string'))


db.define_table('client_third_party',
                Field('auth_user_id', 'reference auth_user'),
                Field('third_party_id', 'reference third_party'))


db.define_table('log_time',
                Field('device_id', 'text'),
                Field('reset_cause', 'text'),
                Field('current_time_', 'text'),
                Field('reset_cause_core_0', 'string'),
                Field('reset_cause_core_1', 'string')
                )


db.define_table('log_time1',
                Field('dumpjson')
                )

db.define_table('image',
                Field('title'),
                Field('file', 'upload'),
                format='%(title)s')

db.define_table('Firmware',
                Field('title'),
                Field('file', 'upload'),
                format='%(title)s')

db.define_table('replace_devices',
                Field('previousUnit'),
                Field('previous_unit_id', 'integer'),
                Field('newUnit'),
                Field('new_unit_id', 'integer'),
                Field('transfer_status')
                )

db.define_table('deleted_user',
                Field('user_ref_id', 'integer'),
                Field('unit_ref_id', 'integer')
                )

db.define_table('dump_json',
                Field('dumpjson')
                )

db.define_table('User_Info_test_csv_temp',
                Field('user_id', 'string', requires=IS_NOT_EMPTY()),
                #Field('reg_without_zero', 'string'),
                Field('user_name', 'string', requires=IS_NOT_EMPTY()),
                Field('department', 'string'),
                Field('fp0', 'text', requires=IS_NOT_EMPTY()),
                Field('fp0_size', 'integer'),
                Field('fp1', 'text', requires=IS_NOT_EMPTY()),
                Field('fp1_size'),
                Field('face', 'string'),
                Field('retina', 'string'),
                Field('password', 'string'),
                Field('group_no'),
                Field('card', 'text'),
                Field('phone'),
                Field('email'),
                Field('fathers_name'),
                Field('mothers_name'),
                Field('parents_email'),
                Field('parents_phone'),
                Field('address'),
                Field('class_session'),
                Field('classroll', 'text'),
                Field('privilege', 'integer'),
                Field('status'),
                Field('client_ref_id'),
                Field('unit_ref_id'))

db.define_table('User_Info_test_csv_temp_test_card_no',
                Field('card_no_1', 'integer', requires=IS_NOT_EMPTY()),
                Field('card_no_2', 'integer', requires=IS_NOT_EMPTY()),
                Field('registration_id', 'text', requires=IS_NOT_EMPTY()),
                Field('user_name', 'string'),
                Field('phone'),
                Field('email'),
                Field('fathers_name'),
                Field('mothers_name'),
                Field('parents_email'),
                Field('parents_phone'),
                Field('address'),
                Field('class_session'),
                Field('client_ref_id'),
                Field('unit_ref_id'))

db.define_table('log_time_test',
                Field('device_id', 'text'),
                Field('reset_cause', 'text'),
                Field('current_time', 'datetime'))

db.define_table('scan_card',
                Field('unit_id', 'text'),
                Field('card_finger', 'text'),
                Field('ready_mode', 'integer', default=0))


db.define_table('unit_type',
                Field('unit_id', 'string'),
                Field('type', 'string'))

db.define_table('Unit_Class',
                Field('unit_class_name', 'string')
                )


db.define_table('Ota_Firmware_Lists',
                Field('unit_class_ref_id', 'reference Unit_Class'),
                Field('version', 'string'),
                Field('file_name', 'string')
                )
db.define_table('Manufactured_device',
                Field('device_id'),
                Field('unit_class_ref_id', 'reference Unit_Class'),
                Field('manufacture_date', 'datetime'),
                Field('wifi'),
                Field('pcb'),
                Field('micro_controller'),
                Field('model'),
                Field('casing_type'),
                Field('RSSI'),
                Field('assembler', 'string')
                )

db.define_table('Manufacture_Unit',
                Field('manufactured_device_ref_id',
                      'reference Manufactured_device'),
                Field('unit_ref_id', 'reference Units')
                )

db.define_table('Device_History',
                Field('unit_ref_id', 'reference Units'),
                Field('history_date', 'datetime'),
                Field('problem', 'text'),
                Field('solution', 'text')
                )

db.define_table('Casing_Type',
                Field('name')
                )

db.define_table('pull_registry',
                Field('unit_ref_id', 'reference Units'),
                Field('card')
                )

db.define_table('rec_size',
                Field('unit_ref_id', 'reference Units'),
                Field('number_of_rec')
                )

db.define_table('Unit_Firmware_Version',
                Field('unit_ref_id', 'reference Units'),
                Field('current_firmware_version')
                )

db.define_table('Debug_Log',
                Field('unit_ref_id', 'reference Units'),
                Field('value', 'integer'),
                Field('debug_state'),
                Field('record_time', 'datetime')
                )

db.define_table('Reset_Rec',
                Field('unit_ref_id', 'reference Units'),
                Field('state', 'integer')
                )

db.define_table('Messages',
                Field('unit_ref_id', 'reference Units'),
                Field('warning'),
                Field('expire'),
                Field('regular'),
                Field('welcome'),
                Field('background_color', 'string'),
                Field('font_color', 'string'),
                Field('zk_ip', 'string'),
                Field('port', 'string'),
                Field('display_type', 'string')
                )

db.define_table('Unit_Messages',
                Field('unit_ref_id', 'reference Units'),
                Field('message_ref_id', 'reference Messages')
                )

db.define_table('Billing',
                Field('unit_ref_id', 'reference Units'),
                Field('expiry_date', 'datetime'),
                Field('status', 'integer')
                )
db.define_table('Daily_Schedules',
               Field('day_name','string',requires=IS_NOT_EMPTY()),
               Field('time','string'),
               Field('subject','string'),
               Field('subject_code','string'),
               Field('batch_name','string'),
               Field('teacher_name','string'),
               Field('department','string'),
               Field('admin_name','string'),
               Field('room_name','string')
                )

db.define_table('Room_Lists',
               Field('room_name','string',requires=IS_NOT_EMPTY()),
               Field('day','string'),
               Field('building','string'),
               Field('admin','string'),
               Field('date','date'),
               Field('details','string')
               )

db.define_table('Absent_Logs',
                Field('user_ref_id', 'reference Users', requires=IS_NOT_EMPTY()),
                Field('Date', 'date', requires=IS_NOT_EMPTY())
               )
db.define_table('In_Out_Record',
               Field('unit_ref_id', 'reference Units'),
               Field('user_ref_id', 'reference Users'),
               Field('access_date', 'date', requires=IS_NOT_EMPTY()),
               Field('access_time', 'time', requires=IS_NOT_EMPTY()),
               Field('in_time', 'time', requires=IS_NOT_EMPTY()),
               Field('out_time', 'time',default='00:00:00'),
               Field('verified', 'integer', default=0),
               Field('status', 'integer', default=0),
               Field('workcode', 'integer', default=0),
               Field('in_out','string')
               )
db.define_table('Device_Models',
               Field('Model_No', 'string'),
               Field('Sensor_Types', 'string'),
               Field('Main_Processor', 'string'),
               Field('Display', 'string'),
               Field('Power_Cable', 'string'),
               Field('Model_Type', 'string'),
               Field('ext2'),
               Field('ext3'),
               Field('ext4'),
               Field('ext5'),
               Field('ext6'),
               Field('ext7'),
               )
db.define_table('Classes',
               Field('Client_Ref_ID', 'reference auth_user'),
               Field('Name', 'string', requires=IS_NOT_EMPTY()),
               Field('Section', 'string'),
               Field('in_time','time',requires=IS_NOT_EMPTY()),
               Field('out_time','time',requires=IS_NOT_EMPTY())
               )
db.define_table('Regular_Alarm',
                Field('client_ref_id', 'reference auth_user'),
                Field('alarm_time'),
                Field('alarm_duration'),
                Field('alarm_day'),
                Field('duration_time'),
                Field('day_name'),
                Field('alarm_status'),
                Field('confirm_status'),
                Field('unit_ref_id', 'reference Units'),
                Field('ext6'),
                Field('ext7'),
                Field('ext8'),
                )
db.define_table('Special_Alarm',
                Field('client_ref_id', 'reference auth_user'),
                Field('alarm_time'),
                Field('alarm_duration'),
                Field('alarm_date'),
                Field('duration_time'),
                Field('alarm_status'),
                Field('confirm_status'),
                Field('unit_ref_id', 'reference Units'),
                Field('ext6'),
                Field('ext7'),
                Field('ext8'),
                )
db.define_table('Deleted_Users',
                Field('user_ref_id', 'integer', requires=IS_NOT_EMPTY()),
                Field('registration_id', 'string', requires=IS_NOT_EMPTY()),
                Field('card', 'string'),
                Field('card_mifare_1', 'string'),
                Field('fp0' 'text'),
                Field('fp1', 'text'),
                Field('deleted_date', 'date'),
                Field('client_ref_id', 'reference auth_user', requires=IS_NOT_EMPTY()),
                Field('ext6'),
                Field('ext7'),
                Field('ext8'),
                Field('ext9'),
                Field('ext10'),
                Field('ext11'),
                Field('ext12')
                )
db.define_table('Unit_History',
                Field('client_ref_id', 'reference auth_user'),
                Field('delete_time', 'datetime'),
                Field('unit_id', 'string'),
                Field('unit_ref_id', 'reference Units'),
                Field('ext5'),
                Field('ext6'),
                Field('ext7'),
                Field('ext8'),
                Field('ext9'),
                Field('ext10'),
                Field('ext11'),
                Field('ext12')
               )
db.define_table('Client_Users_Info',
                Field('client_ref_id', 'reference auth_user'),
                Field('total_user', 'string'),
                Field('total_present', 'string'),
                Field('total_leave', 'string'),
                Field('total_absent', 'string'),
                Field('info_date', 'date'),
                Field('department', 'string'),
                Field('ext8'),
                Field('ext9'),
                Field('ext10'),
                Field('ext11'),
                Field('ext12'),
                Field('ext13'),
                Field('ext14')
                )
db.define_table('Assign_Unit_Vendor',
                Field('client_ref_id', 'reference auth_user'),
                Field('manufacture_ref_id', 'reference Manufactured_device'),
                Field('device_id', 'string'),
                Field('model', 'string'),
                Field('assign_date', 'date'),
                Field('manufacture_date', 'date'),
                Field('status', 'integer'),
                Field('device_bill', 'integer'),
                Field('free_period', 'date'),
                Field('total_bill', 'string'),
                Field('bill_due', 'string'),
                Field('last_paid', 'date'),
                Field('payment_status', 'string'),
                Field('bill_update', 'date'),
                Field('return_date', 'date'),
                Field('ext16'),
                Field('ext17'),
                Field('ext18')
                )
db.define_table('Bill_Due',
                Field('client_ref_id', 'reference auth_user'),
                Field('manufacture_ref_id', 'reference Manufactured_device'),
                Field('due_date', 'date'),
                Field('amount', 'string'),
                Field('month_name', 'string'),
                Field('status', 'integer', default=0),
                Field('ext7'),
                Field('ext8'),
                Field('ext9'),
                Field('ext10'),
                Field('ext11'),
                Field('ext12')
                )
db.define_table('Unit_Wifi_Status',
                Field('unit_id', 'string'),
                Field('unit_ref_id', 'reference Units'),
                Field('green', 'string'),
                Field('yellow', 'string'),
                Field('red', 'string'),
                Field('record_date', 'date'),
                Field('record_time', 'time'),
                Field('ext8'),
                Field('ext9'),
                Field('ext10'),
                Field('ext11'),
                Field('ext12'),
                Field('ext13')
                )
db.define_table('Stress_Test_Report',
                Field('unit_id', 'string'),
                Field('flash_size', 'string'),
                Field('rtc_available', 'string'),
                Field('rtc_status', 'string'),
                Field('rec_size', 'string'),
                Field('clone_date', 'date'),
                Field('clone_time', 'string'),
                Field('rdm_status', 'string'),
                Field('memory_full_time', 'time'),
                Field('eeprom_status', 'string'),
                Field('comment_address', 'string'),
                Field('current_log_address', 'string'),
                Field('unsent_log_start_address', 'string'),
                Field('firmware_version', 'string'),
                Field('rssi', 'string'),
                Field('ssid', 'string'),
                Field('password', 'string'),
                Field('report_time', 'time'),
                Field('memory_full_time1', 'string'),
                Field('report_date_time', 'datetime'),
                Field('row_color', 'string')
                )
db.define_table('Deactive_Device',
                Field('unit_id', 'string'),
                Field('manufacture_ref_id', 'integer', default=0),
                Field('deactive_date', 'datetime'),
                Field('client_ref_id', 'integer', default=0),
                Field('status', 'integer', default=0),
                Field('ext6'),
                Field('ext7'),
                Field('ext8'),
                Field('ext9'),
                Field('ext10'),
                Field('ext11'),
                Field('ext12')
                )
db.define_table('Updated_Client',
                Field('client_ref_id', 'reference auth_user'),
                Field('password', 'string'),
                Field('change_date', 'datetime'),
                Field('client_name', 'string'),
                Field('ext7'),
                Field('ext8'),
                Field('ext9'),
                Field('ext10'),
                Field('ext11'),
                Field('ext12')
                )
db.define_table('HR_Info',
                Field('client_ref_id', 'reference auth_user'),
                Field('user_ref_id', 'reference Users', ondelete='CASCADE'),
                Field('reg_id', 'string'),
                Field('assign_date', 'datetime'),
                Field('salary', 'string'),
                Field('in_time', 'time'),
                Field('out_time', 'time'),
                Field('time_diff', 'integer'),
                Field('ext10'),
                Field('ext11'),
                Field('ext12'),
                Field('ext13'),
                Field('ext14'),
                Field('ext15')
                )
db.define_table('User_Image',
                Field('client_ref_id', 'reference auth_user'),
                Field('user_ref_id', 'reference Users', ondelete='CASCADE'),
                Field('registration_id', 'string'),
                Field('image_name', 'string'),
                Field('ext5'),
                Field('ext6'),
                Field('ext7'),
                Field('ext8'),
                Field('ext9'),
                Field('ext10')
                )
db.define_table('lecture_details',
                Field('client_ref_id', 'reference auth_user'),
                Field('course_name', 'string'),
                Field('semester_name', 'string'),
                Field('lecture_date', 'date'),
                Field('teacher_name', 'string'),
                Field('time_slot1', 'time'),
                Field('time_slot2', 'time'),
                Field('device_name', 'string'),
                Field('unit_ref_id', 'reference Units'),
                Field('ext7'),
                Field('ext8'),
                Field('ext9'),
                Field('ext10')
                )
db.define_table('District_List',
                Field('district_name', 'string'),
                Field('ext2'),
                Field('ext3'),
                Field('ext4'),
                Field('ext5'),
                Field('ext6'),
                Field('ext7')
                )
db.define_table('Upazila_List',
                Field('upazila_name', 'string'),
                Field('district_name', 'string'),
                Field('district_ref_id', 'reference District_List'),
                Field('ext4'),
                Field('ext5'),
                Field('ext6'),
                Field('ext7')
                )
db.define_table('Institution_Info',
                Field('district_name', 'string'),
                Field('district_ref_id', 'reference District_List', ondelete='CASCADE'),
                Field('upazila_name', 'string'),
                Field('upazila_ref_id', 'reference Upazila_List', ondelete='CASCADE'),
                Field('institution_name', 'string'),
                Field('institute_id', 'reference auth_user'),
                Field('full_name', 'string'),
                Field('ext8'),
                Field('ext9'),
                Field('ext10'),
                Field('ext11'),
                Field('ext12'),
                Field('ext13'),
                Field('ext14')
                )
db.define_table('Institute_Auth',
                Field('institute_ref_id', 'reference Institution_Info'),
                Field('auth_ref_id', 'reference auth_user'),
                Field('ext3'),
                Field('ext4'),
                Field('ext5'),
                Field('ext6')
                )
db.define_table('shift',
                Field('client_ref_id', 'reference auth_user'),
                Field('shift_name','string'),
                Field('shift_start','time'),
                Field('shift_end','time'),
                Field('shift_break_start','time'),
                Field('shift_break_end','time')
                )

db.define_table('employee_work_schedule',
                Field('client_ref_id', 'reference auth_user'),
                Field('user_ref_id', 'reference Users', ondelete='CASCADE'),
                Field('shift_id', 'reference shift', ondelete='CASCADE'),
                Field('shift_date', 'date'),
                Field('reg_id', 'string'),
                Field('in_time', 'time'),
                Field('out_time', 'time'),
                Field('shift_name', 'string'),
                Field('start_dt', 'datetime'),
                Field('end_dt', 'datetime')
                )
db.define_table('Employee_Salary',
                Field('client_ref_id', 'reference auth_user'),
                Field('user_ref_id', 'reference Users', ondelete='CASCADE'),
                Field('month', 'date'),
                Field('salary', 'integer'),
                Field('leave', 'boolean', default=True),
                Field('holiday', 'boolean', default=True),
                Field('shourly', 'integer', default=0),
                Field('hourly_limit', 'integer', default=0),
                Field('salary_type', 'integer', default=0),
                Field('last_log_type', 'string'),
                Field('status', 'integer', default=1),
                Field('house_rent', 'integer', default=0),
                Field('medical_al', 'integer', default=0),
                Field('conv', 'integer', default=0)
                )
db.define_table('Employee_Salary_Settings',
                Field('client_ref_id', 'reference auth_user'),
                Field('type', 'string'),  # client / month / specific day of user as dayofuser
                Field('user_ref_id', 'reference Users', ondelete='CASCADE'),
                Field('setting_date', 'date'),
                Field('in_out_threshold', 'integer', default=30),  #by seconds
                Field('late_day_threshold', 'integer', default=0),  #how many day's he/she late as absent -For Only Type: days
                Field('early_in', 'boolean'),
                Field('early_out', 'boolean'),
                Field('late_in', 'boolean'),
                Field('over_time', 'boolean'),
                Field('penalty', 'integer', default=0),
                Field('note', 'string'),
                Field('bonus', 'integer', default=0),
                Field('bonus_note', 'string'),
                Field('reference_id', 'integer'),   # Department or Branch
                Field('day_off', 'integer', default=0),  # Day Of status client wise
                Field('salary_use', 'integer', default=100),  # salary use of 100%
                Field('overtime_rate', 'integer', default=0)
                )
db.define_table('Attendance_Requests',
                Field('user_ref_id', 'reference Users'),
                Field('attendance_datetime', 'datetime'),
                Field('mac_id', 'string'),
                Field('longitude', 'string'),
                Field('latitude', 'string'),
                Field('status', 'string'),
                Field('location', 'string'),
                Field('unit_ref_id', 'reference Units'),
                Field('ext9'),
                Field('ext10'),
                Field('ext11')
                )
db.define_table('Branches',
                Field('client_ref_id', 'reference auth_user'),
                Field('name', type='string'),
                Field('status', type='integer', default=1),
                Field('ext4'),
                Field('ext5'),
                Field('ext6'),
                Field('ext7'),
                Field('ext9'),
                Field('ext10')
                )
db.define_table('Branch_Users',
                Field('client_ref_id', 'reference auth_user'),
                Field('branch_ref_id', 'reference Branches'),
                Field('user_ref_id', 'reference Users'),
                Field('ext4'),
                Field('ext5'),
                Field('ext6'),
                Field('ext7'),
                Field('ext9'),
                Field('ext10')
                )
db.define_table('Roles',
                Field('client_ref_id', 'reference auth_user'),
                Field('name', 'string'),
                Field('ext3'),
                Field('ext4'),
                Field('ext5')
                )
db.define_table('Role_Access',
                Field('role_ref_id', 'reference Roles'),
                Field('access', 'string'),
                Field('is_branch', 'integer', default=0),
                Field('ext4'),
                Field('ext5')
                )
db.define_table('Designations',
                Field('client_ref_id', 'reference auth_user'),
                Field('name', type='string'),
                Field('status', type='integer', default=1),
                Field('ext4'),
                Field('ext5'),
                Field('ext6')
                )
db.define_table('Designation_Users',
                Field('client_ref_id', 'reference auth_user'),
                Field('designation_ref_id', 'reference Designations'),
                Field('user_ref_id', 'reference Users'),
                Field('ext4'),
                Field('ext5'),
                Field('ext6')
                )
db.define_table('Role_Devices',
                Field('client_ref_id', 'reference auth_user'),
                Field('role_ref_id', 'reference Roles', ondelete='CASCADE'),
                Field('unit_ref_id', 'reference Units'),
                Field('ext4'),
                Field('ext5')
		        )
db.define_table('Shift_Users',
                Field('client_ref_id', 'reference auth_user'),
                Field('shift_ref_id', 'reference shift', ondelete='CASCADE'),
                Field('user_ref_id', 'reference Users', ondelete='CASCADE'),
                Field('start_date', 'date'),
                Field('end_date', 'date'),
                Field('start_datetime', 'datetime'),
                Field('end_datetime', 'datetime'),
                Field('shift_type', 'string'),
                Field('ext9'),
                Field('ext10')
                )
db.define_table('Bill',
                Field('client_name', 'reference auth_user',
                      requires=IS_IN_DB(db, db.auth_user.id, '%(first_name)s %(last_name)s (%(username)s)', error_message='Client does not exist in DB')),
                Field('description', 'text', requires=IS_NOT_EMPTY(
                    error_message='This field is required')),
                Field('debit', 'integer'),
                Field('credit', 'integer'),
                Field('transaction_method', requires=IS_IN_SET(
                    ['Cash', 'Non-cash'], zero=None)),
                Field('deleted', 'boolean', default=False,
                      requires=IS_NOT_EMPTY()),
                Field('edited_note', 'reference Bill',
                      ),
                Field('created_on', 'datetime', default=request.now),
                Field('modified_by', 'reference auth_user',
                      default=None if auth.user is None else auth.user.id),
                Field('billing_month', 'string'),
                Field('balance', 'integer'),
                Field('transaction_id', 'string')
                )
db.define_table('Manufactured_Device_Info',
                Field('manufactured_device_ref_id', 'reference Manufactured_device', ondelete='CASCADE'),
                Field('device_bill', 'integer'),
                Field('ext3'),
                Field('ext4'),
                Field('ext5'),
                Field('ext6'),
                Field('ext7'),
                Field('ext8')
                )

db.define_table('Leave_Type',
               Field('name', 'string'),
               Field('no_of_leave', 'integer', default=0),
               Field('pay_status', 'string'),
               Field('is_deleted', 'boolean', default=False),
               Field('created_by', 'reference auth_user'),
               Field('created_date', 'datetime'),
               Field('updated_by', 'reference auth_user'),
               Field('updated_date', 'datetime'),
            )


db.define_table('Assigned_Yearly_Leave',
               Field('leave_type_id', 'reference Leave_Type'),
               Field('rams_dept_ref_id', 'reference Classes'),                               
               Field('rams_des_ref_id', 'reference Designations'),               
               Field('rams_user_id', 'reference Users'),
               Field('assign_type', 'integer', default=0),                
               Field('leave_entitled', 'integer', default=0),
               Field('is_deleted', 'boolean', default=False),
               Field('created_by', 'reference auth_user'),
               Field('created_date', 'datetime'),
               Field('updated_by', 'reference auth_user'),
               Field('updated_date', 'datetime'),
            )



db.define_table('Leave__Leave_Mgt',
               Field('rams_leave_type_id', 'reference Leave_Type'),
               Field('rams_user_id', 'reference Users'),
               Field('leave_date', 'datetime'),
               Field('description', 'string'),
               Field('is_deleted', 'boolean', default=False),
               Field('is_approved', 'string'),
               Field('created_by', 'integer'),
               Field('created_date', 'datetime'),
               Field('updated_by', 'integer'),
               Field('updated_date', 'datetime'),
               Field('approved_by', 'reference auth_user'),
               Field('approved_date', 'datetime'),
            )


db.define_table('Table_Migration',
                Field('table_name', 'string'),
                Field('table_updated_id', 'integer'),
                Field('migration_date', 'datetime'),
                Field('migration_by', 'reference auth_user'),
                )
