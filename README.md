# Backend for biller

schema: http://techaso.ddns.net/api/schema/redoc/

## Contribution rules
### Naming
- Variables : all lower case. eg: `lower_case_variable`
- Constants : all caps. eg: `INSTALLED_APPS`
- Classes : Use pascal notation. eg: `UserController`
- Variable naming must be clear and self-explanatory 

### Functions
- Follow single responsibility rule.
- Name of the function must short and self-explanatory.
- Avoid nesting.
- Break complex logic into simple functions.
- Avoid `try .. expect` instead add more validations.
- Mention the type of argument passing
- Mention the return type of a function

### Unit Test
- Below is the 3 step commands to be executed
- `coverage run --source='.' manage.py test`
- `coverage report`
- `coverage xml -o coverage.xml`

### Start Server 
- Below is the command to start a Django server
- `python manage.py runserver`

### Elastic Search Indexing
- Below is the command to index elastic search
- `echo y | python manage.py search_index --rebuild`

### Create a new app 
- Below is the command to create a new app with our custom template
- `python manage.py generate_app <app_name>`
