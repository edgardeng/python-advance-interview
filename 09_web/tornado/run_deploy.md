## Running and deploying

Instead of configuring a WSGI container to find your application, you write a main() function that starts the server:

Configure your operating system or process manager to run this program to start the server. 

###  Processes and ports

Due to the Python GIL (Global Interpreter Lock), it is necessary to run multiple Python processes to take full advantage of multi-CPU machines. 

Tornado includes a built-in multi-process mode to start several processes at once 
> (note that multi-process mode does not work on Windows). 

```python
def main():
    app = make_app()
    server = tornado.httpserver.HTTPServer(app)
    server.bind(8888)
    server.start(0)  # forks one process per cpu
    IOLoop.current().start()
```

### Running behind a load balancer

When running behind a load balancer like nginx, it is recommended to pass xheaders=True to the HTTPServer constructor. 

tell Tornado to use headers like X-Real-IP to get the user’s IP address instead of attributing all traffic to the balancer’s IP address.


### Static files and aggressive file caching

serve static files from Tornado by specifying the static_path setting in your application:

We also automatically serve /robots.txt and /favicon.ico from the static directory (even though they don’t start with the /static/ prefix).

### Debug mode and automatic reloading
If you pass debug=True to the Application constructor, the app will be run in debug/development mode. In this mode, several features intended for convenience while developing will be enabled (each of which is also available as an individual flag; if both are specified the individual flag takes precedence):

* autoreload=True: The app will watch for changes to its source files and reload itself when anything changes. This reduces the need to manually restart the server during development. However, certain failures (such as syntax errors at import time) can still take the server down in a way that debug mode cannot currently recover from.
* compiled_template_cache=False: Templates will not be cached.
* static_hash_cache=False: Static file hashes (used by the static_url function) will not be cached.
* serve_traceback=True: When an exception in a RequestHandler is not caught, an error page including a stack trace will be generated.