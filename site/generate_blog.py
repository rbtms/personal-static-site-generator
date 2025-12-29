#!/usr/bin/python3
#
# Script to generate blog.html and the individual blog posts
#
import os
import shutil
import pypandoc
from constants import *
from utils import add_indentation_to_every_line


def extract_headers_from_markdown(content: str) -> dict:
    """Extract headers from markdown content."""
    headers = {}
    lines = content.split('\n')

    # Look for header comments at the beginning of the file
    for line in lines:
        # Extract key-value pairs from header comments
        if line.startswith('<!-- ') and ':' in line:
            header_content = line.removeprefix('<!-- ').removesuffix(' -->')
            key_value = header_content.split(':')

            key = key_value[0].strip()
            value = ':'.join(key_value[1:]).strip()
            headers[key] = value
        # Stop when we hit the first non-header line
        else:
            break

    return headers

def read_blogposts_from_folder(path_blogpost_folder: str) -> list:
    """Read all markdown files from the blogpost folder and return list of blogposts."""
    blogposts = []

    for filename in sorted(os.listdir(path_blogpost_folder)):
        if filename.endswith('.md'):
            file_path = os.path.join(path_blogpost_folder, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Extract headers from the markdown file
            headers = extract_headers_from_markdown(content)

            # Create blogpost object with headers and content
            blogpost = {
                'headers': headers,
                'content': content,
                'filename': filename,
                'path_md': file_path
            }
            blogposts.append(blogpost)

    # Sort by date
    blogposts = sorted(blogposts, key=lambda _: _['headers']['date'],
                       reverse=True)
#
    return blogposts

def make_header_html(blogpost_json):
    """Create HTML header element for a blogpost."""
    filename = blogpost_json['filename']
    headers = blogpost_json['headers']

    # Extract date from headers
    date = headers.get('date', '')

    # Create the HTML element
    html = '<div class="blogpost-header">\n'
    html += f'  <span class="blogpost-date">{date}</span>\n'
    html += f'  <a class="blogpost-link" href="./{BLOG_BUILD_FOLDER_NAME}/{filename.replace(".md", ".html")}">{headers.get("title", "Untitled")}</a>\n'
    html += '</div>\n'

    return html

def replace_blogpost_headers(template_content: str, path_blogpost_folder, indentation_length: int) -> str:
    # Read all blogposts from the folder
    full_path_blogpost_folder = os.path.join(SCRIPT_FOLDER, path_blogpost_folder)
    blogposts_json = read_blogposts_from_folder(full_path_blogpost_folder)

    # Convert blogposts to JSON string
    blogpost_headers_content = ''
    for json_entry in blogposts_json:
        blogpost_headers_content += make_header_html(json_entry)

    blogpost_headers_content = add_indentation_to_every_line(blogpost_headers_content, indentation_length)

    # Replace placeholder in template with JSON content
    return template_content.replace(
        f'{TEMPLATE_TAG_START}{BLOGPOSTS_TAG}{path_blogpost_folder}{TEMPLATE_TAG_END}',
        # For some reason it inserts double indentation in the first entry. This
        # removes it.
        blogpost_headers_content[indentation_length:],
        1
    )

# ---- Convert markdown to html ----

def create_build_blog_folder(build_blog_dir: str):
    if os.path.exists(build_blog_dir):
        shutil.rmtree(build_blog_dir)

    os.mkdir(build_blog_dir)

def convert_markdown_to_html(blog_entry: dict, build_blog_dir: str):
    replace_tag = f'<!-- {BLOGPOST_TAG}content -->'

    path_output = os.path.join(build_blog_dir, blog_entry["filename"].replace(".md", ".html"))
    html_output = pypandoc.convert_file(blog_entry['path_md'], 'html',
                          extra_args=["--strip-comments"])

    generic_blogpost_path = os.path.join(BUILD_FOLDER,
                                         BLOGPOST_GENERIC_FILENAME.replace(TEMPLATE_EXTENSION, '.html'))
    generic_blogpost_content = open(generic_blogpost_path, 'r', encoding='utf8').read()
    blog_html = generic_blogpost_content.replace(replace_tag, html_output)

    open(path_output, 'w', encoding='utf8').write(blog_html)

def parse_blogposts():
    # Read all blogposts from the folder
    path_blogpost_dir = os.path.join(SCRIPT_FOLDER, BLOGPOST_FOLDER_NAME)
    build_blog_dir = os.path.join(BUILD_FOLDER, 'blog')

    blogposts_json = read_blogposts_from_folder(path_blogpost_dir)
    create_build_blog_folder(build_blog_dir)

    for entry in blogposts_json:
        convert_markdown_to_html(entry, build_blog_dir)
