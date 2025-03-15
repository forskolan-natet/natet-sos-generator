class Properties:
    def __init__(self, path):
        self.members_path = None
        self.previous_schema = None
        self.closed_days_path = None
        self.extra_sos_to = []
        self.less_sos_to = []
        self.min_nr_of_days_between_sos = 12

        properties_file = open(path, "r")
        for line in properties_file:
            if line.startswith("member_file="):
                self.members_path = line.strip().split("=")[1]
            elif line.startswith("previous_schedule="):
                self.previous_schema = line.strip().split("=")[1]
            elif line.startswith("closed_days="):
                self.closed_days_path = line.strip().split("=")[1]
            elif line.startswith("extra_sos_to="):
                self.extra_sos_to = map(int, line.strip().split("=")[1].split(","))
            elif line.startswith("less_sos_to="):
                self.less_sos_to = map(int, line.strip().split("=")[1].split(","))
            elif line.startswith("min_nr_of_days_between_sos="):
                self.min_nr_of_days_between_sos = int(line.strip().split("=")[1])
        properties_file.close()
