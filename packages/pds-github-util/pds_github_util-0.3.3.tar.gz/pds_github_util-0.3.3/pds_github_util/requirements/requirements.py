import os
import logging
import github3
import re
from mdutils import MdUtils
from pds_github_util.tags.tags import Tags

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)




class Requirements:

    def __init__(self, org, repo, token=None, dev=False):
        self._organization = org
        self._repository = repo
        self._dev = dev

        gh = github3.login(token=token)
        self._repo = gh.repository(self._organization, self._repository)
        self._requirements = self._get_requirements_from_issues()
        self._tags = Tags(org, repo, token=token)
        self._current_tag = self._tags.get_latest_tag(self._dev)
        self._requirements_tag_map = self._get_requirement_tag_map()

    def _get_requirements_from_issues(self):
        summary = {}

        for issue in self._repo.issues(state='all', direction='asc', labels='requirement'):
            topic_assigned = False
            for label in issue.labels():
                if label.name.startswith("requirement-topic"):
                    requirement_topic = label.name.split(':')[1]
                    if requirement_topic not in summary.keys():
                        summary[requirement_topic] = []
                    summary[requirement_topic].append({'number': issue.number,
                                                       'title': issue.title,
                                                       'link': issue.url})
                    topic_assigned = True
                    continue

        if not topic_assigned:
            if "default" not in summary.keys():
                summary["default"] = []
            summary["default"].append({'number': issue.number,
                                       'title': issue.title,
                                       'link': issue.url})

        return summary

    def _get_requirement_tag_map(self):

        requirements_issue_map = {}
        requirements_tag_map = {}
        for issue in self._repo.issues(state='closed', direction='asc'):
            body_sections = issue.body.split("**Applicable requirements")
            if len(body_sections) > 1:
                impacted_requirements_str = body_sections[1]
                prog = re.compile("#[0-9]+")
                requirements = prog.findall(impacted_requirements_str)
                requirements = [ int(req[1:]) for req in requirements] # remove leading # and convert to int to be consistent with requirement dictionnary
                for req in requirements:
                    if req not in requirements_tag_map.keys():
                        requirements_tag_map[req] = {'issues': set(),  'tags': set()}
                    issue_date_isoz = issue.closed_at.isoformat().replace('+00:00', 'Z')
                    earliest_tag_closed_after = self._tags.get_earliest_tag_after(issue_date_isoz)
                    requirements_tag_map[req]['issues'].add(issue.number)
                    requirements_tag_map[req]['tags'].add(earliest_tag_closed_after)
        return requirements_tag_map

    def get_requirements(self):
        return self._requirements

    @staticmethod
    def _version_paragraph_intro(versions_len):
        if versions_len == 0:
            return ''
        elif versions_len ==1:
            return 'The version implementing or impacting this requirement is:'
        else:
            return 'The versions implementing or impacting this requirement are:'

    def write_requirements(self, output_file_name=None):
        if output_file_name is None:
            output_file_name = os.path.join(self._current_tag, 'REQUIREMENTS.md')

        output_file_dir = os.path.dirname(output_file_name)
        if len(output_file_dir):
            os.makedirs(output_file_dir, exist_ok=True)
        requirements_md = MdUtils(file_name=output_file_name, title="Requirements Summary")

        for req_topic in self._requirements:
            requirements_md.new_header(level=1, title=req_topic)
            for req in self._requirements[req_topic]:
                impacted = self._current_tag in self._requirements_tag_map[req['number']]['tags'] if req['number'] in self._requirements_tag_map else False
                impacted_icon = ':boom:' if impacted else ''
                title = f"{req['title']} ([#{req['number']}](https://github.com/{self._repo}/issues/{req['number']})) {impacted_icon}"
                requirements_md.new_header(level=2, title=title)
                if impacted:
                    issue_lines = []
                    requirements_md.new_paragraph('The issues which impact the current requirements are:')
                    for n in self._requirements_tag_map[req['number']]['issues']:
                        issue = self._repo.issue(n)
                        issue_lines.append(f'{issue.title} ([#{n}](https://github.com/{self._repo}/issues/{n}))')
                    requirements_md.new_list(issue_lines)
                else:
                    requirements_md.new_paragraph('This requirement is not impacted by the current version')


        requirements_md.create_md_file()

        return output_file_name
