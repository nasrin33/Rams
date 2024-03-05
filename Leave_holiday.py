from datetime import datetime, timedelta

@auth.requires_login()
def check_permission(access):
    if auth.user.parent in [None, 0]:
        return {
            'aid': auth.user.id,
            'branches': []
        }
    elif auth.user.roles_ref_id in [None, 0]:
        return redirect(URL('default', 'error_403'))
    else:
        role = db(db.Roles.id == auth.user.roles_ref_id).select().first()
        if role:
            has_permission = False
            branches = []
            for Role_Access in db((db.Role_Access.role_ref_id == role.id) & (db.Role_Access.is_branch == 0)).select():
                if access == Role_Access.access:
                    has_permission = True
            if has_permission == False:
                return redirect(URL('default', 'error_403'))
            for Role_Access in db((db.Role_Access.role_ref_id == role.id) & (db.Role_Access.is_branch == 1)).select():
                branches.append(Role_Access.access)
            return {
                'aid': auth.user.parent,
                'branches': branches
            }
        else:
            return redirect(URL('default', 'error_403'))
    return redirect(URL('default', 'error_403'))


@auth.requires_login()
def leave_holiday_management():
    active_tab = 'holiday'
    msge = ""
    c = "noclients"

    NoneType = type(None)
    if isinstance(session.client_id, NoneType):
        aid = auth.user.id
        client = "%(username)s" % auth.user
        session_set = "FALSE"
    else:
        aid = session.client_id
        client = session.client_name
        session_set = "TRUE"

    permissions = check_permission('holiday_or_leave_management')
    aid = permissions['aid']

    # making institute name
    institute = db.executesql("select institution_name from auth_user where id = %s", aid)[0][0]
    if not institute:
        institute = client

    users_status = 'inactive'
    if request.vars.inactivated_users and request.vars.inactivated_users == 'on':
        users_status = 'all_users'

    if len(permissions['branches']) == 0:
        branches = db.executesql("SELECT id, name FROM Branches WHERE status = 1 AND client_ref_id = %s", aid)
        allowable_branches = False
    else:
        branches = db.executesql("SELECT id, name FROM Branches WHERE status = 1 AND client_ref_id = %s AND id in %s",
                                 (aid, permissions['branches']))
        allowable_branches = permissions['branches']

    classes = db.executesql("select * from Classes where Client_Ref_ID=%s", aid)
    designations = db.executesql("select id,name from Designations where client_ref_id=%s", aid)
    classs = "all"
    start_date = datetime.now().replace(day=1).strftime('%Y-%m-%d')
    end_date = datetime.now().strftime('%Y-%m-%d')

    if request.vars.daterangepicker:
        date_range = request.vars.daterangepicker
        ranges = date_range.split("to")
        start_date = datetime.strptime(ranges[0].strip(), "%Y-%m-%d").date()
        end_date = datetime.strptime(ranges[1].strip(), "%Y-%m-%d").date()

    if request.vars.classs and (request.vars.classs not in ["all", '']):
        class_filter_query = "and u.department = '{}'".format(request.vars.classs)
    else:
        class_filter_query = ''

    if request.vars.branch and (request.vars.branch not in ["all", '']):
        allowable_branches = request.vars.branch
    else:
        allowable_branches = allowable_branches

    if request.vars.designation and (request.vars.designation not in ["all", '']):
        designation_query = " inner join Designation_Users as du on du.user_ref_id=u.id"
        designation_id = " and du.designation_ref_id=" + request.vars.designation
    else:
        designation_query = ""
        designation_id = ""

    if request.vars.GHL_Al_Del:
        aholiday = request.vars.aholiday
        db.executesql(
            "delete gh from Government_Holiday as gh inner join Vendor_Auth as va on va.auth_ref_id=gh.client_ref_id where va.vendor_ref_id=%s and gh.holiday=%s",
            (aid, aholiday))
    users = db.executesql(
        "select u.id,u.registration_id,u.user_name from Users as u inner join Client_Users as cu on u.id=cu.user_ref_id where u.deleted!=1 and u.status='active' and cu.client_ref_id=%s",
        aid)
    if request.vars.Submit_GH:
        active_tab = 'holiday'
        date_range = request.vars.holiday_date_range
        date_range = date_range.split("to")
        start_date = datetime.strptime(date_range[0].strip(), "%Y-%m-%d").date()
        end_date = datetime.strptime(date_range[1].strip(), "%Y-%m-%d").date()
        day_name = request.vars.day_name
        if str(day_name) == "11":
            msge = ''
            description = request.vars.description
            # clients = request.vars.clients
            for holiday in (start_date + timedelta(n) for n in range((end_date - start_date).days + 1)):
                # c = clients
                NoneType = type(None)
                exist = db.executesql(
                    "select holiday from Government_Holiday where holiday=%s and client_ref_id=%s", (holiday, aid))
                if exist:
                    msge += str(holiday) + ', '
                    # return locals()
                # db.Government_Holiday.insert(holiday=request.vars.holiday,description=request.vars.description)
                else:
                    db.executesql(
                        "insert into Government_Holiday(holiday,description,client_ref_id) values(%s,%s,%s)",
                        (holiday,
                         description, aid))
        else:
            # clients = request.vars.clients
            description = request.vars.description
            days = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1) if
                    (start_date + timedelta(days=x)).weekday() == int(day_name)]
            for holiday in days:
                # c = clients
                NoneType = type(None)

                exist = db.executesql(
                    "select holiday from Government_Holiday where holiday=%s and client_ref_id=%s", (holiday, aid))
                if exist:
                    msge += str(holiday) + ', '
                    # return locals()
                # db.Government_Holiday.insert(holiday=request.vars.holiday,description=request.vars.description)
                else:
                    db.executesql(
                        "insert into Government_Holiday(holiday,description,client_ref_id) values(%s,%s,%s)",
                        (holiday,
                         description, aid))
        # if msge != '':
        #     msge = 'Holiday ' + str(msge) + ' allready exists.'
    if request.vars.Submit_GH_Del:
        holiday = request.vars.holiday
        id = request.vars.id
        db.executesql(
            "delete from Government_Holiday where holiday=%s and id=%s",
            (holiday, id))

    if request.vars.Submit_SL_Del:
        id = request.vars.id
        db.executesql("delete from Student_Holidays where id=%s", id)

    if request.vars.Submit_SL:
        active_tab = 'leave'
        date_range = request.vars.leave_date_range
        date_range = date_range.split("to")
        start_date = datetime.strptime(date_range[0].strip(), "%Y-%m-%d").date()
        end_date = datetime.strptime(date_range[1].strip(), "%Y-%m-%d").date()
        day_name = request.vars.day_name

        msge = ''
        leave_type = request.vars.leave_type
        description = request.vars.cDescription
        reg_ids = request.vars.userId
        pay_status = request.vars.pay_status
        if isinstance(reg_ids, NoneType):
            return 'error'
        elif isinstance(reg_ids, str):
            reg_ids = list(reg_ids.split(" "))
        elif not isinstance(reg_ids, list):
            return 'error'
        if str(day_name) == "11":
            for holiday in (start_date + timedelta(n) for n in range((end_date - start_date).days + 1)):
                for reg_id in reg_ids:
                    exist = db.executesql(
                        "select holiday from Student_Holidays where holiday=%s and user_ref_id=%s and client_ref_id=%s",
                        (holiday,
                         reg_id,
                         aid))
                    if exist:
                        msge += str(holiday) + ', '
                    else:
                        db.executesql(
                            "insert into Student_Holidays(user_ref_id,holiday,description,pay_status,leave_type,client_ref_id) values (%s,%s,%s,%s,%s,%s)",
                            (reg_id, holiday, description, pay_status, leave_type, aid))
            if msge != '':
                msge = 'Leave date ' + msge[0:-2] + ' allready exists for this user.'
        else:
            days = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1) if
                    (start_date + timedelta(days=x)).weekday() == int(day_name)]
            for holiday in days:
                for reg_id in reg_ids:
                    exist = db.executesql(
                        "select holiday from Student_Holidays where holiday=%s and user_ref_id=%s and client_ref_id=%s",
                        (holiday,
                         reg_id,
                         aid))
                    if exist:
                        msge += str(holiday) + ', '
                    else:
                        db.executesql(
                            "insert into Student_Holidays(user_ref_id,holiday,description,pay_status,leave_type,client_ref_id) values (%s,%s,%s,%s,%s,%s)",
                            (reg_id, holiday, description, pay_status, leave_type, aid))
            if msge != '':
                msge = 'Leave date ' + msge[0:-2] + ' allready exists for this user.'
        active_tab = 'leave'
    if request.vars.search_holiday:
        active_tab = 'holiday'
        # date_range = request.vars.leave_date_range
        # date_range = date_range.split("to")
        # start_date = datetime.strptime(date_range[0].strip(), "%Y-%m-%d").date()
        # end_date = datetime.strptime(date_range[1].strip(), "%Y-%m-%d").date()

        GHL = db.executesql(
            "select gh.id,gh.holiday,gh.description,gh.client_ref_id,a.username from Government_Holiday as gh inner join auth_user as a on a.id=gh.client_ref_id where client_ref_id=%s and gh.holiday>=%s and gh.holiday<=%s",
            (aid, start_date, end_date))
        SLL = db.executesql("select u.registration_id,s.user_ref_id,s.holiday,s.description,s.id,s.pay_status, \
        s.leave_type, u.user_name from Users as u inner join Student_Holidays as s on s.user_ref_id=u.id \
        inner join Client_Users as cu on cu.user_ref_id=u.id where cu.client_ref_id=%s and \
        s.holiday>=%s and s.holiday<=%s", (aid, start_date, end_date))
    elif request.vars.search_leave:
        active_tab = 'leave'
        # date_range = request.vars.leave_date_range
        # date_range = date_range.split("to")
        # start_date = datetime.strptime(date_range[0].strip(), "%Y-%m-%d").date()
        # end_date = datetime.strptime(date_range[1].strip(), "%Y-%m-%d").date()

        GHL = db.executesql("select gh.id,gh.holiday,gh.description,gh.client_ref_id,a.username from \
        Government_Holiday as gh inner join auth_user as a on a.id=gh.client_ref_id where \
        client_ref_id=%s and gh.holiday>=%s and gh.holiday<=%s", (aid, start_date, end_date))
        # SLL = db.executesql("select u.registration_id,s.user_ref_id,s.holiday,s.description,s.id,s.pay_status, \
        # s.leave_type, u.user_name from Users as u inner join Student_Holidays as sh on sh.user_ref_id=u.id \
        # inner join Client_Users as cu on cu.user_ref_id=u.id where cu.client_ref_id=%s and \
        # s.holiday>=%s and s.holiday<=%s",(aid, start_date, end_date))

        if allowable_branches:
            if request.vars.branch and (request.vars.branch not in ["all", '']):

                query = "select u.registration_id,s.user_ref_id,s.holiday,s.description,s.id,s.pay_status, \
                    s.leave_type, u.user_name from Users as u \
                    inner join Student_Holidays as s on s.user_ref_id=u.id \
                    inner join Client_Users as cu on cu.user_ref_id=u.id \
                    left join Branch_Users as bu on bu.user_ref_id = u.id\
                    {} where cu.client_ref_id=%s and u.status != %s and s.holiday>=%s and s.holiday<=%s and bu.branch_ref_id = %s {}{}".format(
                    designation_query, class_filter_query, designation_id)
                data = (aid, users_status, start_date, end_date, request.vars.branch)
            else:
                query = "select u.registration_id,s.user_ref_id,s.holiday,s.description,s.id,s.pay_status, \
                    s.leave_type, u.user_name from Users as u \
                    inner join Student_Holidays as s on s.user_ref_id=u.id \
                                inner join Client_Users as cu on cu.user_ref_id=u.id\
                                left join Branch_Users as bu on bu.user_ref_id = u.id\
                                {} where cu.client_ref_id=%s and u.status != %s and s.holiday>=%s and s.holiday<=%s and bu.branch_ref_id in %s {}{}".format(
                    designation_query, class_filter_query, designation_id)
                data = (aid, users_status, start_date, end_date, allowable_branches)
        else:
            query = "select u.registration_id,s.user_ref_id,s.holiday,s.description,s.id,s.pay_status, \
                    s.leave_type, u.user_name from Users as u \
                    inner join Student_Holidays as s on s.user_ref_id=u.id \
                inner join Client_Users as cu on cu.user_ref_id=u.id\
                {} where cu.client_ref_id=%s and u.status != %s and s.holiday>=%s and s.holiday<=%s {}{}".format(
                designation_query, class_filter_query, designation_id)
            data = (aid, users_status, start_date, end_date)
        SLL = db.executesql(query, data)
    else:
        start_date = datetime.now().replace(day=1).strftime('%Y-%m-%d')
        end_date = datetime.now().strftime('%Y-%m-%d')

        GHL = db.executesql(
            "select gh.id,gh.holiday,gh.description,gh.client_ref_id,a.username from Government_Holiday as gh inner join auth_user as a on a.id=gh.client_ref_id where client_ref_id=%s and gh.holiday>=%s and gh.holiday<=%s",
            (aid, start_date, end_date))
        SLL = db.executesql("select u.registration_id,s.user_ref_id,s.holiday,s.description,s.id,s.pay_status, \
        s.leave_type, u.user_name from Users as u inner join Student_Holidays as s on s.user_ref_id=u.id \
        inner join Client_Users as cu on cu.user_ref_id=u.id where cu.client_ref_id=%s and \
        s.holiday>=%s and s.holiday<=%s", (aid, start_date, end_date))
    # SLL = db.executesql(
    #     "select u.registration_id,s.user_ref_id,s.holiday,s.description,s.id,s.pay_status, s.leave_type, u.user_name from Users as u, Student_Holidays as s where u.id=s.user_ref_id and s.user_ref_id in (select user_ref_id from Client_Users where client_ref_id=%s)",
    #     aid)
    # GHL = db.executesql("select gh.id,gh.holiday,gh.description,gh.client_ref_id,a.username from Government_Holiday as gh inner join auth_user as a on a.id=gh.client_ref_id where client_ref_id=%s",aid)
    # # if len(user_names) > 0:
    # #     GHL = GHL_client_list
    return locals()


@auth.requires_login()
def Leave_management():
    msge=''
    active_tab = 'leave_type'
    aid= auth.user.id
    leave_type = db.executesql("select id,name from Leave_Type")
    classes = db.executesql("select id, name from Classes where Client_Ref_ID=%s", aid)
    designations = db.executesql("select id,name from Designations where client_ref_id=%s", aid)
    users = db.executesql(
        "select u.id,u.registration_id,u.user_name from Users as u inner join Client_Users as cu on u.id=cu.user_ref_id where u.deleted!=1 and u.status='active' and cu.client_ref_id=%s",
        aid)


    if request.vars.Submit_LT:
        active_tab = 'leave_type'
        msge = ''
        name = request.vars.cname
        no_of_leave = request.vars.cleave
        pay_status = request.vars.cpay_status


        db.executesql("insert into Leave_Type(name, no_of_leave, pay_status, created_by) values (%s,%s,%s,%s)",
                            (name, no_of_leave, pay_status, auth.user.id))
        msge='Leave Type saved successfully'
        active_tab = 'leave_type'
        

    if request.vars.Submit_edit_LT:
        msge = ''
        auth_id= auth.user.id
        id= request.vars.edit_type_id
        name = request.vars.edit_type_name
        no_of_leave = request.vars.edit_no_of_leave
        pay_status = request.vars.edit_pay_status

        updated_date= datetime.now()

        db.executesql("update Leave_Type set name=%s, no_of_leave=%s, pay_status=%s, updated_by=%s, updated_date=%s where id=%s",
                        (name, no_of_leave, pay_status, auth_id, updated_date, id))
        msge = 'Leave Type is updated'
        active_tab = 'leave_type'


    if request.vars.Submit_LT_Del:
        id = request.vars.id
        db.executesql("delete from Leave_Type where id=%s", id)
        msge='Leave Type deleted successfully'
        active_tab = 'leave_type'


    if request.vars.Submit_LR:
        msge = ''
        cLeaveType = request.vars.cLeaveType
        cAssignType = request.vars.cassignType
        cclass= request.vars.cclass
        cdesignation= request.vars.cdesignation
        cuser= request.vars.cuser
        cleave = request.vars.cleave

        if cuser.strip():
            db.executesql("insert into Assigned_Yearly_Leave(leave_type_id, rams_dept_ref_id, rams_des_ref_id, rams_user_id, leave_entitled, created_by) values (%s,%s,%s,%s,%s,%s)",
                            (cLeaveType, cclass, cdesignation, cuser, cleave, auth.user.id))
            
        if cdesignation.strip():
            user_list= db.executesql("select user_ref_id from Designation_Users where designation_ref_id=%s", cdesignation)
            for user_ref_id in user_list:
                db.executesql("insert into Assigned_Yearly_Leave(leave_type_id, rams_dept_ref_id, rams_des_ref_id, rams_user_id, leave_entitled, created_by) values (%s,%s,%s,%s,%s,%s)",
                            (cLeaveType, cclass, cdesignation, user_ref_id, cleave, auth.user.id))
                
        if cclass.strip():
            dept_name= db.executesql("select name from Classes where id=%s", cclass)
            user_list= db.executesql("select id from Users where department=%s", dept_name)

        msge='Assigned Yearly Leave saved successfully'
        active_tab = 'assigned_yearly_leave'


    if request.vars.Submit_edit_ayl:
        id = request.vars.edit_ayl_id
        leave_type_id = request.vars.edit_ayl_leave_type
        rams_user_id = request.vars.edit_ayl_users
        leave_entitled = request.vars.edit_leave_entitled

        updated_date= datetime.now()
        updated_by= auth.user.id

        db.executesql("update Assigned_Yearly_Leave set leave_type_id=%s, rams_user_id=%s, leave_entitled=%s, updated_by=%s, updated_date=%s where id=%s", (leave_type_id, rams_user_id, leave_entitled, updated_by, updated_date, id))
        msge = 'Yearly Leave is updated'
        active_tab = 'assigned_yearly_leave'


    if request.vars.Submit_LR_Del:
        id = request.vars.id
        db.executesql("delete from Assigned_Yearly_Leave where id=%s", id)
        msge='Assigned Yearly Leave deleted successfully'
        active_tab = 'assigned_yearly_leave'


    leave_type_list = db.executesql("select id,name,no_of_leave,pay_status,created_by from Leave_Type")
    leave_role_list = db.executesql("select LR.id, LR.leave_type_id, LR.rams_user_id, LR.leave_entitled, u.user_name, LT.name from Assigned_Yearly_Leave as LR inner join Users as u on LR.rams_user_id=u.id inner join Leave_Type as LT on LR.leave_type_id=LT.id")

    return locals()


@auth.requires_login()
def get_type_info():
    id= request.vars.c_id
    leave_type_list= db.executesql("select LT.id, LT.name, LT.no_of_leave, LT.pay_status from Leave_Type as LT where LT.id= %s", id)

    return response.json({
            'leave_type': leave_type_list,
        })

@auth.requires_login()
def get_yearly_leave():
    id= request.vars.c_id
    aid= auth.user.id
    yearly_leave_list= db.executesql("select AYL.id, AYL.rams_user_id, AYL.leave_entitled, AYL.leave_type_id from Assigned_Yearly_Leave as AYL where AYL.id= %s", id)
    users = db.executesql(
        "select u.id,u.registration_id,u.user_name from Users as u inner join Client_Users as cu on u.id=cu.user_ref_id where u.deleted!=1 and u.status='active' and cu.client_ref_id=%s",
        aid)
    leave_type = db.executesql("select id,name from leave_type where created_by=%s", aid)

    return response.json({
            'leave_type': leave_type,
            'users': users,
            'yearly_leave': yearly_leave_list
        })



@auth.requires_login()
def apply_leave():
    
    if request.vars.Submit_AL:
        rams_user_id= request.vars.user_id
        leave_type_id= request.vars.leave_type
        from_date=  datetime.strptime(request.vars.from_date, '%Y-%m-%d')
        to_date= datetime.strptime(request.vars.to_date, '%Y-%m-%d')
        description= request.vars.description
        leave_requested= int(request.vars.leave_requested)
        leave_due= int(request.vars.leave_due)


        existing_leave=db.executesql("select LM.id from Leave__Leave_Mgt as LM where LM.rams_user_id=%s and LM.is_deleted=0 AND LM.leave_date BETWEEN %s AND %s",(rams_user_id, from_date, to_date))
        
        if existing_leave:
            msge = 'Leave exists withing the selected date range'
        
        elif leave_requested > leave_due:
            msge= "Insufficient leave balance. Please contact with administrator"

        else:
            approved_date= datetime.now()

            while from_date <= to_date:

                db.executesql("insert into Leave__Leave_Mgt(rams_leave_type_id, rams_user_id, leave_date, description, is_approved,approved_by_id, approved_date) values (%s,%s,%s,%s,%s,%s,%s)",(leave_type_id, rams_user_id, from_date,description,"approved", auth.user.id, approved_date))

                from_date += timedelta(days=1)


                msge = 'Leave is added'
                
        aid= auth.user.id
    
        current_date= datetime.now().date()


        users = db.executesql(
        "select u.id,u.registration_id,u.user_name from Users as u inner join Client_Users as cu on u.id=cu.user_ref_id where u.deleted!=1 and u.status='active' and cu.client_ref_id=%s",aid)
        
        return locals()


    msge=""
    aid= auth.user.id
    
    current_date= datetime.now().date()

    users = db.executesql(
        "select u.id,u.registration_id,u.user_name from Users as u inner join Client_Users as cu on u.id=cu.user_ref_id where u.deleted!=1 and u.status='active' and cu.client_ref_id=%s",aid)
    return locals()


def get_leave_type():
    id= request.args(0)

    user_leave_type_list=[]
    
    assigned_yearly_leave_list= db.executesql("select AYL.id, AYL.rams_user_id, AYL.leave_type_id, AYL.leave_entitled, LT.name from Assigned_Yearly_Leave as AYL join Leave_Type as LT on LT.id=AYL.leave_type_id where AYL.is_deleted=0 and AYL.rams_user_id= %s", id)
   
    for assigned_yearly_leave in assigned_yearly_leave_list:
        
        leave_type_id=assigned_yearly_leave[2]

        leave_type_wise_count= db.executesql("SELECT count(LLM.id) FROM Leave__Leave_Mgt as LLM where LLM.is_deleted=0 and LLM.is_approved!='rejected' and LLM.rams_user_id= %s and LLM.rams_leave_type_id=%s", (id, leave_type_id))
                
        leave_due = assigned_yearly_leave[3]-leave_type_wise_count[0][0]
        
        if leave_due>0:
            leave_type_data={
                    "id": assigned_yearly_leave[2],
                    "name": assigned_yearly_leave[4],
                    "leave_due": leave_due
                }
        user_leave_type_list.append(leave_type_data)
        


    return response.json({
            'leave_type': user_leave_type_list,
        })

@auth.requires_login()
def leave_approval():
    if request.vars.Submit_LA_apr:
        id = request.vars.id
        is_approved= "approved"
        approved_date= datetime.now()
        user_id=auth.user.id

        db.executesql("update Leave__Leave_Mgt set approved_by_id=%s, approved_date=%s, is_approved=%s where id=%s",
                    (user_id, approved_date, is_approved, id))
        db.commit()
        msge = 'Leave is approved'

    if request.vars.Submit_LA_rej:
        id = request.vars.id
        user_id=auth.user.id
        approved_date= datetime.now()
        is_approved= "rejected"
        db.executesql("update Leave__Leave_Mgt set approved_by_id=%s, approved_date=%s, is_approved=%s where id=%s",
                    (user_id, approved_date, is_approved, id))

        db.commit()
        msge = 'Leave is rejected'

    msge= ""
    aid= auth.user.id
    leave_list = db.executesql("select LLM.id, LLM.rams_leave_type_id, LLM.rams_user_id, LLM.leave_date, LLM.description, LLM.created_date, u.user_name, LT.name from Leave__Leave_Mgt as LLM inner join Users as u on LLM.rams_user_id=u.id inner join Leave_Type as LT on LLM.rams_leave_type_id=LT.id join Client_Users as cu on LLM.rams_user_id=cu.user_ref_id where LLM.is_approved='pending' and cu.client_ref_id=%s", aid)

    return locals()

@auth.requires_login()
def post_selected_approved():

    id_list= request.vars.ids
    leave_id_list = [int(id) for id in id_list.split(',')]
    user_id=auth.user.id
    is_approved= "approved"
    approved_date= datetime.now()
    # update each row
    for id in leave_id_list:
        db.executesql("update Leave__Leave_Mgt set approved_by_id=%s, approved_date=%s, is_approved=%s where id=%s",
                    (user_id, approved_date, is_approved, id))
        db.commit()

    msg= "Approved"
    return msg

@auth.requires_login()
def post_selected_rejected():

    id_list= request.vars.ids
    leave_id_list = [int(id) for id in id_list.split(',')]
    is_approved= "rejected"
    user_id=auth.user.id
    approved_date= datetime.now()

    # update each row
    for id in leave_id_list:
        db.executesql("update Leave__Leave_Mgt set approved_by_id=%s, approved_date=%s, is_approved=%s where id=%s",
                    (user_id, approved_date, is_approved, id))
        
        db.commit()

    msg= "Rejected"
    return msg

@auth.requires_login()
def leave_list():
     msge=""
     aid= auth.user.id

     leave_list = db.executesql("select LLM.id, LLM.rams_leave_type_id, LLM.rams_user_id, LLM.leave_date, LLM.description, LLM.created_date, u.user_name, LT.name,LLM.is_approved from Leave__Leave_Mgt as LLM inner join Users as u on LLM.rams_user_id=u.id inner join Leave_Type as LT on LLM.rams_leave_type_id=LT.id join Client_Users as cu on LLM.rams_user_id=cu.user_ref_id where cu.client_ref_id=%s", aid)
     return locals()

def edit_leave2():
    return redirect(URL('Leave_holiday', 'edit_leave'))

def edit_leave():
    if request.vars.Submit_EL:
        id= request.vars.leave_id
        rams_user_id= request.vars.user_id
        leave_type_id= request.vars.leave_type
        leave_date= request.vars.leave_date
        description= request.vars.description
        approved_date= datetime.now()
        auth_id= auth.user.id

        
        
        db.executesql("update Leave__Leave_Mgt set is_deleted=1,approved_by_id=%s,approved_date=%s where id=%s", (auth_id,approved_date,id))

        db.executesql("insert into Leave__Leave_Mgt(rams_leave_type_id, rams_user_id, leave_date, description, is_approved,created_by_id, approved_by_id, approved_date) values (%s,%s,%s,%s,%s,%s,%s,%s)",(leave_type_id, rams_user_id, leave_date, description,"approved", auth_id, auth_id, approved_date))

        msge = 'Leave is updated'
        return redirect(URL('Leave_holiday', 'leave_list'))

        
    msge=""
    id= request.vars.leave_id
    leave_data= db.executesql("select LLM.id, LLM.rams_leave_type_id, LLM.rams_user_id, LLM.leave_date, LLM.description from Leave__Leave_Mgt as LLM where LLM.id=%s", id)
    aid= auth.user.id
    
    current_date= datetime.now().date()

    users = db.executesql(
        "select u.id,u.registration_id,u.user_name from Users as u inner join Client_Users as cu on u.id=cu.user_ref_id where u.deleted!=1 and u.status='active' and cu.client_ref_id=%s",aid)
    
#     leave_date= datetime.strptime(leave_data[0][3], '%Y-%m-%d')
    leave_date= leave_data[0][3].strftime('%Y-%m-%d')
#     rams_user_id= leave_data[0][2]
        
    return locals()

def get_edit_leave_type():
    id= request.args[0]
    
    edit_leave_type_id= int(request.args[1]) 

    user_leave_type_list=[]
    
    assigned_yearly_leave_list= db.executesql("select AYL.id, AYL.rams_user_id, AYL.leave_type_id, AYL.leave_entitled, LT.name from Assigned_Yearly_Leave as AYL join Leave_type as LT on LT.id=AYL.leave_type_id where AYL.is_deleted=0 and AYL.rams_user_id= %s", id)
   
    for assigned_yearly_leave in assigned_yearly_leave_list:
        
        leave_type_id=assigned_yearly_leave[2]

        leave_type_wise_count= db.executesql("SELECT count(LLM.id) FROM Leave__Leave_Mgt as LLM where LLM.is_deleted=0 and LLM.is_approved!='rejected' and LLM.rams_user_id= %s and LLM.rams_leave_type_id=%s", (id, leave_type_id))
                
#         leave_due = assigned_yearly_leave[3]-leave_type_wise_count[0][0] 
        leave_due = assigned_yearly_leave[3]-leave_type_wise_count[0][0]+1 if edit_leave_type_id==assigned_yearly_leave[2] else assigned_yearly_leave[3]-leave_type_wise_count[0][0]

        
        if leave_due>0:
            leave_type_data={
                    "id": assigned_yearly_leave[2],
                    "name": assigned_yearly_leave[4],
                    "leave_due": leave_due
                }
        user_leave_type_list.append(leave_type_data)
        


    return response.json({
            'leave_type': user_leave_type_list,
        })


def api_add_leave():
    id = request.vars.id
    rams_leave_type_id = request.vars.rams_leave_type_id
    rams_user_id = request.vars.rams_user_id
    leave_date = request.vars.leave_date
    description = request.vars.description
    created_by_id = request.vars.created_by_id
    created_date = request.vars.created_date
    updated_date=request.vars.updated_date

    db.executesql("insert into Leave__Leave_Mgt(id, rams_leave_type_id, rams_user_id, leave_date, description, is_approved,created_by_id, created_date, updated_date) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)",(id,rams_leave_type_id, rams_user_id, leave_date ,description,"pending", created_by_id, created_date,updated_date))

    
    

def api_update_leave():
    id = request.vars.leave_id
    rams_leave_type_id = request.vars.rams_leave_type_id
    rams_user_id = request.vars.rams_user_id
    description = request.vars.description
    updated_by_id = request.vars.updated_by_id
    updated_date=request.vars.updated_date

    db.executesql("update Leave__Leave_Mgt set rams_leave_type_id=%s, rams_user_id=%s, description=%s, updated_by_id=%s, updated_date=%s where id=%s",(rams_leave_type_id, rams_user_id, description, updated_by_id, updated_date, id))
    
    
    
def api_delete_leave():
    id = request.vars.leave_id
    is_deleted= 1
    # print(is_deleted)
    updated_by_id = request.vars.updated_by_id
    updated_date=request.vars.updated_date

    db.executesql("update Leave__Leave_Mgt set is_deleted=%s, updated_by_id=%s, updated_date=%s where id=%s",(is_deleted,updated_by_id, updated_date, id))
