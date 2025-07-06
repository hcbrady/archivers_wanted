import requests
from django.core.management.base import BaseCommand
from participation.models import Opportunity, Tag
from dotenv import load_dotenv
import os

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"}
ORG_NAME = "internetarchive"

class Command(BaseCommand):
    help = 'Import repositories from Internet Archive that have open issues'

    def handle(self, *args, **kwargs):
        repos = self.fetch_all_repositories()
        repos_with_open_issues = [repo for repo in repos if repo.get("has_issues", False) and repo.get("open_issues_count", 0) > 0]

        for repo in repos_with_open_issues:
            self.create_or_update_repository_opportunity(repo)

        self.stdout.write(self.style.SUCCESS(f"Imported {len(repos_with_open_issues)} repositories with open issues."))

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

    def create_or_update_repository_opportunity(self, repo):
        """Create or update an Opportunity from the repo info."""
        full_name = repo.get('full_name') or ""
        title = f"Contribute code to this repo: {full_name}"
        description = repo.get('description') or ""
        issue_count = repo.get("open_issues_count", 0)
        url = repo["html_url"]
        summary = (
            f"<b>Repo description on GitHub:</b> {description}</br>"
            f"<b>Number of Open Issues:</b> {issue_count}</br><br>"
            f"Learn more <a target='_blank' href={url}>here</a>."
        )
        language = repo.get("language")

        opportunity, created = Opportunity.objects.update_or_create(
            title=title,
            defaults={
                "summary": summary,
            },
        )
        if language:
            tag, _ = Tag.objects.get_or_create(name=language, defaults={'category': 'Skill'})
            opportunity.tags.add(tag)
        if created:
            self.stdout.write(f"Created Opportunity for repo: {title}")
        else:
            self.stdout.write(f"Updated Opportunity for repo: {title}")
