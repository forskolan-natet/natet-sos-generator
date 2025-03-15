import pandas

class MembersExcel:
    # Sheet
    MEMBERS_SHEET = "Medlemmar"
    # Columns
    ID_COLUMN = "ID"
    NAME_COLUMN = "Namn"
    FAMILY_COLUMN = "Familj"
    GROUP_COLUMN = "Grupp"
    EXTRA_ROLE_COLUMN = "Extra roll"
    SPONSOR_FAMILY_COLUMN = "Fadderfamilj"
    START_DATE_COLUMN = "Startdatum"
    END_DATE_COLUMN = "Slutdatum"

    @staticmethod
    def read_member_dict(path_to_member_excel):
        members_from_excel = MembersExcel.parse_members(path_to_member_excel)
        members = []
        for member in members_from_excel:
            end_date = None
            if member.end_date is not None:
                end_date = member.end_date.date()
            members.append({
                "id": int(member.id),
                "first_name": member.name.split(" ")[0],
                "last_name": member.name.split(" ", 1)[1],
                "sos_percentage": member.sos_count() * 50,
                "start_date": member.start_date.date(),
                "end_date": end_date,
                "sponsored_by_member": MembersExcel.find_sponsor(member, members_from_excel),
                "partner_id": MembersExcel.find_partner_id(member, members_from_excel)
            })
        return members

    @staticmethod
    def find_partner_id(member, all_members):
        for m in all_members:
            if m.id != member.id and m.family == member.family:
                return int(m.id)
        raise Exception("No partner found...") 
    
    @staticmethod
    def find_sponsor(member, all_members):
        for m in all_members:
            if m.family == member.sponsor_family:
                return int(m.id)
        return None

    @staticmethod
    def parse_members(path_to_member_excel):
        data_frame = pandas.read_excel(path_to_member_excel, sheet_name=MembersExcel.MEMBERS_SHEET)

        members = []
        for i in data_frame.index:
            extra_role = data_frame.at[i, MembersExcel.EXTRA_ROLE_COLUMN]
            sponsor_family = data_frame.at[i, MembersExcel.SPONSOR_FAMILY_COLUMN]
            end_date = data_frame.at[i, MembersExcel.END_DATE_COLUMN]

            members.append(Member(data_frame.at[i, MembersExcel.ID_COLUMN],
                                   data_frame.at[i, MembersExcel.NAME_COLUMN],
                                   data_frame.at[i, MembersExcel.FAMILY_COLUMN],
                                   data_frame.at[i, MembersExcel.GROUP_COLUMN],
                                   extra_role if pandas.notna(extra_role) else None,
                                   sponsor_family if pandas.notna(sponsor_family) else None,
                                   data_frame.at[i, MembersExcel.START_DATE_COLUMN],
                                   end_date if pandas.notna(end_date) else None,)
             )

        return members

class Member:
    BOARD_MEMBER = "Styrelse"
    ECONOMY_GROUP = "Ekonomi"
    PERSONNEL_GROUP = "Personal"

    def __init__(self, member_id, name, family, group, extra_role, sponsor_family, start_date, end_date):
        self.id = member_id
        self.name = name
        self.family = family
        self.group = group
        self.extra_role = extra_role
        self.sponsor_family = sponsor_family
        self.start_date = start_date
        self.end_date = end_date

    def sos_count(self):
        if self.extra_role == Member.BOARD_MEMBER and (self.group == Member.ECONOMY_GROUP or self.group == Member.PERSONNEL_GROUP):
            return 0
        elif self.extra_role == Member.BOARD_MEMBER:
            return 1
        else:
            return 2
