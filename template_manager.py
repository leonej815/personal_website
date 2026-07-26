import re
import os


def get_nav_contents(html_file_path, title=None):
    print(f"DEBUG: Received path -> {html_file_path}")
    base_name = re.match(r"/(.*)\.html", html_file_path).group(1)
    if title == None:
        title = base_name.replace("_", " ").title() + " Joseph Leone"
    css_file_path = f"css/{base_name}.css"
    js_file_path = f"javascript/{base_name}.js"
    css_html = ""
    js_html = ""
    if os.path.exists(css_file_path):
        css_html = f"<link rel='stylesheet' type='text/css' href='{css_file_path}'>"
    if os.path.exists(js_file_path):
        js_html = f"<script src='{js_file_path}'></script>"
    nav_contents = get_text_content("nav.html")
    nav_contents = nav_contents.replace("{{ title }}", title)
    nav_contents = nav_contents.replace("{{ css }}", css_html)
    nav_contents = nav_contents.replace("{{ js }}", js_html)
    print(f"{{{{ active:{base_name} }}}}")
    print(f"{{{{ active:{base_name} }}}}")
    print(f"{{{{ active:{base_name} }}}}")
    nav_contents = nav_contents.replace(f"{{{{ active:{base_name} }}}}", "class=active")    
    nav_contents = re.sub(r"\{\{ active:.* \}\}", "class=inactive", nav_contents)
    return nav_contents


def get_index_contents(nav):
    index_contents = get_text_content("index.html")
    index_contents = index_contents.replace("{{ nav }}", nav)
    return index_contents


def get_page_contents(file_path, nav):
    file_name = file_path.lstrip("/")
    page_contents = get_text_content(file_name)
    page_contents = page_contents.replace("{{ nav }}", nav)
    return page_contents


def text_404(file_path):
    file_path = file_path.lstrip("/")
    message = f"<h1>404: " + file_path + " not found</h1>"
    response_body = message.encode("utf-8")
    response = {
        "status": "404 NOT FOUND",
        "response_body": response_body,
        "headers": [("Content-type", "text/html")]
    }
    return response


def text_200(response_body):
    response = {
        "status": "200 OK",
        "response_body": response_body,
        "headers": [("Content-type", "text/html; charset=utf-8")]
    }
    return response


def image_404():
    response = {
        "status": "404 NOT FOUND",
        "response_body": b"Image not found",
        "headers": [("Content-type", "text/plain")]
    }
    return response


def image_200(file_path, response_body):
    if file_path.endswith(".png"):
        content_type = "image/png"
    else:
        content_type = "image/jpeg"
    response = {
        "status": "200 OK",
        "response_body": response_body,
        "headers": [("Content-type", content_type)]
    }
    return response


def pdf_200(response_body):
    response = {
        "status": "200 OK",
        "response_body": response_body,
        "headers": [("Content-type", "application/pdf")]
    }
    return response


def pdf_404():
    response = {
        "status": "404 NOT FOUND",
        "response_body": b"PDF not found",
        "headers": [("Content-type", "text/plain")]
    }
    return response


def get_image_content(file_path):
    with open(file_path, "rb") as file:
        image_content = file.read()
    return image_content


def get_text_content(file_name):
    with open(file_name, "r", encoding="utf-8") as file:
        text_content = file.read()
    return text_content

