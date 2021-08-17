import re


def compute_security_score(row):
    score = 0

    technical_scheme = row[10]
    if technical_scheme == 'HTLC':
        score += 3
    elif technical_scheme == 'Sidechain':
        score += 2
    elif technical_scheme == 'Hybrid':
        score += 1
    elif technical_scheme == 'Notary':
        score += 0
    else:
        score += 0

    source_permission = row[6]
    target_permission = row[8]
    score += permission_score(source_permission)
    score += permission_score(target_permission)
    return score


def permission_score(scheme):
    match = re.search(r'\bpublic\b', scheme, re.IGNORECASE)
    if match:
        return 1
    else:
        return 0
