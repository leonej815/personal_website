import re
import os


def get_nav_contents(html_file_path, title=None):
    """Takes the file path of the html file that the nav file is going to be loaded with and formats the nav file text by replacing double bracket tags.
    Inputs:
        html_file_path (str): file path of associated main file
        title (str): title for the webpage
    Outputs:
        nav_contents (str): updated nav file contents with tags replaced
    """

    # get the name of the file without the file extension
    base_name = re.match(r"/(.*)\.html", html_file_path).group(1)

    # format the title
    if title == None:
        title = base_name.replace("_", " ").title() + " Joseph Leone"

    # use the file name without extension to get the associated file paths for css/js
    css_file_path = f"css/{base_name}.css"
    js_file_path = f"javascript/{base_name}.js"

    # create html elements for css and javascript file inclusion
    css_html = ""
    js_html = ""
    if os.path.exists(css_file_path):
        css_html = f"<link rel='stylesheet' type='text/css' href='{css_file_path}'>"
    if os.path.exists(js_file_path):
        js_html = f"<script src='{js_file_path}'></script>"

    # load text from nav html file and replace bracket tags with new html
    nav_contents = get_text_content("nav.html")
    nav_contents = nav_contents.replace("{{ title }}", title)
    nav_contents = nav_contents.replace("{{ css }}", css_html)
    nav_contents = nav_contents.replace("{{ js }}", js_html)

    # this highlights the nav button for the current page that is being displayed
    nav_contents = nav_contents.replace(f"{{{{ active:{base_name} }}}}", "class=active")    
    nav_contents = re.sub(r"\{\{ active:.* \}\}", "class=inactive", nav_contents)

    return nav_contents


def get_index_contents(nav):
    """Get the contents of the home page.
    Inputs:
        nav (str): nav content for the home page
    Outputs:
        index_contents (str): all content needed for home page
    """

    # get the content of index.html and insert the nav html
    index_contents = get_text_content("index.html")
    index_contents = index_contents.replace("{{ nav }}", nav)

    return index_contents


def get_page_contents(file_path, nav):
    """Function to prepare contents for pages that aren't the home page
    Inputs:
        file_path (str): file_path to main html file for the page
        nav (str): associated nav content for given file_path
    Outputs:
        page_contents (str): fully prepared content for the page
    """

    file_name = file_path.lstrip("/")

    # get page contents and insert nav contents
    page_contents = get_text_content(file_name)
    page_contents = page_contents.replace("{{ nav }}", nav)

    return page_contents


def text_404(file_path):
    """Returns 404 response when text file isn't found"""

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
    """Returns 200 response with text data when text file found"""

    response = {
        "status": "200 OK",
        "response_body": response_body,
        "headers": [("Content-type", "text/html; charset=utf-8")]
    }
    return response


def image_404():
    """Returns 404 response when image file isn't found"""

    response = {
        "status": "404 NOT FOUND",
        "response_body": b"Image not found",
        "headers": [("Content-type", "text/plain")]
    }
    return response


def image_200(file_path, response_body):
    """Returns 200 response with image file data when image file found"""

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
    """Returns 200 response with pdf file data when pdf file found"""
    response = {
        "status": "200 OK",
        "response_body": response_body,
        "headers": [("Content-type", "application/pdf")]
    }
    return response


def pdf_404():
    """Returns 404 response when pdf file isn't found"""
    response = {
        "status": "404 NOT FOUND",
        "response_body": b"PDF not found",
        "headers": [("Content-type", "text/plain")]
    }
    return response


def get_image_content(file_path):
    """Open image file at file_path and return image content as bytes"""

    with open(file_path, "rb") as file:
        image_content = file.read()
    return image_content


def get_text_content(file_name):
    """Open text file at file_name and return text content as a string"""

    with open(file_name, "r", encoding="utf-8") as file:
        text_content = file.read()
    return text_content

