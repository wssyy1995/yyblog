# yuanzu=([1,2,3],[4,5,6],[7,8,9])
# list=[l[0]for l in yuanzu]
# print(list)
#
# # form 格式
# <form method="post">
#     {{ form.csrf_token }}
#     {{ form.username.label }}<br>
#     {{ form.username }}<br>
#     {% if form.username.errors %}
#         {% for message in form.username.errors %}
#         <small class="error">{{ message }}</small><br>
#         {% endfor %}
#     {% endif %}
#     {{ form.password.label }}<br>
#     {{ form.password }}<br>
#     {% if form.password.errors %}
#         {% for message in form.password.errors %}
#         <small class="error">{{ message }}</small><br>
#         {% endfor %}
#     {% endif %}
#     {{ form.remember }}{{ form.remember.label }}<br>
#     {{ form.submit }}<br>
# </form>
#
#

import time,datetime
timestamp=time.time()
print(timestamp)
print(type(time.time()))
timelocal=time.localtime(timestamp)
print(timelocal)
timelocal_s=time.strftime("%Y-%m-%d",time.localtime(timestamp))
print(type(timelocal_s))


