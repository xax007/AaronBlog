import web
import os
import sys
import glob
import traceback
from yaml import load, dump, BaseLoader
import markdown


urls = (
    '/', 'index',
    '/posts/(.+)', 'post',
)
app = web.application(urls, globals()).wsgifunc()

post_dir = '_posts'

def read_post_content(post):
    md = ""
    header_tag = 0
    for line in post:
        if line.strip() == '---':
            header_tag +=1
        elif header_tag == 2:
            md += line
    return md


def get_post_header(post, format):
    post_headers = ""
    try:
        header_tag = 0
        for line in post:
            if line.strip() == '---':
                header_tag += 1
            elif header_tag:
                post_headers += line
            if header_tag == 2:
                break
        if format:
            post_headers = load(post_headers, Loader=BaseLoader)
        return post_headers
    except Exception:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_traceback,
                            limit=1, file=sys.stdout)


class post:
    def GET(self, post):
        
        post_path = os.path.join(os.getcwd(), post_dir)
        post_file = os.path.join(post_path, post + '.md')
        try:
            if os.path.exists(post_file):
                post_content = ""
                with open(post_file, encoding="utf-8") as post:
                    post_content = post.readlines()
                post = read_post_content(post_content)
                post_header = get_post_header(post_content, format=True)
                md = markdown.Markdown(output_format="html5", extensions=['fenced_code','tables'])
                html = md.convert(post)
                render = web.template.render('templates')
                return render.post(html, post_header)
            else:
                return web.notfound()
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback,
                              limit=1, file=sys.stdout)

class index:
    def GET(self):
        posts = []
        try:
            # files = glob.glob(post_dir + "/*.md")
            # files.sort(key=os.path.getctime)
            # files.reverse()
            post_path = os.path.join(os.getcwd(), post_dir)
            files = os.listdir(post_path)
            files.sort(reverse=True)
            
            for post_file in files:
                file_path = os.path.join(post_path, post_file)
                if file_path.endswith('.md'):
                    file_path = file_path
                else:
                    continue
                with open(file_path) as f:
                    post_info = get_post_header(f, format=True)
                    post_info.update({'url': os.path.basename(post_file)[:-3]})
                    posts.append(post_info)
            render = web.template.render('templates')
            return render.index(posts, url=web.ctx.home)
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback,
                              limit=1, file=sys.stdout)
        
        
    

if __name__ == "__main__":
    app.run()
