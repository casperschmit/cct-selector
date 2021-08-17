from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor, defer
from scrapy.utils.log import configure_logging
from datetime import datetime
from operator import itemgetter

from get_database import get_database
from database import db_manager
from search.search import keyword_search_handler

from analysis.cost import compute_cost_score
from analysis.security import compute_security_score
from analysis.compatibility import compute_compatibility_score
from analysis.dev_support import GitSpider
from analysis.complexity import compute_complexity, get_most_starred, get_git_repos, get_git_org
# from cost import compute_cost_score
# from security import compute_security_score
# from compatibility import compute_compatibility_score
# from dev_support import GitSpider
# from complexity import compute_complexity, get_most_starred, get_git_repos, get_git_org

from flaskdss import db
from flaskdss.models import Project, Attributes, CCT
from flask_login import current_user

import pickle
import pathlib
import pandas as pd




def interpret_license(license_key):
    if license_key == 'apache-2.0':
        return 1
    elif license_key == 'mit':
        return 1
    elif license_key == 'gpl' or license_key == 'gpl-2.0' or license_key == 'gpl-3.0' or 'lgpl-3.0':
        return 1
    else:
        return 0


def days_between(d1, d2):
    days = abs((d2 - d1).days)
    return days


def compute_devsupport(wp, docs, repo, org):
    score = 0

    wp_docs_score = 0
    email_score = 0
    license_score = 0
    issue_score = 0
    latest_commit_score = 0

    # WP or Docs present
    if wp is not None or docs is not None:
        wp_docs_score = 1

    if repo:
        # Open source license present
        try:
            # Get license from most starred repository
            license_key = repo.get_license().license.key
            license_score = interpret_license(license_key)
        except Exception as e:
            pass

        # Closed issues greater than 50%
        closed_issues = repo.get_issues(state='closed').totalCount
        open_issues = repo.open_issues

        # Check if greater than 50% of issues are closed
        if (open_issues + closed_issues > 0):
            if (closed_issues / (open_issues + closed_issues)) > 0.5:
                issue_score = 1

        # Check if email address is present
        if org.email:
            email_score = 1

        # Check if latest commit was less than three months ago
        commits = repo.get_commits()
        commit = commits[0]
        date_str = commit.last_modified.split(", ")[1]
        date_time_obj = datetime.strptime(date_str, '%d %b %Y %H:%M:%S %Z')
        if days_between(date_time_obj, datetime.now()) <= (3 * 30):
            latest_commit_score = 1

    score = latest_commit_score + email_score + wp_docs_score + license_score + issue_score
    return score


def compute_attributes(weights):
    computed_attributes = {}

    # get database from google sheets (deprecated)
    # df = get_database()

    # Get database from AWS
    connector = db_manager.DBconnect()
    df = db_manager.get_df(connector.connect(), 'cct')

    # df = pd.read_excel('/Users/casper/PycharmProjects/semantic-search/search/kb-input-test.xlsx')

    # Get Wizard input
    wizard_answers = Project.query.filter_by(user=current_user.id).first()

    # Relevancy search
    input_content = wizard_answers.description
    relevancy = keyword_search_handler(df, 'scrape', 50, False, input_content) # Search without recalibration
    # relevancy = {'Cosmos': 5.827898232597742}
    print(relevancy)
    for index, row in df.iterrows():  # df.iloc[1:].iterrows():
        print(row)

        git_link = row.github
        name = row[1]
        wp = row.whitepaper
        docs = row.docs

        if git_link:
            repo = get_most_starred(get_git_repos(git_link), [])
            devsupport_score = compute_devsupport(wp, docs, repo, get_git_org(git_link))
            complexity_score = compute_complexity(row.id, git_link, current_user.id)  # Compute complexity
            cost_score = compute_cost_score(wizard_answers, 2, repo)
        else:
            devsupport_score = compute_devsupport(wp, docs, None, None)
            complexity_score = 0
            cost_score = compute_cost_score(wizard_answers, 2, None)

        security_score = compute_security_score(row)
        compatibility_score = compute_compatibility_score(row, wizard_answers)

        if name in relevancy:
            relevancy_score = relevancy[str(name)]
        else:
            relevancy_score = 0

        cct = CCT.query.filter_by(name=name, whitepaper=wp).first()
        table_entry = Attributes.query.filter_by(cct=cct.id, user=current_user.id).first()
        if table_entry:
            table_entry.cost = cost_score
            table_entry.compatibility = compatibility_score
            table_entry.relevancy = relevancy_score
            table_entry.complexity = complexity_score
            table_entry.security = security_score
            table_entry.dev_support = devsupport_score
            db.session.commit()
        else:
            attributes = Attributes(
                cct=cct.id,
                user=current_user.id,
                cost=cost_score,
                compatibility=compatibility_score,
                relevancy=round(relevancy_score, 2),
                complexity=complexity_score,
                security=security_score,
                dev_support=devsupport_score
            )
            db.session.add(attributes)
    db.session.commit()

    compute_aggregated_score(weights)
    return True


def compute_aggregated_score(weights):
    output_list = Attributes.query.filter_by(user=current_user.id).all()

    max_cost = 10
    max_compatibility = 9
    max_devsupport = 5
    max_security = 5

    sum_relevancy = 0
    for item in output_list:
        sum_relevancy += item.relevancy

    print(sum_relevancy)

    for item in output_list:
        item.aggregated = ((item.relevancy / sum_relevancy) * weights.relevancy_weight.data) + \
                          ((item.cost / max_cost) * weights.cost_weight.data) + \
                          ((item.compatibility / max_compatibility) * weights.compatibility_weight.data) + \
                          (item.complexity * weights.complexity_weight.data) + \
                          ((item.security / max_security) * weights.security_weight.data) + \
                          ((item.dev_support / max_devsupport) * weights.devsupport_weight.data)
        item.aggregated = round(item.aggregated, 2)
        db.session.commit()


def sort_output_table(output_list, sort_by):
    return sorted(output_list, key=itemgetter(sort_by), reverse=True)


def get_output_table():
    output_list = []
    results = Attributes.query.filter_by(user=current_user.id).all()
    for result in results:
        cct = CCT.query.filter_by(id=result.cct).first()
        output = {
            'name': cct.name,
            'cost': result.cost,
            'compatibility': result.compatibility,
            'relevancy': result.relevancy,
            'complexity': result.complexity,
            'security': result.security,
            'developer_support': result.dev_support,
            'aggregated': result.aggregated
        }

        output_list.append(output)

    return output_list

