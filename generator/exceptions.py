class DeadlockInGenerationError(Exception):
    pass


class NotPossibleToGenerateSosError(Exception):
    pass


class TooManyMembersOnDayError(Exception):
    pass


class BadDistributionBetweenDepartmentsError(Exception):
    pass


class DepartmentNotAvailableError(Exception):
    pass
