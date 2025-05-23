## Điện Thanh Liêm Shop ##

### Documentations

**Demonstration Video:** [link](https://drive.google.com/file/d/1ye77Qocw_qQ2avx6V66eVjA9k1hriTxF/view?usp=sharing)

**Final Project Report:** [link](https://github.com/Konic-NLP/final-project-OOAD/blob/version_4.27/Project%207.pdf)

**Final Class Diagram:** [link](https://github.com/Konic-NLP/final-project-OOAD/blob/version_4.27/Project7%20UML.pdf)

**UML for Project5:** [link](https://github.com/Konic-NLP/final-project-OOAD/blob/version_4.27/Project5%20UML.pdf)

**UML for Project6:** [link](https://github.com/Konic-NLP/final-project-OOAD/blob/version_4.27/Project6%20UML.pdf)

**Documentation of UML changes:** [link](https://docs.google.com/document/d/19sNARZsjykJEfHG_ropwVkZsUiufORlpjCKaFUAuUww/edit?usp=sharing)

### OO Patterns

1. **MTV**

   The **MTV** (a variant of MVC, means Model, Template and Views) pattern built-in Django really brings the whole system loose coupling and high cohesion. It split different functions into different modules. The models in the MTV pattern, which are defined in the models.py files, handle the object-relational mapping between the system and the database.It offer the API for us to execute query and extract or store the data. The templates in the MTV pattern are made up of multiple HTML for different pages, which plays the role of view in MVC to display the UI to the users. They contain the surface static contents, including text and pictures of the web pages, and they also contain functions written in javascript, which can fulfill the basic interactions between the user and the system. The views in the MTV pattern mediate between the models and the templates, like the controller in MVC, passing front-end requests to the model and passing back-end information to the templates (or to the user). 
   
2. **Decorator**
   
   The Decorator pattern in Django framework is functional-based:  the decorator function wraps up other functions. In our project, 
   Namely, in our system, we force the user to log in if they want to add items to or edit the shopping cart. To achieve this, a login function wrap the functions written in the view.py of the cart folder, which handles the add item request, edit request, visit cart request, and delete cart request. Before running those functions, the system will call the decorator function login first, judging if the user is in login status, and then it will call the function wrapped in the decorator. 

3. **Command**

   The command pattern is used in our project. The template receives the request from the users and it plays the role of the invoker since the template decouples from the view,  who is in charge of processing the request and response to the user. The URL route plays the role of command, which get the request and send it to the suitable object(function) in the file to process the request.
   
4. **Proxy**

  proxy pattern implemented by the class meta property in the django framework. The client can access to the goodinfo tables by the proxy tabels while cannot change the data in the goodsinfo(like insert,delete). And the order method in goodsinfoproxy can be ordered by one fied without impacting the order of goodsinfo.

### Install and Run ###

first, please create a virtual enviorment

` pip install virtualenv`

`virtualenv [the name for the environment]     e.g   virtualenv venv`

- On linux: python3 -m venv env


activate the virtual enviroment

`source activate [the name for the virtualvenv]`

- On linux: source env/bin/activate

To intall all the packages:

```python
pip install -Ur requirements.txt 
```

To run the project: 

```
python manage.py runserver
```

## Restart Gunicorn
sudo systemctl restart gunicorn


### Super user:
Username: trucvip123
Email address: 
Password: lumia930
