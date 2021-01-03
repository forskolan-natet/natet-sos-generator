import mysql.connector
from generator.date_range import date_range


class DAO:
    def __init__(self):
        self.db = mysql.connector.connect(host="127.0.0.1", user="root", passwd="kaka1234", db="forskolannatet")

    def _run(self):
        cursor = self.db.cursor()
        cursor.execute(self.query)
        return cursor.fetchall()


class ClosedDaysDAO(DAO):
    query = """
            select date(dat_begin) start, date(dat_end) end
            from adm_dates
            where dat_cat_id = 19
                and dat_all_day = 1;
            """

    def get_closed_days(self):
        result = self._run()

        closed_days = []
        for start, end in result:
            for date in date_range(start, end):
                closed_days.append(date.strftime("%Y-%m-%d"))

        return closed_days
    

class MembersDAO(DAO):
    query = """
            select
                users.usr_id AS id,
                (select user_data.usd_value from adm_user_data as user_data where user_data.usd_usr_id = users.usr_id and user_data.usd_usf_id = 2) AS firstname,
                (select user_data.usd_value from adm_user_data as user_data where user_data.usd_usr_id = users.usr_id and user_data.usd_usf_id = 1) AS lastname,
                (select members.mem_begin from adm_members as members where members.mem_usr_id = users.usr_id and members.mem_rol_id = 2) as startDate, # 2=Member
                (select members.mem_end from adm_members as members where members.mem_usr_id = users.usr_id and members.mem_rol_id = 2) as endDate, # 2=Member
                (select relations.ure_usr_id2 from adm_user_relations as relations where relations.ure_urt_id = 5 and users.usr_id = relations.ure_usr_id1) as partner_id,
                (select relations.ure_usr_id2 from adm_user_relations as relations where relations.ure_urt_id = 6 and users.usr_id = relations.ure_usr_id1 limit 1) as sponsorTo,
                (select relations.ure_usr_id2 from adm_user_relations as relations where relations.ure_urt_id = 7 and users.usr_id = relations.ure_usr_id1 limit 1) as sponsor,
                (case
                    when 0 < (select count(*) from adm_members as members
                              where members.mem_usr_id = users.usr_id
                              and members.mem_leader = 1
                              and members.mem_rol_id in (9, 10) # 9=personal, 10=ekonomi
                              and members.mem_end > cast((now() + interval 1 month) as date)) then 0
                    when 0 < (select count(*) from adm_members as members
                              where members.mem_usr_id = users.usr_id
                              and members.mem_rol_id in (5, 15) # 5=styrelsen, 15=Löneansvarig
                              and members.mem_end > cast((now() + interval 1 month) as date)) then 50
                    else 100 end) as sosPercentage
            from
                adm_users users
            where # Only actvive members
                (select count(*) from adm_members as members
                where members.mem_rol_id = 2
                and members.mem_usr_id = users.usr_id
                and members.mem_end > CURDATE()) > 0
            and # No kids
                (select count(*) from adm_members as members  where members.mem_rol_id = 11 and members.mem_usr_id = users.usr_id) = 0
            order by sosPercentage asc;
            """

    def get_members_for_sos_generator(self):
        result = self._run()

        members = []
        for id, first_name, last_name, start_date, end_date, partner_id, sponsor_to_member, \
                sponsored_by_member, sos_percentage in result:
            members.append({
                "id": id,
                "first_name": first_name,
                "last_name": last_name,
                "sos_percentage": sos_percentage,
                "start_date": start_date,
                "end_date": end_date,
                "sponsor_to_member": sponsor_to_member,
                "sponsored_by_member": sponsored_by_member,
                "partner_id": partner_id
            })
        return members


class ScheduleLiveDAO(DAO):
    select_last_scheduled_date = """SELECT DATE(MAX(sl.`day`)) FROM `sos_schedule` sl"""
    select_last_ten_sos_days = """
        SELECT
            `sl`.`day`,
            `sl`.`department_id`,
            `sl`.`user_id`
        FROM
            (
                SELECT
                    `day`,
                    `department_id`,
                    `user_id`
                FROM
                    `sos_schedule`
                ORDER BY `day` DESC
                LIMIT 20
            ) as `sl`
        ORDER BY `sl`.`day` ASC
        """

    def get_last_scheduled_date(self):
        cursor = self.db.cursor()
        cursor.execute(self.select_last_scheduled_date)
        result = cursor.fetchall()
        return result[0][0].strftime("%Y-%m-%d")

    def get_last_ten_sos_days(self):
        cursor = self.db.cursor()
        cursor.execute(self.select_last_ten_sos_days)
        result = cursor.fetchall()

        last_ten_days = {}
        for date, department_id, member_id in result:
            if not last_ten_days.get(date):
                last_ten_days[date] = []
            last_ten_days[date].append(member_id)
        return last_ten_days


class SchedulePlanningDAO(DAO):
    query = """INSERT INTO `sos_schedule` (`day`, `department_id`, `user_id`) VALUES (%s, %s, %s);"""

    def add_sos(self, date, department_id, user_id):
        cursor = self.db.cursor()
        try:
            cursor.execute(self.query, (date, department_id, user_id))
            self.db.commit()
        except:
            self.db.rollback()
