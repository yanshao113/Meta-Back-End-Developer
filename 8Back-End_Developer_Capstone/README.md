# Back-End Developer Capstone
## Little Lemon Web Application
### Setting up the Project
* pipenv install django
* pipenv shell
* django-admin startproject littlelemon
* python manage.py startapp restaurant
* pipenv install mysqlclient
* python manage.py makemigrations
* python manage.py mirgate
* python mangae.py createsuperuser
   * username: admin
   * email: admin@littlelemon.com
   * password: admin@littlelemon

### API
1.GET:http://127.0.0.1:8000/api/menu/ 
![](https://github.com/yanshao113/Meta-Back-End-Developer/blob/main/8Back-End_Developer_Capstone/screenshot/menu-get.png)

2.POST:http://127.0.0.1:8000/api/menu/ 
![](https://github.com/yanshao113/Meta-Back-End-Developer/blob/main/8Back-End_Developer_Capstone/screenshot/menu-post.png)

3.GET:http://127.0.0.1:8000/api/menu-items/1 
![](https://github.com/yanshao113/Meta-Back-End-Developer/blob/main/8Back-End_Developer_Capstone/screenshot/menu-item%3A1-get.png)

4.GET:http://127.0.0.1:8000/api/book/
![](https://github.com/yanshao113/Meta-Back-End-Developer/blob/main/8Back-End_Developer_Capstone/screenshot/book-get.png)

5.POST:http://127.0.0.1:8000/api/book/
![](https://github.com/yanshao113/Meta-Back-End-Developer/blob/main/8Back-End_Developer_Capstone/screenshot/book-post.png)

6.GET:http://127.0.0.1:8000/api/bookings/tables/
![](https://github.com/yanshao113/Meta-Back-End-Developer/blob/main/8Back-End_Developer_Capstone/screenshot/bookings-tables-get.png)

7. http://127.0.0.1:8000/auth/token/login/ && http://127.0.0.1:8000/auth/token/logout/
![](https://github.com/yanshao113/Meta-Back-End-Developer/blob/main/8Back-End_Developer_Capstone/screenshot/auth%3Atoken%3Alogin.png)


### TEST
* python manage.py test
