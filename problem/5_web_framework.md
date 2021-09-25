## 四、Web框架

###  1. 如何理解 Django 被称为 MTV 模式？
* MVC。说是 Model View Controller，
* 而在 Django 中因为 Template 来处理视图展现，所以称为: MTV

接下里会问到的就是分层的概念，有句话叫：“没有什么问题是不能通过增加一层解决的，如果有，那就再加一层。”当然还会有设计模式的一些原则等着你，比如开-闭原则、单一职责原则等。

###  2. 解释下什么是 ORM 以及它的优缺点是什么？

ORM：Object Relational Mapping(对象关系映射)，它做的事就是帮我们封装一下对数据库的操作，避免我们来写不太好维护的 SQL 代码。

优点: 让我们写的代码更容易维护，因为里面不用夹杂着各种 SQL 代码。

缺点: 是失去了 SQL 的灵活，并且越是通用的 ORM 框架，性能损耗会越大。

###  3. Django 中的 Model.objects.raw 这个方法的使用，它的作用、原理、性能提升

 ：N+1 的问题。


###  4. Django 系统中如何配置数据库的长连接？

这涉及到 Django 如何处理数据库连接细节的问题。默认情况下对于每一个请求 Django 都会建立一个新的数据库连接。这意味着当请求量过大时就会出现数据库(MySQL)的 Too many connection 的问题，对于这个问题，在其他的语言框架中有连接池这样的东西来减少数据库的连接数，来提升连接的使用效率。而在 Django中，为了处理这一问题，增加了一个配置:
CONN_MAX_AGE，在 settings 的 DATABASES 配置中。配置了该选项后，Django 会跟数据库保持链接（时长取决于 CONN_MAX_AGE 设定的值 ），不再会针对每个请求都创建新的连接了。
但是需要注意的是，这跟数据库连接池的概念还不太一样。

 
### HTTPS和HTTP的区别：
 
 https协议要申请证书到ca，需要一定经济成本
 http是明文传输，https是加密的安全传输
 连接的端口不一样，http是80，https是443
 http连接很简单，没有状态；https是ssl加密的传输，身份认证的网络协议，相对http传输比较安全。
 
 还有很多，自己去整理一下吧
 第5题：简述Django的orm
 ORM，全拼Object-Relation Mapping，意为对象-关系映射
 实现了数据模型与数据库的解耦，通过简单的配置就可以轻松更换数据库，而不需要修改代码只需要面向对象编程
 ORM操作本质上会根据对接的数据库引擎，翻译成对应的sql语句,
 所有使用Django开发的项目无需关心程序底层使用的是MySql、Oracle、SQLite....，如果数据库迁移，只需要更换Django的数据库引擎即可。
 
 
### 如何解决验证码的问题，用什么模块，听过哪些人工打码平台？

* PIL、pytesser、tesseract模块
* 平台的话有： 云打码 挣码
 斐斐打码
 若快打码
 超级鹰

###  ip 被封了怎么解决，自己做过 ip 池么？

关于 ip 可以通过 ip 代理池来解决问题 ip 代理池相关的可以在 github 上搜索 ip proxy 自己选一个

去说 github.com/awolfly9/IP… 提供大体思路：

获取器 通过 requests 的爬虫爬取免费的 IP 代理网址获取 IP。

过滤器通过获取器获取的代理请求网页数据有数据返回的保存进 Redis。

定时检测器定时拿出一部分 Proxy 重新的用过滤器进行检测剔除不能用的代理。

利用 Flask web 服务器提供 API 方便提取 IP

###  是否了解网络的同步和异步？

* 同步：提交请求->等待服务器处理->处理完毕返回，这个期间客户端浏览器不能干任何事

* 异步: 请求通过事件触发->服务器处理（这是浏览器仍然可以作其他事情）->处理完毕
 
###  Python如何爬取 HTTPS 网站？
> 简单类问题

在使用 requests 前加入：requests.packages.urllib3.disable_warnings()。

为 requests 添加 verify=False 参数

导入ssl模块 `  ssl._create_default_https_context = ssl._create_unverified_context`

### 【爬虫】动态加载又对及时性要求很高怎么处理？
1. Selenium + Phantomjs
2. 尽量不使用 sleep 而使用 WebDriverWait

### python 爬虫有哪些常用框架？

1. [Scrapy](https://scrapy.org/)
> Scrapy是一个为了爬取网站数据，提取结构性数据而编写的应用框架。 可以应用在包括数据挖掘，信息处理或存储历史数据等一系列的程序中。用这个框架可以轻松爬下来如亚马逊商品信息之类的数据。

2. [PySpider](https://github.com/binux/pyspider)
> pyspider 是一个用python实现的功能强大的网络爬虫系统，能在浏览器界面上进行脚本的编写，功能的调度和爬取结果的实时查看，后端使用常用的数据库进行爬取结果的存储，还能定时设置任务与任务优先级等。

3. [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
Beautiful Soup 是一个可以从HTML或XML文件中提取数据的Python库.它能够通过你喜欢的转换器实现惯用的文档导航,查找,修改文档的方式.Beautiful Soup会帮你节省数小时甚至数天的工作时间
 
### Scrapy 的优缺点?
**优点：scrapy 是异步的**

采取可读性更强的 xpath 代替正则, 强大的统计和 log 系统，同时在不同的 url 上爬行支持 shell 方式，方便独立调试写 middleware,方便写一些统一的过滤器，通过管道的方式存入数据库。

**缺点：基于 python 的爬虫框架，扩展性比较差**

基于 twisted 框架，运行中的 exception 是不会干掉 reactor，并且异步框架出错后是不会停掉其他任务的，数据出错后难以察觉。

### scrapy 和 request的区别?

scrapy 是封装起来的框架，他包含了下载器，解析器，日志及异常处理，基于多线程， twisted 的方式处理，对于固定单个网站的爬取开发，有优势，但是对于多网站爬取，并发及分布式处理方面，不够灵活，不便调整与括展。

request 是一个 HTTP 库， 只是用来，进行请求，对于 HTTP 请求，他是一个强大的库，下载，解析全部自己处理，灵活性更高，高并发与分布式部署也非常灵活，对于功能可以更好实现。

### 描述下 scrapy 框架运行的机制？

1. 从 start_urls 里获取第一批 url 并发送请求，请求由引擎交给调度器入请求队列，获取完毕后，调度器将请求队列里的请求交给下载器去获取请求对应的响应资源，并将响应交给自己编写的解析方法做提取处理，如果提取出需要的数据，则交给管道文件处理；
2. 如果提取出 url，则继续执行之前的步骤（发送 url 请求，并由引擎将请求交给调度器入队列…)，直到请求队列里没有请求，程序结束。

### 实现模拟登录的方式有哪些？

* 使用一个具有登录状态的 cookie，结合请求报头一起发送，可以直接发送 get 请求，访问登录后才能访问的页面。
* 先发送登录界面的 get 请求，在登录页面 HTML 里获取登录需要的数据（如果需要的话），然后结合账户密码，再发送 post 请求，即可登录成功。然后根据获取的 cookie信息，继续访问之后的页面。

###  遇到过的反爬虫的策略？

* BAN IP
* BAN USERAGENT
* BAN COOKIES
* 验证码验证
* javascript渲染
* ajax异步传输
 

### 常用的反反爬虫的方案？ 
###  你用过多线程和异步吗？除此之外你还用过什么方法来提高爬虫效率？对Python爬虫框架是否有了解？
###  有没有做过增量式抓取？

