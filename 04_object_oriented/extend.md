## 继承
> 定义一个class的时候，可以从某个现有的class继承，新的class称为子类（Subclass），而被继承的class称为基类、父类或超类（Base class、Super class）。

继承最大的好处是子类获得了父类的全部功能

```python
class Animal(object):
    def run(self):
        print('Animal is running...')
class Dog(Animal):
    pass

class Cat(Animal):
    pass

```
继承可以把父类的所有功能都直接拿过来，这样就不必重零做起，子类只需要新增自己特有的方法，也可以把父类不适合的方法覆盖重写。

动态语言的鸭子类型特点决定了继承不像静态语

### 多态

当子类和父类都存在相同的方法时子类的盖了父类的，这就是继承的另一个好处：多态。

```python
class Dog(Animal):
    def run(self):
        print('Dog is running...')

class Cat(Animal):
    def run(self):
        print('Cat is running...')
```

### 鸭子类型 

> 在程序设计中，鸭子类型（英语：Duck typing）是动态类型和某些静态语言的一种对象推断风格。
 
> "鸭子类型"像多态一样工作，但是没有继承。“鸭子类型”的语言是这么推断的：一只鸟走起来像鸭子、游起泳来像鸭子、叫起来也像鸭子，那它就可以被当做鸭子。
>
> 也就是说，它不关注对象的类型，而是关注对象具有的行为(方法)
    
```python
class Dog(object):
    def run(self):
        print('Dog is running...')

class Cat(object):
    def run(self):
        print('Cat is running...')
for animal in [Dog, Cat]:
    animal().run()
```
Dog,Cat中有相同的方法run()，当有一个函数调用Duck类时并调用say()方法，我们传入Cat类和Dog类也行，函数并不会检查对象是不是Duck，而是只要你有这样的方法就能运行。

比如部分魔法函数：
 * 只要实现了类中的__getitem__()，就可以把类当作一个collection，
 * 实现__iter__和__next__就可以当作一个iterator。
 
 python中的鸭子类型允许我们使用任何提供所需方法的对象，而不需要迫使它成为一个子类。


### 抽象基类

* 在某些情况下判断某个对象的类型：

    


### isintance 和 type


### 多继承

#### 类属性和实例属性以及查找顺序
　　1.向上查找，即先查找对象变量（实例属性），后查找类属性：
　　2.多继承采用MRO（【Method Resolution Order】：方法解析顺序）算法：
　　　　Python语言包含了很多优秀的特性，其中多重继承就是其中之一，但是多重继承会引发很多问题，比如二义性，Python中一切皆引用，这使得他不会像C++一样使用虚基类处理基类对象重复的问题，但是如果父类存在同名函数的时候还是会产生二义性，Python中处理这种问题的方法就是MRO

    3.C3算法（参考：https://www.cnblogs.com/LLBFWH/p/10009064.html）：　　
    　　　　求某一类在多继承中的继承顺序:
    　　　　类的mro == [类] + [父类的继承顺序] + [父类2的继承顺序]
    　　　　如果从左到右的第一个类在后面的顺序中出现,那么就提取出来到mro顺序中
    　　　　[ABCD] + [EO] --> A = [BCD] + [EO]
    　　　　如果从左到右的第一个类在后面的顺序中出现,且在后面的顺序中也是第一位,那么就提出来到mro顺序中
    　　　　[ABCD] + [AEO] --> A = [BCD] + [EO]
    　　　　如果从左到右的第一个类在后面的顺序中出现,但不是在第一位,那么应该继续往后找,找到符合规则的项目
    　　　　[ABCD] + [EAO] --> E = [ABCD] + [AO]
    　　　　[ABCD] + [EAO] + [GEO] --> G = [ABCD] + [EAO] + [EO]
    　　　　[ABCD] + [EAO] + [EO] --> GE = [ABCD] + [AO] + [O]
    　　　　关键结论:
    　　　　 　　 这个类没有发生继承,他的顺序永远是[类o]
    　　　　　　  只要是单继承,不是多继承,那么mro顺序就是从子类到父类的顺序
    
    　　4.查找顺序：
    　　　　4.1 菱形继承：（Python2.3以前为经典类，默认不继承object（D），而2.3以后为新式类，默认继承object，即最后查找object类）
           4.2 分别继承：
