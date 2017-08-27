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
                `id`,
                `firstname`,
                `lastname`,
                `sosPercentage`,
                `startDate`,
                `dateEnd`,
                `family_id`,
                `s1`.`newFamilyID` AS `sponsor_for_family`,
                `s2`.`sponsorFamilyID` AS `sponsored_by_family`
            FROM
                (
                    SELECT
                        `member`.`id`,
                        `member`.`firstname`,
                        `member`.`lastname`,
                        `member`.`sosPercentage`,
                        `member`.`startDate`,
                        `member`.`dateEnd`,
                        `families`.`groupID` as `family_id`
                    FROM
                        `member`,
                        (SELECT
                            `member_group`.`memberID`,
                            `member_group`.`groupID`
                        FROM
                            `group`,
                            `member_group`
                        WHERE
                            `group`.`id`=`member_group`.`groupID`
                            AND `group`.`type`=1) AS `families`
                    WHERE
                        `member`.`id`=`families`.`memberID`
                        AND `member`.`isActive`=1
                        AND `member`.`isChild`=0
                        AND `member`.`sosPercentage`>0
                ) as members
            LEFT JOIN `sponsor` AS `s1` ON `s1`.`sponsorFamilyID` = `members`.`family_id`
            LEFT JOIN `sponsor`AS `s2` ON `s2`.`newFamilyID` = `members`.`family_id`;
            """

    def get_members_for_sos_generator(self):
        result = self._run()

        members = []
        for id, first_name, last_name, sos_percentage, start_date, end_date, family_id, sponsor_for_family, \
                sponsored_by_family in result:
            members.append({
                "id": id,
                "first_name": first_name,
                "last_name": last_name,
                "sos_percentage": sos_percentage,
                "start_date": start_date,
                "end_date": end_date,
                "family": family_id,
                "sponsor_for_family": sponsor_for_family,
                "sponsored_by_family": sponsored_by_family
            })
        return members


class ScheduleLiveDAO(DAO):
    select_last_scheduled_date = """SELECT DATE(MAX(sl.`theDay`)) FROM `scheduleLive` sl"""
    select_last_ten_sos_days = """
        SELECT
            `sl`.`theDay`,
            `sl`.`departmentID`,
            `sl`.`memberID`
        FROM
            (
                SELECT
                    `theDay`,
                    `departmentID`,
                    `memberID`
                FROM
                    `scheduleLive`
                ORDER BY `theDay` DESC
                LIMIT 20
            ) as `sl`
        ORDER BY `sl`.`theDay` ASC
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
    query = """SELECT id, name, type FROM `group`"""

    def get_groups(self):
        result = self._run()
        groups = {}
        for id, name, type in result:
            groups[id] = Group(name, type)

        return groups


class SponsorDAO(DAO):
    query = """SELECT sponsorFamilyID, newFamilyID FROM `sponsor`"""

    def get_groups(self):
        result = self._run()
        sponsors = {}
        for sponsor_family_id, new_family_id in result:
            sponsors[sponsor_family_id] = new_family_id

        return sponsors
