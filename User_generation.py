from wish_list import *
from user_pass_role import *
from course_list import *



user="schriever@gmail.com"
'''
courses=[10955,10956,10954,10957]
user_add("Mark Schriever", user, "12345678", "Senior", "test", "s")
for course in courses:
    wish_add("schriever@gmail.com", course)
    print(course," added")

user="schriever@gmail.com"
courses=[10950,10951]
for course in courses:
    course_add("schriever@gmail.com", course)
    print(course," added")
'''    
print(wishlist_get("schriever@gmail.com"))
wish_remove(user,10957)
