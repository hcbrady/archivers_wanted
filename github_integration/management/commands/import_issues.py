import requests
from django.core.management.base import BaseCommand
from participation.models import Opportunity
from django.utils import timezone
from dotenv import load_dotenv
import os

load_dotenv()  # Load .env variables

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"}
ORG_NAME = "internetarchive"


class Command(BaseCommand):
    help = 'Import open GitHub issues from Internet Archive'

    def handle(self, *args, **kwargs):
        repos = self.fetch_all_repositories()
        for repo in repos:
            if not repo.get("has_issues", False):
                self.stdout.write(f"Skipping {repo['full_name']} (issues disabled)")
                continue
            self.import_issues_from_repo(repo)

    def fetch_all_repositories(self):
        """Fetch all repositories from the org."""
        repos = []
        page = 1
        while True:
            url = f"https://api.github.com/orgs/{ORG_NAME}/repos?per_page=100&page={page}"
            response = requests.get(url, headers=GITHUB_HEADERS)
            if response.status_code != 200:
                self.stderr.write(f"Failed to fetch repositories: {response.text}")
                break
            page_repos = response.json()
            if not page_repos:
                break
            repos.extend(page_repos)
            page += 1
        return repos

    def import_issues_from_repo(self, repo):
        """Import all open issues from a single repo."""
        full_name = repo["full_name"]
        issues_url = f"https://api.github.com/repos/{full_name}/issues"

        response = requests.get(issues_url, headers=GITHUB_HEADERS)
        if response.status_code != 200:
            self.stderr.write(f"Failed to fetch issues from {full_name}: {response.text}")
            return

        issues = response.json()
        issue_titles = []

        for issue in issues:
            if "pull_request" in issue:
                continue  # Skip pull requests
            opportunity = self.create_or_update_opportunity(issue)
            issue_titles.append(opportunity.title)

        # Optional: Clean up old issues no longer in GitHub
        Opportunity.objects.exclude(title__in=issue_titles).delete()

        self.stdout.write(self.style.SUCCESS(f"Imported issues from {full_name}"))

    def create_or_update_opportunity(self, issue):
        """Create or update a local Opportunity object from a GitHub issue."""
        title = issue["title"]
        summary = issue.get("body", "") or ""
        url = issue["html_url"]

        opportunity, created = Opportunity.objects.update_or_create(
            title=title,
            defaults={"summary": summary},
        )
        return opportunity

