import os
from yaml import load, dump, BaseLoader
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


class ParsePostHeaderError(ValueError):
    pass


def read_md(file):
    md = ""
    header_tag = 0
    with open(file) as f:
        for line in f:
            if line.strip() == '---':
                header_tag +=1
            elif header_tag == 2:
                md += line
    print(md)

def parse_post_file(file):
    post_headers = ""
    headers = []
    try:
        with open(file) as post:
            header_tag = 0
            header = {}
            for line in post:
                if line.strip() == '---':
                    header_tag += 1
                elif header_tag:
                    post_headers += line
                if header_tag == 2:
                    break
        yaml_header = load(post_headers, Loader=BaseLoader)
    except Exception as e:
        print(e)

    return yaml_header


def test_post():
    posts_dir = os.path.join(os.getcwd(), '_posts')
    posts = []
    for file in os.listdir(posts_dir):
        file_path = os.path.join(posts_dir, file)
        header = parse_post_file(file_path)
        posts.append(header['title'])

read_md('_posts/hello.md')