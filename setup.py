from http.server import HTTPServer, CGIHTTPRequestHandler,BaseHTTPRequestHandler
class Handler(CGIHTTPRequestHandler,BaseHTTPRequestHandler):
    cgi_directories = ["/"]

httpd = HTTPServer(("", 8000), Handler)
httpd.serve_forever()