
from alerta.app import severity
from alerta.models import severity_code, status_code


def status_from_severity(previous_severity, current_severity, previous_status=status_code.OPEN, current_status=status_code.UNKNOWN):
    if current_severity in [severity_code.NORMAL, severity_code.CLEARED, severity_code.OK]:
        return status_code.CLOSED
    if current_status in [status_code.BLACKOUT, status_code.SHELVED]:
        return current_status
    if previous_status in [status_code.BLACKOUT, status_code.CLOSED, status_code.EXPIRED]:
        return status_code.OPEN
    if severity.trend(previous_severity, current_severity) == severity_code.MORE_SEVERE:
        return status_code.OPEN
    return previous_status
