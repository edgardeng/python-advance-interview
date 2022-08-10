## Time
> [时间相关函数](https://docs.python.org/3/library/time.html)

**epoch** : the point where the time starts, January 1, 1970, 00:00:00 (UTC).

| From |  To | Use |
|:---- |:----|:---- |
| seconds since the epoch | struct_time in UTC | gmtime() |
| seconds since the epoch| struct_time in local time| localtime()| 
| struct_time in UTC| seconds since the epoch| calendar.timegm()| 
| struct_time in local time| seconds since the epoch| mktime() | 
| string | struct_time | mktime() |  


### 几个重要的函数

