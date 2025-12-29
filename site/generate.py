#!/usr/bin/python3
#
# Script to generate the website
#

import os
import shutil
from constants import *
from generate_projects import replace_projects
from generate_blog import replace_blogpost_headers, parse_blogposts
from utils import add_indentation_to_every_line


def copy_assets():
    """
        Copies all assets from the ASSETS_FOLDER to the BUILD_FOLDER/assets directory.
        If the BUILD_FOLDER/assets directory already exists, it is deleted before copying.
    """
    build_assets_dir = os.path.join(BUILD_FOLDER, 'assets')

    if os.path.exists(build_assets_dir):
        shutil.rmtree(build_assets_dir)

    shutil.copytree(ASSETS_FOLDER, build_assets_dir)

def replace_partial(template_content: str, partial_filename: str, indentation_length: int) -> str:
    """
    Replace placeholders in template content with content from a partial file.

    Args:
        template_content (str): The content of the template where replacements need to be made.
        partial_filename (str): The name of the partial file containing the content to insert.

    Returns:
        str: The updated template content after replacing the placeholder with the partial content.

    Raises:
        ValueError: If the specified partial file does not exist.

    Description:
        This function takes the content of a template and replaces placeholders like <!-- replace:<FILE> -->
        with the content from a corresponding partial file. It reads the partial file, replaces the placeholder
        in the template content, and returns the updated template.
    """
    partial_path = os.path.join(PARTIALS_FOLDER, partial_filename)

    if os.path.exists(partial_path):
        with open(partial_path, 'r', encoding='utf8') as partial_file:
            partial_content = partial_file.read()

            # Indentate partial
            partial_content = add_indentation_to_every_line(partial_content, indentation_length)

            # Replace the placeholder with the content from the partial file
            template_content = template_content.replace(
                f'{TEMPLATE_TAG_START}{REPLACE_TAG}{partial_filename}{TEMPLATE_TAG_END}',
                # For some reason it inserts double indentation in the first entry. This
                # removes it.
                partial_content[indentation_length:],
                1
            )
    else:
        raise ValueError(f'Partial path doesn\'t exist: {partial_path}')

    return template_content

def recreate_build_folder(build_folder: str) -> None:
    """Delete the build folder if it exists and recreate it."""
    if os.path.exists(build_folder):
        shutil.rmtree(build_folder)

    os.makedirs(build_folder)

def replace_template(filename: str):
    """
    Replace placeholders in a template file with content from partial files.

    Args:
        filename (str): The name of the template file to process.
    """
    tags = [REPLACE_TAG, PROJECTS_TAG, BLOGPOSTS_TAG]
    tag_functions = {
        REPLACE_TAG: replace_partial,
        PROJECTS_TAG: replace_projects,
        BLOGPOSTS_TAG: replace_blogpost_headers
    }

    # Open and read the contents of the template file
    with open(os.path.join(TEMPLATES_FOLDER, filename), 'r', encoding='utf8') as template_file:
        template_content = template_file.read()

    # Find all placeholders in the template content that need replacement
    for line in template_content.split('\n'):
        for tag in tags:
            if line.strip().startswith(TEMPLATE_TAG_START + tag)\
                and line.strip().endswith(TEMPLATE_TAG_END):
                replace_tag_end = len(TEMPLATE_TAG_START) + len(tag)
                partial_filename = line.strip()[replace_tag_end:][:-len(TEMPLATE_TAG_END)]
                tag_indentation = len(line.split('<')[0])

                template_content = tag_functions[tag](template_content, partial_filename, tag_indentation)

    # Write the modified template content to the build directory
    output_path = os.path.join(BUILD_FOLDER, filename)
    with open(output_path, 'w', encoding='utf8') as output_file:
        output_file.write(template_content)


def main():
    # Iterate through all files in the TEMPLATES_FOLDER and replace their placeholders
    template_files = os.listdir(TEMPLATES_FOLDER)
    recreate_build_folder(BUILD_FOLDER)

    # Priorize parsing blogpost_generic.html so that it can be further replaced by blog post parsing
    if BLOGPOST_GENERIC_FILENAME in template_files:
        template_files.remove(BLOGPOST_GENERIC_FILENAME)
        template_files = [BLOGPOST_GENERIC_FILENAME] + template_files

    for template_filename in template_files:
        if template_filename.endswith(TEMPLATE_EXTENSION):
            replace_template(template_filename)

    copy_assets()
    parse_blogposts()

    # Remove generated generic blogpost file
    generic_blogpost_path = os.path.join(BUILD_FOLDER,
                                         BLOGPOST_GENERIC_FILENAME.replace(TEMPLATE_EXTENSION, '.html'))
    if os.path.exists(generic_blogpost_path):
        os.remove(generic_blogpost_path)

main()
