import os

BLOG_BUILD_FOLDER_NAME = 'blog'
BLOGPOST_FOLDER_NAME = 'blogposts'

SCRIPT_FOLDER = os.path.dirname(__file__)
BUILD_FOLDER     = os.path.join(SCRIPT_FOLDER, '..', 'build')
BUILD_BLOG_FOLDER = os.path.join(BUILD_FOLDER, BLOG_BUILD_FOLDER_NAME)
ASSETS_FOLDER    = os.path.join(SCRIPT_FOLDER, 'assets')
TEMPLATES_FOLDER = os.path.join(SCRIPT_FOLDER, 'templates')
PARTIALS_FOLDER  = os.path.join(SCRIPT_FOLDER, 'partials')

TEMPLATE_EXTENSION = '.html'
# Spaces are mandatory
TEMPLATE_TAG_START = '<!-- '
TEMPLATE_TAG_END = ' -->'
REPLACE_TAG = 'replace:'
PROJECTS_TAG = 'projects:'
BLOGPOSTS_TAG = 'blogposts:'
BLOGPOST_TAG = 'blogpost:'

BLOGPOST_GENERIC_FILENAME = f'blogpost_generic{TEMPLATE_EXTENSION}'