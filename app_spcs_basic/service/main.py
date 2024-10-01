from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import json
import traceback
import sys

PORT = int(os.environ.get("PORT", 8080))
GET_PATHS = ('/', '/index.html', '/healthcheck')
POST_PATHS = ('/echo')

class handler(BaseHTTPRequestHandler):
    """
        Simple Python HTTP server that acts as both an ingress (GET)
        and as a service function endpoint (POST)
    """

    def do_GET(self):
        """
        Returns an HTML page bundled with the server
        """
        if self.path not in GET_PATHS:
            self.send_error(404)
            return

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        with open('index.html', 'rb') as f:
            self.wfile.write(f.read())

    def do_POST(self):
        """
        POSTing to /echo in the external function format will echo the payload back to Snowflake.
        See https://docs.snowflake.com/en/sql-reference/external-functions-data-format
        """
        if self.path not in POST_PATHS:
            self.send_error(404)
            return

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        try:
            # post body looks something like...
            # {
            #   "data": [
            #     [0, 10, "Alex", "2014-01-01 16:00:00"],
            #     [1, 20, "Steve", "2015-01-01 16:00:00"],
            #     [2, 30, "Alice", "2016-01-01 16:00:00"],
            #     [3, 40, "Adrian", "2017-01-01 16:00:00"]
            #   ]
            # }
            content_len = int(self.headers.get('Content-Length'))
            post_body = self.rfile.read(content_len)
            parsed = json.loads(post_body)

            # in our case, we only have the one column, so we'll just have [rowid, message]
            # and in fact, we're just echoing, so all we have to do is just return the same payload
            # so you can see what's happening in logs, we'll echo all the rows we found
            for [rowid, message] in parsed["data"]:
                print(f"{rowid}: {message}")

            # echo back the exact same data, making sure it's JSON
            self.wfile.write(json.dumps(parsed).encode('utf-8'))
        except:
            tb = traceback.format_exc()
            print(tb, file=sys.stderr)
            self.send_error(500, "Exception occurred", tb)

with HTTPServer(('', PORT), handler) as server:
    server.serve_forever()
