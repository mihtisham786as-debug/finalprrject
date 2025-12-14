class User:
    def __init__(self, username, role):
        self.username = username
        self.role = role


class SecurityIncident:
    def __init__(self, category, severity, status, resolution_time):
        self.category = category
        self.severity = severity
        self.status = status
        self.resolution_time = resolution_time


class Dataset:
    def __init__(self, name, size_mb, rows, source):
        self.name = name
        self.size_mb = size_mb
        self.rows = rows
        self.source = source


class ITTicket:
    def __init__(self, staff, status, resolution_time):
        self.staff = staff
        self.status = status
        self.resolution_time = resolution_time