## Templates and UI

> Tornado includes a simple, fast, and flexible templating language

### Configuring templates

To put your template files in a different directory, use the template_path Application setting
(or override RequestHandler.get_template_path if you have different template paths for different handlers).

To load templates from a non-filesystem location, subclass tornado.template.BaseLoader and pass an instance as the
template_loader application setting.

Compiled templates are cached by default; `settings compiled_template_cache=False` or `debug=True` to turn off.

### Template Syntax

```html

<html>
<head>
    <title>{{ title }}</title>
</head>
<body>
<ul>
    {% for item in items %}
    <li>{{ escape(item) }}</li>
    {% end %}
</ul>
</body>
</html>
```

render this template with:

```python
class MainHandler(RequestHandler):
    def get(self):
        items = ["Item 1", "Item 2", "Item 3"]
        self.render("template.html", title="My title", items=items)
```

* `{% * %}` for Control statements
* escape: alias for tornado.escape.xhtml_escape
* xhtml_escape: alias for tornado.escape.xhtml_escape
* url_escape: alias for tornado.escape.url_escape
* json_encode: alias for tornado.escape.json_encode
* squeeze: alias for tornado.escape.squeeze
* linkify: alias for tornado.escape.linkify
* datetime: the Python datetime module
* handler: the current RequestHandler object
* request: alias for handler.request
* current_user: alias for handler.current_user
* locale: alias for handler.locale
* _: alias for handler.locale.translate
* static_url: alias for handler.static_url
* xsrf_form_html: alias for handler.xsrf_form_html
* reverse_url: alias for Application.reverse_url
* All entries from the ui_methods and ui_modules Application settings
* Any keyword arguments passed to render or render_string

Here is a properly internationalized template:

```html

<html>
<head>
    <title>FriendFeed - {{ _("Sign in") }}</title>
</head>
<body>
<form action="{{ request.path }}" method="post">
    <div>{{ _("Username") }} <input type="text" name="username"/></div>
    <div>{{ _("Password") }} <input type="password" name="password"/></div>
    <div><input type="submit" value="{{ _(" Sign in") }}"/></div>
    {% module xsrf_form_html() %}
</form>
</body>
</html>
```

set their locale as a preference, you can override this default locale selection by overriding
RequestHandler.get_user_locale:

```python
class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        user_id = self.get_secure_cookie("user")
        if not user_id: return None
        return self.backend.get_user_by_id(user_id)

    def get_user_locale(self):
        if "locale" not in self.current_user.prefs:
            # Use the Accept-Language header
            return None
        return self.current_user.prefs["locale"]
```

The tornado.locale module supports loading translations in two formats: the .mo format used by gettext and related
tools, and a simple .csv format.

format. An application will generally call either tornado.locale.load_translations or
tornado.locale.load_gettext_translations once at startup;

### UI modules

make an Entry module to render them on both pages.

First, create a Python module for your UI modules, e.g. uimodules.py:

```python
from tornado.web import UIModule


class Entry(UIModule):
    def render(self, entry, show_comments=False):
        return self.render_string("module-entry.html", entry=entry, show_comments=show_comments)

```

using the ui_modules setting in your application:

```python
from . import uimodules
from tornado.web import RequestHandler, Application, HTTPError


class HomeHandler(RequestHandler):
    def get(self):
        entries = self.db.query("SELECT * FROM entries ORDER BY date DESC")
        self.render("home.html", entries=entries)


class EntryHandler(RequestHandler):
    def get(self, entry_id):
        entry = self.db.get("SELECT * FROM entries WHERE id = %s", entry_id)
        if not entry: raise HTTPError(404)
        self.render("entry.html", entry=entry)


settings = {
    "ui_modules": uimodules,
}
application = Application([
    (r"/", HomeHandler),
    (r"/entry/([0-9]+)", EntryHandler),
], **settings)
```

Within a template, you can call a module with the {% module %} statement.

```html
{% for entry in entries %}
{% module Entry(entry) %}
{% end %}
```

Modules can include custom CSS and JavaScript functions by overriding the embedded_css, embedded_javascript,
javascript_files, or css_files methods:

When additional Python code is not required, a template file itself may be used as a module. For example, the preceding
example could be rewritten to put the following in module-entry.html:

```html
{{ set_resources(embedded_css=".entry { margin-bottom: 1em; }") }}
<!-- more template html... -->
```

This revised template module would be invoked with:

```html
{% module Template("module-entry.html", show_comments=True) %}
```

The set_resources function is only available in templates invoked via {% module Template(...) %}. Unlike the {% include
... %} directive, template modules have a distinct namespace from their containing template - they can only see the
global template namespace and their own keyword arguments.
