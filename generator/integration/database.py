import MySQLdb
from ..models.member import Member


class DAO:
    def __init__(self, query):
        self.db = MySQLdb.connect(host="127.0.0.1", user="root", passwd="kaka1234", db="sosnatet_1")
        self.query = query

    def _run(self):
        cursor = self.db.cursor()
        cursor.execute(self.query)
        return cursor.fetchall()


class ClosedDaysDAO(DAO):
    query = """SELECT sc.`theDay` FROM `scheduleClosed` sc WHERE sc.`theDay` > CURDATE()"""

    def __init__(self):
        super().__init__(self.query)

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
                `member`.`sos_percentage`,
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
                AND `member`.`sos_percentage`>0;
            """

    def __init__(self):
        super().__init__(self.query)

    def get_members_for_sos_generator(self):
        result = self._run()

        members = []
        for id, first_name, last_name, sos_percentage, family_id in result:
            m = Member(id=id, first_name=first_name, last_name=last_name, sos_percentage=sos_percentage, family=family_id)
            members.append(m)
        return members
