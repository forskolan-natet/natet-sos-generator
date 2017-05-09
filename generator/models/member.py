class Member:
    id = 0

    def __init__(self, id=None, first_name="", last_name="", sos_percentage=100, family=0, sponsor_for_family=None,
                 sponsored_by_family=None):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.sos_percentage = sos_percentage
        self.family = family
        self.sponsor_for_family = sponsor_for_family
        self.sponsored_by_family = sponsored_by_family

    @property
    def name(self):
        return self.first_name + " " + self.last_name

    @property
    def is_sponsor(self):
        return self.sponsor_for_family is not None

    @property
    def is_sponsored(self):
        return self.sponsored_by_family is not None

    def __repr__(self):
        return "<%s %s (sos:%s)>" % (self.first_name, self.last_name, self.sos_percentage)
