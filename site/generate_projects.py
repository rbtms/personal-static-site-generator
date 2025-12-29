#!/usr/bin/python3
#
# Script to generate projects.html
#
import os
import json
from constants import *
from utils import add_indentation_to_every_line

def make_project(json_entry: dict) -> str:
    """
    Generates HTML for a project based on the provided JSON data.

    Args:
        json_entry (dict): A dictionary containing project data (name, repo, imgurl, videourl, desc).

    Returns:
        str: The HTML string representing the project.
    """
    return f"""<div class="project">
    <span class="project-title"> {json_entry['name']}
        <a href='{json_entry['repo']}'>
            <img class="github-link" src='assets/img/github-mark-white.png'>
        </a>
    </span>
    {
        f'<img class="project-pic" src="{json_entry["imgurl"]}"/>'
        if 'imgurl' in json_entry else
        f'<video class="project-pic" src="{json_entry["videourl"]}"controls> </video>'
    }
    <span class="project-desc">{json_entry['desc']}</span>
</div>
"""

def replace_projects(template_content: str, json_filename: str, indentation_length: int) -> str:
    """
    Replaces a placeholder in the template with generated HTML for a list of projects.

    Args:
        template_content (str): The content of the template where replacements need to be made.
        json_filename (str): The name of the JSON file containing project data.
        indentation_length (int): The indentation to apply to the generated project HTML.

    Returns:
        str: The updated template content after replacing the placeholder with project HTML.
    """
    json_content = json.load(open(os.path.join(TEMPLATES_FOLDER, json_filename), 'r', encoding='utf-8'))
    projects_content = ''

    for json_entry in json_content:
        projects_content += make_project(json_entry)

    projects_content = add_indentation_to_every_line(projects_content, indentation_length)

    return template_content.replace(
        f'{TEMPLATE_TAG_START}{PROJECTS_TAG}{json_filename}{TEMPLATE_TAG_END}',
        # For some reason it inserts double indentation in the first entry. This
        # removes it.
        projects_content[indentation_length:],
        1
    )
