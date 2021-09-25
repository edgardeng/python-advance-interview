import pymongo

'''
 pymongo-3.11.0

'''

uri = 'mongodb://%s:%s@%s' % ('root', '123456', 'localhost:27017')
# 链接数据库
client = pymongo.MongoClient(uri)
person = client.person            #   myclient["runoobdb"]

if __name__ == '__main__':
  student = person.teacher
  student.insert_one({'name': '张三'})
  result = student.find()
  for r in result:
    print(r)

