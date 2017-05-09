import MySQLdb
from ..models.member import Member


QUERY = """
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


def get_members_for_sos_generator():
    db = MySQLdb.connect(host="127.0.0.1", user="root", passwd="kaka1234", db="sosnatet_1")
    c = db.cursor()
    c.execute(QUERY)
    result = c.fetchall()

    members = []
    for id, first_name, last_name, sos_percentage, family_id in result:
        m = Member(id=id, first_name=first_name, last_name=last_name, sos_percentage=sos_percentage, family=family_id)
        members.append(m)

    return members
