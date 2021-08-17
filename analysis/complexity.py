import subprocess
from urllib.parse import urlparse

from github import Github
from git import Repo
import os
import ast
import shutil
from pathlib import Path
import math
import pandas as pd
from application import ROOT_DIR
from flask_login import current_user

github_token = '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'


def get_most_starred(repos, previous):
    max_count = 0
    most_starred = None
    for repo in repos:
        if repo not in previous and repo.stargazers_count > max_count:
            most_starred = repo
            max_count = repo.stargazers_count

    return most_starred


def get_git_repos(org_url):
    org = get_git_org(org_url)
    repos = org.get_repos()
    return repos


def get_git_org(org_url):
    git = Github(github_token)
    org = urlparse(org_url).path[1:]
    if org[-1] == '/':  # Check if provided url does not end with a slash, otherwise it won't work
        org = org[0:-1]
    org = git.get_organization(org)
    return org


def download_git_repo(git_url, temp_path):
    Path(temp_path).mkdir(parents=True, exist_ok=True)
    # print(os.getcwd())
    os.chdir(ROOT_DIR)
    Repo.clone_from(git_url, temp_path)


def complexity_check(path):
    os.chdir(path)
    sub = subprocess.run(["/opt/homebrew/Cellar/complexity/0.3.0/bin/complexity", "--format", "json"],
                         stdout=subprocess.PIPE)
    output = sub.stdout
    dict_str = output.decode("UTF-8")
    mydata = ast.literal_eval(dict_str)
    return mydata


def clear_dir(path):
    if Path(path).exists():
        shutil.rmtree(path)


def lizard_complexity_check(output_path):
    subprocess.run(["lizard", "--csv", "-o", ROOT_DIR + "/lizard.csv", output_path])


def interpret_lizard(output_file):
    count = 0
    total_cc = 0
    bad = 0
    chunksize = 10 ** 8

    try:
        for chunk in pd.read_csv(output_file, chunksize=chunksize):
            for index, row in chunk.iterrows():
                if int(row[1]) >= 15:
                    bad += 1
                total_cc += int(row[1])
                count += 1
    except pd.errors.EmptyDataError as e:
        return -1

    denominator = math.sqrt(count)
    # return bad / denominator * 100.0
    # return total_cc / count
    return bad / count
    # return total_cc - count + 1


def average_complexity(data):
    complexity = 0
    count = 0
    for f in data.keys():
        complexity += data[f]
        count += 1

    return complexity / count


def compute_complexity(git_link, user_id):
    temp_download_path = ROOT_DIR + '/' + str(user_id) + '/temp'
    most_starred_repo_empty = True
    nth_most_starred = 0
    previous_most_starred = []
    repos = get_git_repos(git_link)

    clear_dir(ROOT_DIR + '/' + str(user_id))

    while most_starred_repo_empty:
        most_starred_repo = get_most_starred(repos, previous_most_starred)
        url = most_starred_repo.clone_url
        print(url)
        download_git_repo(url, temp_download_path)
        lizard_complexity_check(temp_download_path)
        lizard_score = interpret_lizard(ROOT_DIR + "/lizard.csv")  # Cyclomatic complexity
        complexity_score = average_complexity(complexity_check(temp_download_path))  # Whitespace complexity

        if lizard_score == -1:
            most_starred_repo_empty = True
            nth_most_starred += 1
            previous_most_starred.append(most_starred_repo)
        else:
            most_starred_repo_empty = False

        clear_dir(ROOT_DIR + '/' + str(user_id))



    print("Lizard: " + str(lizard_score))
    print("Complexity: " + str(complexity_score))
    return lizard_score

