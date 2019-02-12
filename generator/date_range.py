from datetime import timedelta


def date_range(start, end):
    for n in range(int ((end - start).days)):
        yield start + timedelta(n)
