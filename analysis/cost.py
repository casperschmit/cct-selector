from datetime import datetime


def compute_cost_score(project, devsupport_score, repo):
    score = 0
    team_experience = project.team_experience
    team_size = project.team_size

    if repo:
        # Check if repo older than 365 days
        if abs(repo.created_at - datetime.now()).days >= 365:
            score += 1

    # Check team experience
    score += team_experience

    if 4 <= team_size <= 10:
        score += 1

    # Increment with devsupport score
    score += devsupport_score

    return score
