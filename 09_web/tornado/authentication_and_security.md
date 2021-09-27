## Authentication and security

### Cookies and secure cookies

```python
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        # if not self.get_secure_cookie("mycookie"):
        #     self.set_secure_cookie("mycookie", "myvalue")
        if not self.get_cookie("mycookie"):
            self.set_cookie("mycookie", "myvalue")
            self.write("Your cookie was not set yet!")
        else:
            self.write("Your cookie was set!")
```


If you need to set cookies to, e.g., identify the currently logged in user, you need to sign your cookies to prevent forgery. Tornado supports signed cookies with the set_secure_cookie and get_secure_cookie methods. 

To use these methods, you need to specify a secret key named cookie_secret when you create your application.

Signed cookies contain the encoded value of the cookie in addition to a timestamp and an HMAC signature.
. If the cookie is old or if the signature doesn’t match, get_secure_cookie will return None

By default, Tornado’s secure cookies expire after 30 days
use the `expires_days` keyword argument to `set_secure_cookie` and the `max_age_days` argument to `get_secure_cookie`.

Tornado also supports multiple signing keys to enable signing key rotation.
cookie_secret then must be a dict with integer key versions as keys and the corresponding secrets as values. 

### User authentication

The currently authenticated user is available in every request handler as self.current_user

To implement user authentication in your application, you need to override the get_current_user() method in your request handlers to determine the current user based on, e.g.

```python
from tornado.web import RequestHandler
class BaseHandler(RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")

class MainHandler(BaseHandler):
    def get(self):
        if not self.current_user:
            self.redirect("/login")
            return
        name = tornado.escape.xhtml_escape(self.current_user)
        self.write("Hello, " + name)

class LoginHandler(BaseHandler):
    def get(self):
        self.write('<html><body><form action="/login" method="post">'
                   'Name: <input type="text" name="name">'
                   '<input type="submit" value="Sign in">'
                   '</form></body></html>')

    def post(self):
        self.set_secure_cookie("user", self.get_argument("name"))
        self.redirect("/")
```
 
If a request goes to a method with this decorator `tornado.web.authenticated`, and the user is not logged in, they will be redirected to login_url (another application setting). 

### Third party authentication

The [tornado.auth](https://www.tornadoweb.org/en/stable/auth.html#module-tornado.auth) module implements the authentication and authorization protocols for a number of the most popular sites on the web, including Google/Gmail, Facebook, Twitter, and FriendFeed.


```python
class GoogleOAuth2LoginHandler(tornado.web.RequestHandler,
                               tornado.auth.GoogleOAuth2Mixin):
    async def get(self):
        if self.get_argument('code', False):
            user = await self.get_authenticated_user(
                redirect_uri='http://your.site.com/auth/google',
                code=self.get_argument('code'))
            # Save the user with e.g. set_secure_cookie
        else:
            await self.authorize_redirect(
                redirect_uri='http://your.site.com/auth/google',
                client_id=self.settings['google_oauth']['key'],
                scope=['profile', 'email'],
                response_type='code',
                extra_params={'approval_prompt': 'auto'})
```

### Cross-site request forgery protection

Tornado comes with built-in XSRF protection.
 

If `xsrf_cookies` is set, the Tornado web application will set the _xsrf cookie for all users and reject all POST, PUT, and DELETE requests that do not contain a correct _xsrf value.

You can do this with the special UIModule xsrf_form_html(), available in all templates:

```html
<form action="/new_message" method="post">
  {% module xsrf_form_html() %}
  <input type="text" name="message"/>
  <input type="submit" value="Post"/>
</form>

```

If you need to customize XSRF behavior on a per-handler basis, you can override RequestHandler.check_xsrf_cookie(). 

### DNS Rebinding

This attack involves a DNS name (with a short TTL) that alternates between returning an IP address controlled by the attacker and one controlled by the victim (often a guessable private IP address such as 127.0.0.1 or 192.168.1.1).

Applications that cannot use TLS and rely on network-level access controls (for example, assuming that a server on 127.0.0.1 can only be accessed by the local machine) should guard against DNS rebinding by validating the Host HTTP header.

This means passing a restrictive hostname pattern to either a HostMatches router or the first argument of Application.add_handlers:

```python
# BAD: uses a default host pattern of r'.*'
app = Application([('/foo', FooHandler)])

# GOOD: only matches localhost or its ip address.
app = Application()
app.add_handlers(r'(localhost|127\.0\.0\.1)',
[('/foo', FooHandler)])

# GOOD: same as previous example using tornado.routing.
app = Application([
(HostMatches(r'(localhost|127\.0\.0\.1)'),
[('/foo', FooHandler)]),
])
```
