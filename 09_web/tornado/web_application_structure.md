## Structure of a Tornado web application
> A Tornado web application generally consists of one or more RequestHandler subclasses, an Application object which routes incoming requests to handlers, and a main() function to start the server.
> 通过Applcation对象路由到多个RequestHandler对象，使用main函数启动一个服务
> 
```python
## A minimal “hello world” example 
import tornado.ioloop
from tornado.web import RequestHandler, Application

class MainHandler(RequestHandler):
    def get(self):
        self.write("Hello, world")

def make_app():
    return Application([
        (r"/", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
```

### The Application object

The Application object is responsible for global configuration, including the routing table that maps requests to handlers.

The routing table is a list of URLSpec objects (or tuples), each of which contains (at least) a regular expression and a handler class. 
Order matters; the first matching rule is used. 

  * url正则传值 If the regular expression contains capturing groups, these groups are the path arguments and will be passed to the handler’s HTTP method. 

  * 请求处理器传参 If a dictionary is passed as the third element of the `URLSpec`, it supplies the initialization arguments which will be passed to RequestHandler.initialize. 

  * 反向URL: Finally, the URLSpec may have a name, which will allow it to be used with RequestHandler.reverse_url.
 
```python
from tornado.web import RequestHandler, Application, url
class StoryHandler(RequestHandler):
    def initialize(self, db):
        self.db = db 
    def get(self, story_id):
        self.write("this is story %s" % story_id)

app = Application([  url(r"/story/([0-9]+)", StoryHandler, dict(db=db), name="story")])
```
[Application 更多参数](https://www.tornadoweb.org/en/stable/web.html#tornado.web.Application.settings)

```python
settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "cookie_secret": "__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
    "login_url": "/login",
    "xsrf_cookies": True,
}
application = Application([ ], **settings)

```

### Subclassing RequestHandler
Most of the work of a Tornado web application is done in subclasses of RequestHandler. The main entry point for a handler subclass is a method named after the HTTP method being handled: get(), post(), etc. Each handler may define one or more of these methods to handle different HTTP actions. As described above, these methods will be called with arguments corresponding to the capturing groups of the routing rule that matched.

RequestHandler produce a response 返回结果的方法

* 渲染 render() loads a Template by name and renders it with the given arguments. 
* 写入 write() is used for non-template-based output; it accepts strings, bytes, and dictionaries (dicts will be encoded as JSON).

Many methods in RequestHandler are designed to be overridden in subclasses and be used throughout the application. 

It is common to define a BaseHandler class that overrides methods such as write_error and get_current_user and then subclass your own BaseHandler instead of RequestHandler for all your specific handlers.

### Handling request input 处理输入

The request handler can access the object representing the current request with self.request. 
See the class definition for [HTTPServerRequest](https://www.tornadoweb.org/en/stable/httputil.html#tornado.httputil.HTTPServerRequest) for a complete list of attributes.

Request data in the formats available:

* get_query_argument

* get_body_argument

* self.request.files  
  > only present if the files were uploaded with a form wrapper (i.e. a multipart/form-data Content-Type);

* self.request.body 
 

Due to the quirks of the HTML form encoding (e.g. the ambiguity around singular versus plural arguments), Tornado does not attempt to unify form arguments with other types of input. In particular, we do not parse JSON request bodies. Applications that wish to use JSON instead of form-encoding may override prepare to parse their requests:

```python 
def prepare(self):
if self.request.headers.get("Content-Type", "").startswith("application/json"):
self.json_args = json.loads(self.request.body)
else:
self.json_args = None
```

### Overriding RequestHandler methods

In addition to get()/post()/etc, certain other methods in RequestHandler are designed to be overridden by subclasses when necessary. On every request, the following sequence of calls takes place:

1. A new RequestHandler object is created on each request.
2. initialize() is called with the initialization arguments from the Application configuration. initialize should typically just save the arguments passed into member variables; it may not produce any output or call methods like send_error.
3. prepare() is called. This is most useful in a base class shared by all of your handler subclasses, as prepare is called no matter which HTTP method is used. prepare may produce output; if it calls finish (or redirect, etc), processing stops here.
4. One of the HTTP methods is called: get(), post(), put(), etc.  If the URL regular expression contains capturing groups, they are passed as arguments to this method.
5. When the request is finished, on_finish() is called. 

[RequestHandler documentation](https://www.tornadoweb.org/en/stable/web.html#tornado.web.RequestHandler)

most commonly overridden methods:

* write_error - outputs HTML for use on error pages.
* on_connection_close - called when the client disconnects; applications may choose to detect this case and halt further processing. Note that there is no guarantee that a closed connection can be detected promptly.
* get_current_user - see User authentication.
* get_user_locale - returns Locale object to use for the current user.
* set_default_headers - may be used to set additional headers on the response (such as a custom Server header).

### Error Handling

If a handler raises an exception, Tornado will call RequestHandler.write_error to generate an error page. 
tornado.web.HTTPError can be used to generate a specified status code; all other exceptions return a 500 status.

The default error page includes a stack trace in debug mode and a one-line description of the error (e.g. “500: Internal Server Error”) otherwise. To produce a custom error page, override RequestHandler.write_error (probably in a base class shared by all your handlers). This method may produce output normally via methods such as write and render. If the error was caused by an exception, an exc_info triple will be passed as a keyword argument (note that this exception is not guaranteed to be the current exception in sys.exc_info, so write_error must use e.g. traceback.format_exception instead of traceback.format_exc).

It is also possible to generate an error page from regular handler methods instead of write_error by calling set_status, writing a response, and returning. 

The special exception tornado.web.Finish may be raised to terminate the handler without calling write_error in situations where simply returning is not convenient.

For 404 errors, use the default_handler_class Application setting. 

This handler should override prepare instead of a more specific method like get() so it works with any HTTP method.
It should produce its error page as described above: either by raising a HTTPError(404) and overriding write_error, or calling self.set_status(404) and producing the response directly in prepare().

### Redirection

* RequestHandler.redirect

There is also an optional parameter permanent which you can use to indicate that the redirection is considered permanent. The default value of permanent is False, which generates a 302 Found HTTP response code and is appropriate for things like redirecting users after successful POST requests. If permanent is True, the 301 Moved Permanently HTTP response code is used, which is useful for e.g. redirecting to a canonical URL for a page in an SEO-friendly manner.

* RedirectHandler 
  > lets you configure redirects directly in your Application routing table 
```python
app = tornado.web.Application([
url(r"/app", tornado.web.RedirectHandler,
dict(url="http://itunes.apple.com/my-app-id")),
])
```

 > also supports regular expression substitutions. The following rule redirects all requests beginning with /pictures/ to the prefix /photos/ instead:

```python
app = tornado.web.Application([
url(r"/photos/(.*)", MyPhotoHandler),
url(r"/pictures/(.*)", tornado.web.RedirectHandler,
dict(url=r"/photos/{0}")),
])
```

Unlike RequestHandler.redirect, RedirectHandler uses permanent redirects by default. This is because the routing table does not change at runtime and is presumed to be permanent, while redirects found in handlers are likely to be the result of other logic that may change. To send a temporary redirect with a RedirectHandler, add permanent=False to the RedirectHandler initialization arguments.

### Asynchronous handlers

Certain handler methods (including prepare() and the HTTP verb methods get()/post()/etc) may be overridden as coroutines to make the handler asynchronous.

```python
class MainHandler(tornado.web.RequestHandler):
    async def get(self):
        http = tornado.httpclient.AsyncHTTPClient()
        response = await http.fetch("http://friendfeed-api.com/v2/feed/bret")
        json = tornado.escape.json_decode(response.body)
        self.write("Fetched " + str(len(json["entries"])) +  "from the FriendFeed API")

```

[the chat example](https://github.com/tornadoweb/tornado/tree/stable/demos/chat) application, which implements an AJAX chat room using long polling. 


