import ast


def compute_compatibility_score(row, project):
    score = 0

    technical_fit = ast.literal_eval(project.technical_scheme)  # {'HTLC': 1, 'Hybrid': 2, 'Sidechain': 3, 'Notary': 0}
    usecase_fit = ast.literal_eval(
        project.use_case)  # {'Asset transfer': 1, 'Asset exchange': 2, 'Cross-chain smart contract': 3, 'Cross-chain oracle': 0}
    user_source = project.source_chain  # 'Ethereum'
    user_source_permission = project.source_permissions  # 'Permissionless public'
    user_target = project.target_chain  # 'Bitcoin'
    user_target_permission = project.target_permissions  # 'Permissionless public'

    current_source = row[5]
    current_source_permissions = row[6]
    current_target = row[7]
    current_target_permissions = row[8]
    current_technical_scheme = row[10]
    current_use_case = row[9]

    if current_source == user_source:
        score += 2

    if current_source_permissions == user_source_permission:
        score += 1

    if current_target_permissions == user_target_permission:
        score += 1

    if current_target == user_target:
        score += 2

    if current_technical_scheme in technical_fit:
        score += technical_fit[current_technical_scheme]

    if current_use_case in usecase_fit:
        score += usecase_fit[current_use_case]

    return score
