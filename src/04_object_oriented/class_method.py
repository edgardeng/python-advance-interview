class Foo:
    def method():
        print('method')

    @staticmethod
    def m_static_method():
        print('m_static_method')

    @classmethod
    def m_cls_method(cls):
        print(cls, 'm_cls_method')

    def self_method(self):
        print(self, 'self_method')


if __name__ == '__main__':
    print(Foo)                      # <class '__main__.Foo'>
    print(Foo())                    # <__main__.Foo object at 0x7faa48f85150>
    print(Foo.method)               # <function Foo.method at 0x7fcaeb0db830>
    print(Foo().method)             # <bound method Foo.method of <__main__.Foo object at 0x7fcaeb085150>>
    Foo.method()                    # method
    # Foo().method()                # TypeError: method() takes 0 positional arguments but 1 was given

    print(Foo.m_static_method)   # <function Foo.m_static_method at 0x7f9c748e0170>
    print(Foo().m_static_method) # <function Foo.m_static_method at 0x7f9c748e0170>
    Foo.m_static_method()        # m_static_method
    Foo().m_static_method()      # m_static_method

    print(Foo.m_cls_method)   # <bound method Foo.m_cls_method of <class '__main__.Foo'>>
    print(Foo().m_cls_method) # <bound method Foo.m_cls_method of <class '__main__.Foo'>>
    Foo.m_cls_method()        # <class '__main__.Foo'> m_cls_method
    Foo().m_cls_method()      # <class '__main__.Foo'> m_cls_method

    print(Foo.self_method)      # <function Foo.self_method at 0x7fa4842c20e0>
    print(Foo().self_method)    # <bound method Foo.self_method of <__main__.Foo object at 0x7fa4842bfb90>>
    # Foo.self_method()         # TypeError: self_method() missing 1 required positional argument: 'self'
    Foo().self_method()         # <__main__.Foo object at 0x7fa4842bfb90> self_method
