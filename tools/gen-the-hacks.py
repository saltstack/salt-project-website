'''
Generates markdown files into ../content/the-hacks/*.md

Parses info from: https://thehacks.libsyn.com/rss

Each temp Markdown file generates:

- Filename format: <episode-number>-<lowercase-title>.md
- Frontmatter
    - title (and first header): "<item.title>"
    - summary: "<item.itunes:subtitle>"
    - date: "<item.pubDate>" # Convert to format: "yyyy-mm-dd"
    - url: "/the-hacks/<lowercase-title>"
    - podcast_url: <item.enclosure url>.m4a # Trim anything after .m4a
    - length: "<item.itunes:duration>"
    - image: "<item.itunes:image>"
- Content
  - First header uses <title-case-title>
  - item.description (convert format from HTML -> Markdown format?)
'''
import re
import tomllib
from pathlib import Path

import feedparser # For parsing The Hacks RSS feed
import frontmatter # For formatting the Markdown file

# For converting HTML descriptions into Markdown format
from markdownify import markdownify as md


the_hacks_rss = feedparser.parse('https://thehacks.libsyn.com/rss')
the_hacks_path = Path('content/the-hacks/')

with open("config.toml", "rb") as f:
    the_hacks_config = tomllib.load(f)['the-hacks']

# Regex used for creating a filename with only alphabetic characters
file_title_regex = re.compile('[,\.!?\'\"()]')

episode_number = 1
for episode in reversed(the_hacks_rss['entries']):

    # Make sure episode number is three digits
    if len(str(episode_number)) < 3:
        if len(str(episode_number)) < 2:
            episode_number_value = f"00{episode_number}"
        else:
            episode_number_value = f"0{episode_number}"
    else:
        episode_number_value = str(episode_number)

    # Make sure month and day numbers are two digits
    if len(str(episode['published_parsed'].tm_mon)) == 1:
        published_month = f"0{episode['published_parsed'].tm_mon}"
    else:
        published_month = str(episode['published_parsed'].tm_mon)
    if len(f"{episode['published_parsed'].tm_mday}") == 1:
        published_day = f"0{episode['published_parsed'].tm_mday}"
    else:
        published_day = str(episode['published_parsed'].tm_mday)

    # Prep Markdown file with template
    post = frontmatter.load('tools/the-hacks-template.md')

    # All lowercase title with many special characters removed
    episode_file_title = file_title_regex.sub('', episode['title'].replace('/','').replace(':','').replace('\\','').replace('*','').replace('&','').replace(' ', '-').replace('--', '-')).lower()
    episode_subtitle = episode['subtitle'].replace('\xa0','')

    # Replace all frontmatter from RSS values, add title header, and content
    post['title'] = f"{episode['title']}"
    post['summary'] = f"{episode_subtitle}"
    post['date'] = f"{episode['published_parsed'].tm_year}-{published_month}-{published_day}"
    post['url'] = f"/the-hacks/{episode_file_title}"
    post['podcast_url'] = episode['links'][1]['href'].split('?')[0]
    post['length'] = f"{episode['itunes_duration']}"
    post['image'] = f"{episode['image']['href']}"
    post['tags'] = ['the-hacks']
    post.content = f"\n\n# {episode['title']}\n\n{md(episode['description']).replace('thehacks.libsyn.com/','')}"

    if episode['title'] in the_hacks_config['recommended']:
        post['tags'].append('recommended')

    # Create new Markdown file as content/the-hacks/*.md
    episode_file_name = f"{episode_number_value}-{episode_file_title}.md"
    episode_file_path = Path(the_hacks_path / episode_file_name)
    print(episode_file_path)
    with open(episode_file_path, 'w') as episode_file:
        episode_file.write(frontmatter.dumps(post))
    
    episode_number += 1
