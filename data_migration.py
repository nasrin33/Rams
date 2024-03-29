from datetime import datetime
import requests

@auth.requires_login()
def users_migration():
    till_updated_id= db.executesql("select tm.table_updated_id from Table_Migration as tm where tm.table_name='users'")
    if till_updated_id:
        id=till_updated_id[0][0]
    else:
        id="0"
    users = db.executesql("select u.id,u.registration_id,u.user_name,u.email,u.phone,u.deleted from Users as u where u.id > %s", id)
    if users:
    # Define the data you want to send to Django
        data = {
            'users': users
        }

        django_url = 'http://user.stellarbd.com:8000/rams/api/users_migration/'

        # Send a POST request to Django
        json_data = requests.post(django_url, data=data).json()
        status_code = json_data.get("status_code")

        if status_code=="200":
            last_id = users[-1][0]
            migration_date= datetime.now()
            migration_by= auth.user.id
            table_name="users"

            if till_updated_id:
                db.executesql("update Table_Migration set table_updated_id=%s, migration_date=%s, migration_by=%s where table_name=%s", (last_id,migration_date, migration_by, table_name))
               
            else:
                db.executesql("insert into Table_Migration(table_name, table_updated_id, migration_date, migration_by) values (%s,%s,%s,%s)",(table_name, last_id, migration_date, migration_by))

            msg= "Successful"
            return locals()

        else:
            msg= "Django server not found"
            return locals()


    else:
        msg= "No results found"
        return locals()


@auth.requires_login()
def units_migration():
    till_updated_id= db.executesql("select tm.table_updated_id from Table_Migration as tm where tm.table_name='units'")
    if till_updated_id:
        id=till_updated_id[0][0]
    else:
        id="9000"
    units = db.executesql("select u.id,u.unit_id,u.unit_name from Units as u where u.id > %s", id)
    if units:
    # Define the data you want to send to Django
        data = {
            'units': units
        }

        django_url = 'http://user.stellarbd.com:8000/rams/api/units_migration/'

        # Send a POST request to Django
        json_data = requests.post(django_url, data=data).json()
        status_code = json_data.get("status_code")

        if status_code=="200":
            last_id = units[-1][0]
            migration_date= datetime.now()
            migration_by= auth.user.id
            table_name="units"

            if till_updated_id:
                db.executesql("update Table_Migration set table_updated_id=%s, migration_date=%s, migration_by=%s where table_name=%s", (last_id,migration_date, migration_by, table_name))
               
            else:
                db.executesql("insert into Table_Migration(table_name, table_updated_id, migration_date, migration_by) values (%s,%s,%s,%s)",(table_name, last_id, migration_date, migration_by))

            msg= "Successful"
            return locals()

        else:
            msg= "Django server not found"
            return locals()


    else:
        msg= "No results found"
        return locals()



@auth.requires_login()
def client_users_migration():
    till_updated_id= db.executesql("select tm.table_updated_id from Table_Migration as tm where tm.table_name='client_users'")
    if till_updated_id:
        id=till_updated_id[0][0]
    else:
        id="0"
    client_users = db.executesql("select cu.id, cu.Client_Ref_ID, cu.User_Ref_ID from Client_Users as cu where cu.id > %s",id)
    if client_users:
        data = {
            'client_users': client_users
        }

        django_url = 'http://user.stellarbd.com:8000/rams/api/client_users_migration/'

        # Send a POST request to Django

        json_data = requests.post(django_url, data=data).json()
        status_code = json_data.get("status_code")

        if status_code=="200":

            last_id = client_users[-1][0]
            migration_date= datetime.now()
            migration_by= auth.user.id
            table_name= "client_users"
            if till_updated_id:
                db.executesql("update Table_Migration set table_updated_id=%s,migration_date=%s,migration_by=%s where table_name=%s", (last_id,migration_date, migration_by, table_name))
            else:
                db.executesql("insert into Table_Migration(table_name, table_updated_id, migration_date, migration_by) values (%s,%s,%s,%s)",(table_name, last_id, migration_date, migration_by))

            msg= "Successful"
            return locals()

        else:
            msg= "Django server not found"
            return locals()

    else:
        msg= "No results found"
        return locals()


@auth.requires_login()
def client_unit_migration():
    till_updated_id= db.executesql("select tm.table_updated_id from Table_Migration as tm where tm.table_name='client_unit'")
    if till_updated_id:
        id=till_updated_id[0][0]
    else:
        id="0"
    client_unit = db.executesql("select cu.id, cu.Client_Ref_ID, cu.Unit_Ref_ID from Client_Unit as cu where cu.id > %s",id)
    if client_unit:

        data = {
            'client_unit': client_unit
        }

        django_url = 'http://user.stellarbd.com:8000/rams/api/client_unit_migration/'

        # Send a POST request to Django
        json_data = requests.post(django_url, data=data).json()
        status_code = json_data.get("status_code")

        if status_code=="200":
            last_id = client_unit[-1][0]
            migration_date= datetime.now()
            migration_by= auth.user.id
            table_name= "client_unit"
            if till_updated_id:
                db.executesql("update Table_Migration set table_updated_id=%s,migration_date=%s,migration_by=%s where table_name=%s", (last_id,migration_date, migration_by, table_name))
            else:
                db.executesql("insert into Table_Migration(table_name, table_updated_id, migration_date, migration_by) values (%s,%s,%s,%s)",(table_name, last_id, migration_date, migration_by))

            msg= "Successful"
            return locals()
        else:
            msg= "Django server not found"
            return locals()

    else:
        msg= "No results found"
        return locals()




@auth.requires_login()
def unit_users_migration():
    till_updated_id= db.executesql("select tm.table_updated_id from Table_Migration as tm where tm.table_name='unit_users'")
    if till_updated_id:
        id=till_updated_id[0][0]
    else:
        id="0"
    unit_users = db.executesql("select cu.id, cu.Unit_Ref_ID, cu.User_Ref_ID, cu.access_type from Unit_Users as cu where cu.id > %s",id)
    if unit_users:

        data = {
            'unit_users': unit_users
        }

        django_url = 'http://user.stellarbd.com:8000/rams/api/unit_users_migration/'

        # Send a POST request to Django
        json_data =  requests.post(django_url, data=data).json()
        status_code = json_data.get("status_code")

        if status_code=="200":
            last_id = unit_users[-1][0]
            migration_date= datetime.now()
            migration_by= auth.user.id
            table_name= "unit_users"
            if till_updated_id:
                db.executesql("update Table_Migration set table_updated_id=%s,migration_date=%s,migration_by=%s where table_name=%s", (last_id,migration_date, migration_by, table_name))
            else:
                db.executesql("insert into Table_Migration(table_name, table_updated_id, migration_date, migration_by) values (%s,%s,%s,%s)",(table_name, last_id, migration_date, migration_by))

            msg= "Successful"
            return locals()
        else:
            msg= "Django server not found"
            return locals()
    else:
        msg= "No results found"
        return locals()

    
@auth.requires_login()
def leave_type_migration():
    till_updated_date= db.executesql("select tm.migration_date from Table_Migration as tm where tm.table_name='leave_type'")
    
    if till_updated_date:
        id=till_updated_date[0][0]
    else:
        id="1980-01-01"
    
    leave_type = db.executesql("select LT.id, LT.name, LT.no_of_leave, LT.pay_status, LT.is_deleted, LT.created_by, LT.created_date, LT.updated_by, LT.updated_date from Leave_Type as LT where LT.created_date > %s or LT.updated_date > %s", (id, id))
    
    if leave_type:
        
        data = {
            'leave_type': leave_type
        }

        django_url = 'http://user.stellarbd.com:8000/rams/api/leave_type_migration/'

        # Send a POST request to Django
        json_data = requests.post(django_url, data=data).json()
        status_code = json_data.get("status_code")

        if status_code=="200":
            last_id = leave_type[-1][0]
            migration_date= datetime.now()
            migration_by= auth.user.id
            table_name= "leave_type"
            if till_updated_date:
                db.executesql("update Table_Migration set table_updated_id=%s,migration_date=%s,migration_by=%s where table_name=%s", (last_id,migration_date, migration_by, table_name))
            else:
                db.executesql("insert into Table_Migration(table_name, table_updated_id, migration_date, migration_by) values (%s,%s,%s,%s)",(table_name, last_id, migration_date, migration_by))

            msg= "Successful"
            return locals()
        else:
            msg= "Django server not found"
            return locals()
    else:
        msg= "No results found"
        return locals()



@auth.requires_login()
def assigned_yearly_leave_migration():
    till_updated_date= db.executesql("select tm.migration_date from Table_Migration as tm where tm.table_name='assigned_yearly_leave'")
    
    if till_updated_date:
        id=till_updated_date[0][0]
    else:
        id="1980-01-01"
    
    assigned_yearly_leave = db.executesql("select LT.id, LT.leave_type_id , LT.rams_user_id, LT.leave_entitled, LT.is_deleted, LT.created_by, LT.created_date, LT.updated_by, LT.updated_date from Assigned_Yearly_Leave as LT where LT.created_date > %s or LT.updated_date > %s", (id, id))
    
    if assigned_yearly_leave:
        
        data = {
            'assigned_yearly_leave': assigned_yearly_leave
        }

        django_url = 'http://user.stellarbd.com:8000/rams/api/assigned_yearly_leave_migration/'

        # Send a POST request to Django
        json_data = requests.post(django_url, data=data).json()
        status_code = json_data.get("status_code")

        if status_code=="200":
            last_id = assigned_yearly_leave[-1][0]
            migration_date= datetime.now()
            migration_by= auth.user.id
            table_name= "assigned_yearly_leave"
            if till_updated_date:
                db.executesql("update Table_Migration set table_updated_id=%s,migration_date=%s,migration_by=%s where table_name=%s", (last_id,migration_date, migration_by, table_name))
            else:
                db.executesql("insert into Table_Migration(table_name, table_updated_id, migration_date, migration_by) values (%s,%s,%s,%s)",(table_name, last_id, migration_date, migration_by))

            msg= "Successful"
            return locals()
        else:
            msg= "Django server not found"
            return locals()
    else:
        msg= "No results found"
        return locals()

@auth.requires_login()
def leave_migration():
    till_updated_date= db.executesql("select tm.migration_date from Table_Migration as tm where tm.table_name='leave__leave_mgt'")
    
    if till_updated_date:
        id=till_updated_date[0][0]
    else:
        id="1980-01-01"
    
    leave_mgt = db.executesql("select LT.id, LT.leave_date, LT.rams_leave_type_id, LT.rams_user_id, LT.description, LT.is_deleted, LT.is_approved, LT.created_by_id, LT.created_date, LT.updated_by_id, LT.updated_date, LT.approved_by_id, LT.approved_date from Leave__Leave_Mgt as LT where LT.approved_date > %s", id)
 
    
    if leave_mgt:
        
        data = {
            'leave_mgt': leave_mgt
        }

        django_url = 'http://user.stellarbd.com:8000/rams/api/leave_migration/'

        # Send a POST request to Django
        json_data = requests.post(django_url, data=data).json()
        status_code = json_data.get("status_code")

        if status_code=="200":
            last_id = leave_mgt[-1][0]
            migration_date= datetime.now()
            migration_by= auth.user.id
            table_name= "leave__leave_mgt"
            if till_updated_date:
                db.executesql("update Table_Migration set table_updated_id=%s,migration_date=%s,migration_by=%s where table_name=%s", (last_id,migration_date, migration_by, table_name))
            else:
                db.executesql("insert into Table_Migration(table_name, table_updated_id, migration_date, migration_by) values (%s,%s,%s,%s)",(table_name, last_id, migration_date, migration_by))

            msg= "Successful"
            return locals()
        else:
            msg= "Django server not found"
            return locals()
    else:
        msg= "No results found"
        return locals()


@auth.requires_login()
def access_log_migration():
    till_updated_id= db.executesql("select tm.table_updated_id from Table_Migration as tm where tm.table_name='access_log'")
    
    if till_updated_id:
        id=till_updated_id[0][0]
    else:
        id="0"

    access_log = db.executesql("select LT.id, LT.Unit_ref_ID , LT.User_Ref_ID, LT.access_date, LT.access_time from Access_Log as LT where LT.id > %s",id)

    if access_log:
        
        data = {
            'access_log': access_log
        }

        django_url = 'http://user.stellarbd.com:8000/rams/api/access_log_migration/'

        # Send a POST request to Django
        json_data = requests.post(django_url, data=data).json()
        status_code = json_data.get("status_code")

        if status_code=="200":
            last_id = access_log[-1][0]
            migration_date= datetime.now()
            migration_by= auth.user.id
            table_name= "access_log"
            if till_updated_id:
                db.executesql("update Table_Migration set table_updated_id=%s,migration_date=%s,migration_by=%s where table_name=%s", (last_id,migration_date, migration_by, table_name))
            else:
                db.executesql("insert into Table_Migration(table_name, table_updated_id, migration_date, migration_by) values (%s,%s,%s,%s)",(table_name, last_id, migration_date, migration_by))

            msg= "Successful"
            return locals()
        else:
            msg= "Django server not found"
            return locals()
    else:
        msg= "No results found"
        return locals()

@auth.requires_login()
def table_migration_details():
   
    table_migration_details = db.executesql("select LT.id, LT.table_name, LT.operation, LT.uid, LT.registration_id, LT.user_name, LT.phone, LT.email, LT.deleted, LT.unit_id, LT.unit_name, LT.client_ref_id, LT.user_ref_id, LT.cu_client_ref_id, LT.cu_unit_ref_id, LT.uu_unit_ref_id, LT.uu_user_ref_id, LT.access_type from Table_Migration_Details as LT")

    if table_migration_details:
        
        data = {
            'table_migration_details': table_migration_details
        }

        django_url = 'http://user.stellarbd.com:8000/rams/api/table_migration_details/'

        # Send a POST request to Django
        json_data = requests.post(django_url, data=data).json()
        status_code = json_data.get("status_code")

        if status_code=="200": 
            db.executesql('DELETE FROM Table_Migration_Details')
            msg= "Successful"
            return locals()
        else:
            msg= "Django server not found"
            return locals()
    else:
        msg= "No results found"
        return locals()
