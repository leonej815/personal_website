from wsgiref.simple_server import WSGIServer, make_server
from socketserver import ThreadingMixIn
from template_manager import (
    get_image_content, get_nav_contents, get_index_contents, get_page_contents,
    get_text_content, text_200, text_404, image_200, image_404, pdf_200, pdf_404
)


def web_app(environment, start_response):  
    path = environment.get("PATH_INFO")

    # handle index.html
    if path == "/" or path == "/index.html":
        try:
            nav_content = get_nav_contents("/index.html", "Joseph Leone")
            index_content = get_index_contents(nav_content)
            
            response_body = index_content.encode("utf-8")
            response = text_200(response_body)
        except FileNotFoundError:
            response = text_404(path)

    elif path in ("/education.html", "/projects.html", "/work_history.html", "/coursework.html"):
        try:
            nav_content = get_nav_contents(path)
            page_content = get_page_contents(path, nav_content)
            
            response_body = page_content.encode("utf-8")
            response = text_200(response_body)
        except FileNotFoundError:
            response = text_404(path)

    # handle images
    elif path.startswith("/images/"):
        try:
            file_path = path.lstrip("/")
            response_body = get_image_content(file_path)
            response = image_200(file_path, response_body)
        except FileNotFoundError:
            response = image_404()

    # handle css and js
    elif path.startswith("/css/") or path.startswith("/javascript/"):
        try:
            file_path = path.lstrip("/")
            response_body = get_text_content(file_path).encode("utf-8")
            
            if path.endswith(".css"):
                content_type = "text/css"
            else:
                content_type = "application/javascript"
            
            response = {
                "status": "200 OK",
                "response_body": response_body,
                "headers": [("Content-type", content_type)]
            }
        except FileNotFoundError:
            response = text_404(path)

    # handle pdfs
    elif path.startswith("/pdfs/"):
        try:
            file_path = path.lstrip("/")
            response_body = get_image_content(file_path)
            response = pdf_200(response_body)
        except FileNotFoundError:
            response = pdf_404()

    # catch all 404
    else:
        response = text_404(path)

    start_response(response["status"], response["headers"])
    return [response["response_body"]]


class ThreadingWSGIServer(ThreadingMixIn, WSGIServer):
    daemon_threads = True


# start server locally
if __name__ == "__main__":
    port = 8000  
    with make_server("0.0.0.0", port, web_app, server_class=ThreadingWSGIServer) as httpd:
        httpd.timeout = 0.5
        print(f"Serving on http://localhost:{port}")
        print("Press Ctrl+c to stop.")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nStopping server...")
            httpd.server_close()
            print("Server stopped. Port 8000 is now free.")

