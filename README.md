##LVTUBEN_CD_TOOLKIL
it's a MS for platform/toolkit under the python3, and designed for automatic CI/CD.

# How to setup on your local
1. prepare the requirements for Lvtuben

        # pip3 install -r requirements.txt  
2. migrate the databases for Lvtuben

        # python3 manage.py makemigrations
        # python3 manage.py migrate
                
3. create the super user for management

        # python3 manage.py createsuperuser
        
4. first run your own env

        # python manage.py runserver 0.0.0.0:8000
        
5. request to Lvtuben as "http://127.0.0.1:8000/" via browser


