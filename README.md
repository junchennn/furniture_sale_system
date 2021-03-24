# furniture_sale_system

This is a very simple shopping basket built with Django.

The site displays products' name, price and invetory. Users can add and remove products to/from their basket. The site also include simple user and authentication functions. Each new user receives a "fund" of £1087.65 to purchase items on the site. Simple messages are given out when the user does not have sufficient fund in the account or the item is out of stock. Invetory and user details can only be updated by admin users. 

To get this project running you need to have Python and virtualenv installed. Please activate virtualenv with this command:

```
source env/bin/active
```

Next install the project dependencies with

```
pip install -r requirements.txt
```

Now you can run the project with this command

```
python manage.py runserver
```

