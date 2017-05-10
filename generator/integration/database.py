import MySQLdb


class DAO:
    def __init__(self):
        self.db = MySQLdb.connect(host="127.0.0.1", user="root", passwd="kaka1234", db="sosnatet_1")

    def _run(self):
        cursor = self.db.cursor()
        cursor.execute(self.query)
        return cursor.fetchall()


class ClosedDaysDAO(DAO):
    query = """SELECT sc.`theDay` FROM `scheduleClosed` sc WHERE sc.`theDay` > CURDATE()"""

    def get_closed_days(self):
        result = self._run()

        closed_days = []
        for day in result:
            closed_days.append(day[0].strftime("%Y-%m-%d"))
        return closed_days
    

class MembersDAO(DAO):
    query = """
            SELECT
                `member`.`id`,
                `member`.`firstname`,
                `member`.`lastname`,
                `member`.`sosPercentage`,
                `member`.`dateEnd`,
                `families`.`groupID`
            FROM
                `member`,
                (SELECT
                        `member_group`.`memberID`,
                        `member_group`.`groupID`
                    FROM `group`, `member_group`
                    WHERE
                        `group`.`id`=`member_group`.`groupID`
                        AND `group`.`type`=1
                ) AS `families`
            WHERE
                `member`.`id`=`families`.`memberID`
                AND `member`.`isActive`=1
                AND `member`.`isChild`=0
                AND `member`.`sosPercentage`>0;
            """

    def get_members_for_sos_generator(self):
        result = self._run()

        members = []
        for id, first_name, last_name, sos_percentage, end_date, family_id in result:
            members.append({
                "id": id,
                "first_name": first_name,
                "last_name": last_name,
                "sos_percentage": sos_percentage,
                "end_date": end_date,
                "family": family_id
            })
        return members


class ScheduleLiveDAO(DAO):
    query = """SELECT DATE(MAX(sl.`theDay`)) FROM `scheduleLive` sl"""

    def get_last_scheduled_date(self):
        result = self._run()
        return result[0][0].strftime("%Y-%m-%d")


class SchedulePlanningDAO(DAO):
    query = """INSERT INTO `schedulePlanning` (`theDay`, `departmentID`, `memberID`) VALUES (%s, %s, %s);"""

    def add_sos(self, date, department_id, member_id):
        cursor = self.db.cursor()
        try:
            cursor.execute(self.query, (date, department_id, member_id))
            self.db.commit()
        except:
            self.db.rollback()


class Group:
    def __init__(self, name, type):
        self.name = name
        self.type = type


class GroupDAO(DAO):
    query = """SELECT * FROM `group`"""

    def get_groups(self):
        result = self._run()
        groups = {}
        for id, name, type in result:
            groups[id] = Group(name, type)

        return groups
