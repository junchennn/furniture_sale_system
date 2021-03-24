# Django Furniture System

This is a very simple shopping basket built with Django.

The site displays products' name, price and invetory. Users can add and remove products to their basket and edit quantity within it. 

The site also include simple user and authentication functions. Each new user receives a "fund" of £1087.65 to purchase items on the site. Simple messages are given out when the user does not have sufficient fund in the account or the item is out of stock. 

The search bar enables user to look up and item, with link to update the item information. However, invetory and user details can only be updated by admin users. 

To get this project running you need to have Python and virtualenv installed. Please activate virtualenv with this command:

```
source bin/active
```

Next install the project dependencies with (plese note pacakage libraries are also within this repository)

```
pip install -r requirements.txt
```

Now you can run the project with this command

```
python manage.py runserver
```

To quit the server press "Ctrl-C".

To create an admin account run the command below:

```
python manage.py createsuperuser
```
The exiting databse stores product information read from "problem1_inventory.csv". 

To test admin functions and inspect django admin site, please run the server and login with test admin account:
```
admin
wsp1234
```
