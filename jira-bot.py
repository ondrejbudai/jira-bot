import argparse
import os

from jira import JIRA

JIRA_SERVER = os.getenv("JIRA_SERVER", "https://issues.redhat.com")
DEFAULT_PROJECT_KEY = os.getenv("DEFAULT_PROJECT_KEY", "HMS")
DEFAULT_ISSUE_TYPE = os.getenv("DEFAULT_ISSUE_TYPE", "Task")
DEFAULT_COMPONENT = os.getenv("DEFAULT_COMPONENT", "Image Builder")


def create_jira_task(token, project_key, summary, description, issuetype, epic_link, component):
    options = {
        'server': JIRA_SERVER,
        'headers': {
            'Authorization': f'Bearer {token}'
        }
    }
    try:
        jira = JIRA(options=options)
        print("Connected to Jira successfully using a personal access token.")
    except Exception as e:
        print(f"Failed to connect to Jira: {e}")
        return
    # Task creation dictionary
    issue_dict = {
        'project': {'key': project_key},
        'summary': summary,
        'description': description,
        'issuetype': {'name': issuetype},
    }

    # Add epic link if provided
    if epic_link:
        issue_dict['customfield_12311140'] = epic_link

    # Add component if provided
    if component:
        issue_dict['components'] = [{'name': component}]

    try:
        new_issue = jira.create_issue(fields=issue_dict)
        print(f"Task created successfully: {new_issue.key}")
        #TODO: Update pull request title with the new Jira issue key
    except Exception as e:
        print(f"Failed to create task: {e}")


def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Create a Jira task.")
    parser.add_argument('--token', required=True, help="The Jira personal access token")
    parser.add_argument('--project-key', default=DEFAULT_PROJECT_KEY, help=f"The Jira project id (optional, default: {DEFAULT_PROJECT_KEY})")
    parser.add_argument('--summary', required=True, help="The summary of the task.")
    parser.add_argument('--description', required=True, help="The description of the task.")
    parser.add_argument('--issuetype', default=DEFAULT_ISSUE_TYPE, help=f"The issue type id (optional, default: {DEFAULT_ISSUE_TYPE})")
    parser.add_argument('--epic-link', help="The epic link (optional, e.g. 'HMS-123')")
    parser.add_argument('--component', default=DEFAULT_COMPONENT, help=f"The component (default: '{DEFAULT_COMPONENT}').")

    args = parser.parse_args()

    # Call the task creation function with parsed arguments
    create_jira_task(
        token=args.token,
        project_key=args.project_key,
        summary=args.summary,
        description=args.description,
        issuetype=args.issuetype,
        epic_link=args.epic_link,
        component=args.component
    )


if __name__ == "__main__":
    main()

