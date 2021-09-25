# subprocess模块

> subprocess模块来产生子进程,并连接到子进程的标准输入/输出/错误中去，还可以得到子进程的返回值
> subprocess意在替代其他几个老的模块或者函数，比如：os.system os.spawn* os.popen* popen2.* commands.*


## 一、subprocess.Popen

```python
class subprocess.Popen( args,
    bufsize=0,
    executable=None,
    stdin=None,
    stdout=None,
    stderr=None,
    preexec_fn=None,
    close_fds=False,
    shell=False,
    cwd=None,
    env=None,
    universal_newlines=False,
    startupinfo=None,
    creationflags=0)
```

各参数含义如下：

* args参数。可以是一个字符串，可以是一个包含程序参数的列表。要执行的程序一般就是这个列表的第一项，或者是字符串本身。

```
subprocess.Popen(["cat","test.txt"])
subprocess.Popen("cat test.txt")

```
  这两个之中，后者将不会工作。因为如果是一个字符串的话，必须是程序的路径才可以。(考虑unix的api函数exec，接受的是字符串列表)但是下面的可以工作


`subprocess.Popen("cat test.txt", shell=True)`相当于 `subprocess.Popen(["/bin/sh", "-c", "cat test.txt"])`
在Linux下，当shell=False（默认）时，Popen使用os.execvp()来执行子程序。
args一般要是一个【列表】。如果args是个字符串的话，会被当做是可执行文件的路径，这样就不能传入任何参数了。


shlex.split()可以被用于序列化复杂的命令参数，比如：
```
>>> shlex.split('ls ps top grep pkill')
['ls', 'ps', 'top', 'grep', 'pkill']
>>>import shlex, subprocess
>>>command_line = raw_input()
/bin/cat -input test.txt -output "diege.txt" -cmd "echo '$MONEY'"
>>>args = shlex.split(command_line)
>>> print args
['/bin/cat', '-input', 'test.txt', '-output', 'diege.txt', '-cmd', "echo '$MONEY'"]
>>>p=subprocess.Popen(args)
```

可以看到，空格分隔的选项（如-input）和参数（如test.txt）会被分割为列表里独立的项，但引号里的或者转义过的空格不在此列。这也有点像大多数shell的行为。

在linux下，当shell=True时，如果arg是个字符串，就使用shell来解释执行这个字符串。如果args是个列表，则第一项被视为命令，其余的都视为是给shell本身的参数。也就是说，等效于：

`subprocess.Popen(['/bin/sh', '-c', args[0], args[1], ...])`

在Windows下，下面的却又是可以工作的

`subprocess.Popen(["notepad.exe", "test.txt"])` 和 `subprocess.Popen("notepad.exe test.txt")`
这是由于windows下的api函数CreateProcess接受的是一个字符串。即使是列表形式的参数，也需要先合并成字符串再传递给api函数

`subprocess.Popen("notepad.exe test.txt" shell=True)` 等同于 `subprocess.Popen("cmd.exe /C "+"notepad.exe test.txt" shell=True）`

 * bufsize参数: 和内建函数open()一样：0表示不缓冲，1表示行缓冲，其他正数表示近似的缓冲区字节数，负数表示使用系统默认值。默认是0。

 * executable参数: 指定要执行的程序。它很少会被用到：一般程序可以由args 参数指定。如果shell=True ，executable 可以用于指定用哪个shell来执行（比如bash、csh、zsh等）。*nix下，默认是 /bin/sh ，windows下，就是环境变量 COMSPEC 的值。windows下，只有当你要执行的命令确实是shell内建命令（比如dir ，copy 等）时，你才需要指定shell=True ，而当你要执行一个基于命令行的批处理脚本的时候，不需要指定此项。

 * stdin stdout和stderr： 分别表示子程序的标准输入、标准输出和标准错误。可选的值有PIPE或者一个有效的文件描述符（其实是个正整数）或者一个文件对象，还有None。如果是PIPE，则表示需要创建一个新的管道，如果是None，不会做任何重定向工作，子进程的文件描述符会继承父进程的。另外，stderr的值还可以是STDOUT，表示子进程的标准错误也输出到标准输出。

 * preexec_fn参数： 一个可调用的对象（比如函数），就会在子进程被执行前被调用。（仅限*nix）

 * close_fds参数： True时，*nix下会在开子进程前把除了0、1、2以外的文件描述符都先关闭。在 Windows下也不会继承其他文件描述符。

 * shell参数： 如果把shell设置成True，指定的命令会在shell里解释执行。

 * cwd参数： 如果cwd不是None，则会把cwd做为子程序的当前目录。注意，并不会把该目录做为可执行文件的搜索目录，所以不要把程序文件所在目录设置为cwd 。

 * env参数： 如果env不是None，则子程序的环境变量由env的值来设置，而不是默认那样继承父进程的环境变量。注意，即使你只在env里定义了某一个环境变量的值，也会阻止子程序得到其他的父进程的环境变量（也就是说，如果env里只有1项，那么子进程的环境变量就只有1个了）。例如：

 
```
subprocess.Popen('env', env={'test':'123', 'testtext':'zzz'}) 
test=123
<subprocess.Popen object at 0x2870ad2c>
testtext=zzz
```
 * universal_newlines参数: 为True，则子进程的stdout和stderr被视为文本对象，并且不管是*nix的行结束符（'/n'），还是老mac格式的行结束符（'/r' ），还是windows 格式的行结束符（'/r/n' ）都将被视为 '/n' 。

 * startupinfo和creationflags参数： 如果指定了startupinfo和creationflags，将会被传递给后面的CreateProcess()函数，用于指定子程序的各种其他属性，比如主窗口样式或者是子进程的优先级等。（仅限Windows）

## 二、subprocess.PIPE


 * subprocess.PIPE 一个可以被用于Popen的stdin 、stdout 和stderr 3个参数的特输值，表示需要创建一个新的管道。
 * subprocess.STDOUT  一个可以被用于Popen的stderr参数的输出值，表示子程序的标准错误汇合到标准输出。

实例：
``` 
p=subprocess.Popen("df -h",shell=True,stdout=subprocess.PIPE)
out=p.stdout.readlines()
out
[b'Filesystem  Size Used Avail Capacity Mounted on\n', b'/dev/ad0s1a 713M 313M 343M 48% /\n', b'devfs   1.0K 1.0K  0B 100% /dev\n', b'/dev/ad0s1e 514M 2.1M 471M  0% /tmp\n', b'/dev/ad0s1f 4.3G 2.5G 1.4G 64% /usr\n', b'/dev/ad0s1d 2.0G 121M 1.7G  6% /var\n'
>>> for line in out:
...  print line.strip()
...
Filesystem  Size Used Avail Capacity Mounted on
/dev/ad0s1a 713M 313M 343M 48% /
devfs   1.0K 1.0K  0B 100% /dev
/dev/ad0s1e 514M 2.1M 471M  0% /tmp
/dev/ad0s1f 4.3G 2.5G 1.4G 64% /usr
/dev/ad0s1d 2.0G 121M 1.7G  6% /var

```

stdout可以使用read(),readline(),readlines()等方法

## 三、方便的函数

#### 1、subprocess.call (*popenargs , **kwargs )
> 执行命令，并等待命令结束，再返回子进程的返回值。参数同Popen。 例`subprocess.call('ifconfig',shell=True)`

文档，其实是这样的：
```python
'''源码'''
def call(*popenargs, **kwargs):
      return Popen(*popenargs, **kwargs).wait()
```

####  2、 subprocess.check_call (*popenargs , **kwargs )
> 执行上面的call命令，并检查返回值，如果子进程返回非0，则会抛出CalledProcessError异常，这个异常会有个returncode

属性，记录子进程的返回值。
```python
'''源码'''
def check_call(*popenargs, **kwargs):
    retcode = call(*popenargs, **kwargs)
    if retcode:
        cmd = kwargs.get("args")
        if cmd is None:
            cmd = popenargs[0]
        raise CalledProcessError(retcode, cmd)
    return 0
```

```
>>> subprocess.check_call('ifconfig')
>>> subprocess.call('noifconfig')
Traceback (most recent call last):
File "<stdin>", line 1, in <module>
File "/usr/local/lib/python2.7/subprocess.py", line 493, in call
return Popen(*popenargs, **kwargs).wait()
File "/usr/local/lib/python2.7/subprocess.py", line 679, in __init__
errread, errwrite)
File "/usr/local/lib/python2.7/subprocess.py", line 1228, in _execute_child
raise child_exception
OSError: [Errno 2] No such file or directory
```
异常子进程里抛出的异常，会在父进程中再次抛出。并且，异常会有个叫child_traceback的额外属性，这是个包含子进程错误traceback信息的字符串。
遇到最多的错误回是 OSError，比如执行了一个并不存在的子程序就会产生OSError。
另外，如果使用错误的参数调用Popen，会抛出ValueError。
当子程序返回非0时，check_call()还会产生CalledProcessError 异常。

安全性不像其他的popen函数，本函数不会调用/bin/sh来解释命令，也就是说，命令中的每一个字符都会被安全地传递到子进程里。

#### 3、check_output
>执行程序，并返回其标准输出.

```python
''' 源码'''
def check_output(*popenargs, **kwargs):
    
    if 'stdout' in kwargs:
        raise ValueError('stdout argument not allowed, it will be overridden.')
    
    if 'input' in kwargs and kwargs['input'] is None:
        # Explicitly passing input=None was previously equivalent to passing an
        # empty string. That is maintained here for backwards compatibility.
        kwargs['input'] = '' if kwargs.get('universal_newlines', False) else b''
    
    return run(*popenargs, stdout=PIPE, timeout=timeout, check=True,
               **kwargs).stdout
```

p=subprocess.check_output('ifconfig')

结果是所有行/n分割的一个字符串可以直接print出来 这里开始

#### 4、Popen对象
 
产生对象 `p=subprocess.Popen("df -h",shell=True,stdout=subprocess.PIPE)`

Popen对象有以下方法：

1. Popen.poll() 检查子进程是否已结束，设置并返回returncode属性。

2. Popen.wait() 等待子进程结束，设置并返回returncode属性。
> 注意： 如果子进程输出了大量数据到stdout或者stderr的管道，并达到了系统pipe的缓存大小的话，子进程会等待父进程读取管道，而父进程此时正wait着的话，将会产生传说中的死锁，后果是非常严重滴。建议使用communicate() 来避免这种情况的发生。

3. Popen.communicate(input=None)
和子进程交互：发送数据到stdin，并从stdout和stderr读数据，直到收到EOF。等待子进程结束。可选的input如有有的话，要为字符串类型。

  此函数返回一个元组： (stdoutdata , stderrdata ) 。

注意，要给子进程的stdin发送数据，则Popen的时候，stdin要为PIPE；同理，要可以接收数据的话，stdout或者stderr也要为PIPE。

```
p1=subprocess.Popen('cat /etc/passwd',shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
p2=subprocess.Popen('grep 0:0',shell=True,stdin=p1.stdout,stdout=subprocess.PIPE)
p.communicate()  
# (b'Filesystem  Size Used Avail’,None)
```

4. Popen.send_signal(signal) 给子进程发送signal信号。 注意：windows下目前只支持发送SIGTERM，等效于下面的terminate() 。

5. Popen.terminate() 停止子进程。Posix下是发送SIGTERM信号。windows下是调用TerminateProcess()这个API。

6. Popen.kill() 杀死子进程。Posix下是发送SIGKILL信号。windows下和terminate() 无异。

7. Popen.stdin 如果stdin 参数是PIPE，此属性就是一个文件对象，否则为None 。

8. Popen.stdout  如果stdout参数是PIPE，此属性就是一个文件对象，否则为None 。

9. Popen.stderr  如果stderr 参数是PIPE，此属性就是一个文件对象，否则为None 。

10. Popen.pid 子进程的进程号。注意，如果shell 参数为True，这属性指的是子shell的进程号。
 
11. Popen.returncode  子程序的返回值，由poll()或者wait()设置，间接地也由communicate()设置。

如果为None，表示子进程还没终止。

如果为负数-N的话，表示子进程被N号信号终止。（仅限*nux）

## 用subprocess来代替其他函数都可以用subprocess来完成

> 假定是用 “from subprocess import *” 来导入模块的：

1. 代替shell命令：

  p=`ls -l` 等效于  p=Popen(['ls','-l'],stdout=PIPE).communicate()[0]

2. 代替shell管道：

  p=`dmesg | grep cpu` 等效于

```python
import subprocess

p1=Popen(['dmesg'],stdout=PIPE)
p2=Popen(['grep','cpu'],stdin=p1.stdout,stdout=PIPE)
output = p2.communicate()[0]
# cpu0: <ACPI CPU> on acpi0\nacpi_throttle0: <ACPI CPU Throttling> on cpu0\n

p1=subprocess.Popen('cat /etc/passwd',shell=True,stdout=subprocess.PIPE)
p2=subprocess.Popen('grep 0:0',shell=True,stdin=p1.stdout,stdout=subprocess.PIPE)
p3=subprocess.Popen("cut -d ':' -f 7",shell=True,stdin=p2.stdout,stdout=subprocess.PIPE)
print p3.stdout.read()

```


3. 代替os.system()

  lsl = os.system('ls '+'-l') 等效于  `p=Popen('ls -l', shell=True) lsl=os.waitpid(p.pid,0)[1]`
  注意： 通常并不需要用shell来调用程序。用subprocess可以更方便地得到子程序的返回值。

其实，更真实的替换是：
``` 
try:
retcode = call(“mycmd” + ” myarg”, shell=True)
if retcode < 0:
print >>sys.stderr, “Child was terminated by signal”, -retcode
else:
print >>sys.stderr, “Child returned”, retcode
except OSError, e:
print >>sys.stderr, “Execution failed:”, e
```

4. 代替os.spawn系列

 * P_NOWAIT的例子： pid = os.spawnlp(os.P_NOWAIT, “/bin/mycmd”, “mycmd”, “myarg”) 等效于 pid = Popen(["/bin/mycmd", "myarg"]).pid
 * P_WAIT的例子： retcode = os.spawnlp(os.P_WAIT, “/bin/mycmd”, “mycmd”, “myarg”) 等效于 retcode = call(["/bin/mycmd", "myarg"])
 


5. 返回值处理
   
```python
pipe = os.popen(“cmd”, ‘w')
...
rc = pipe.close()
if rc != None and rc % 256:
print “There were some errors”
```

等效于

```
process = Popen(“cmd”, ‘w', shell=True, stdin=PIPE)
...
process.stdin.close()
if process.wait() != 0:
print “There were some errors”
```
