# Site Generator

A static site generator. I use this for my personal website on [https://rbtms.github.io](https://rbtms.github.io).

## Requirements

```pypandoc``` for converting blog posts from Markdown to HTML.

## Project Structure

```
.
├── generate.sh          # Convenience script that runs generate.py with a given virtual environment
├── README.md            # This file
├── site/
├──── assets/              # Static assets
├──── blogposts/           # Markdown files for blog posts
├──── templates/           # Incomplete HTML templates with placeholders
├──── partials/            # Reusable template fragments
├──── build/               # Final static output
├──── generate.py          # Entrypoint
└── unused_docs/         # Documents not used in the final build but related to the website

```

## Blogpost headers

```
<!-- date: Date of the blog post -->
<!-- title: Title of the blog post -->
```

## License

MIT License.
