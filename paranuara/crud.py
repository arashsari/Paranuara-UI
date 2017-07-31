# CRUD for upload, add, update and delete contacts into datstore data model

from flask import Blueprint, current_app, redirect, render_template, request, \
    session, url_for, flash
from werkzeug.exceptions import BadRequest
import json
import os


builtin_list = list

global COMPANIES_DATA
COMPANIES_DATA = None
global PEOPLE_DATA
PEOPLE_DATA = None
crud = Blueprint('crud', __name__)
CACHED_FILE = None

@crud.route("/companies")
def get_companies():
    global COMPANIES_DATA

    COMPANIES_DATA = get_list('companies')
    return render_template(
        "companies.html",
        companies=COMPANIES_DATA,
        next_page_token=0)

@crud.route("/people")
def get_people():
    global PEOPLE_DATA
    PEOPLE_DATA = get_data('people')
    return render_template(
        "people.html",
        employees=PEOPLE_DATA,
        next_page_token=0)

def get_data(name):
    global COMPANIES_DATA
    global PEOPLE_DATA
    if name == 'companies':
        if COMPANIES_DATA and len(COMPANIES_DATA) > 0:
            return COMPANIES_DATA
    elif name == 'people':
        if PEOPLE_DATA and len(PEOPLE_DATA):
            return PEOPLE_DATA
    else:
        raise BadRequest('Your request data does not exist')

    resource_address = 'paranuara/resources/{}.json'.format(name)
    if os.path.exists(resource_address):
        with open(resource_address) as file:
            return json.load(file)


@crud.route("/")
def list():
    global PEOPLE_DATA
    name = request.args.get('name').lower()
    PEOPLE_DATA = get_list(name)
    return render_template(
        "companies.html",
        contacts=PEOPLE_DATA,
        next_page_token=0)


@crud.route('/<name>/find_employees', methods=['GET'])
def find_employees(name):
    employees=[]
    id = None
    message = None
    category = None
    if name:
        _comp = builtin_list(filter(lambda company: company['company'].lower() == name.lower(), get_data('companies')))
        if len(_comp) > 0: id = _comp[0].get('index', None)
        if id:
            employees = [employee for employee in get_data('people') if employee['company_id'] == id]
        else:
            print ('send back message that no employee')
            message = 'This company deos not have any employee -- Please Hire :-) !!'
            category = 'info'

        return render_template(
            "people.html",
            employees=employees,
            next_page_token=0,
            message=message,
            category = category
        )

@crud.route('/<name>/fruits', methods=['GET', 'POST'])
def find_fruits(name):
    id = None
    message = None
    category = None
    _faviourite_food =None
    if name:
        _faviourite_food = faviourite_food_list(name)
    else:
        message = 'Can\'t find entered name !!'
        category = 'info'
    return render_template(
        "employee_details.html",
        employee=_faviourite_food,
        next_page_token=0
    )

def faviourite_food_list(name):
    fruits= []
    vegetables =[]
    employees = [employee for employee in get_data('people') if employee['name'] == name]
    _favourite_food = employees[0]["favouriteFood"]
    for food in _favourite_food:
        if food in []:
            vegetables.append((food))
        else:
            fruits.append(food)
    return {"username": employees[0]['name'],
            "age": employees[0]['age'],
            "fruits": fruits,
            "vegetables": vegetables
            }

def get_list(name):
    resource_address = 'paranuara/resources/{}.json'.format(name)
    if os.path.exists(resource_address):

        with open(resource_address) as file:
            return json.load(file)

@crud.route('/<id>/edit', methods=['GET', 'POST'])
def edit(id):
    employees = [employee for employee in get_data('people') if employee['index'] == int(id)]
    print(employees)
    return render_template(
        "employee_details.html",
        employee=employees[0],
        next_page_token=0)

@crud.route('/mutual_friends/<name1>/<name2>', methods=['GET', 'POST'])
def mutual_friends(name1, name2):

    _mutual_friens = find_mutual_friens(name1, name2)

    return render_template(
        "employee_details.html",
        _mutual_friens=_mutual_friens[0],
        next_page_token=0,
        message= _mutual_friens[1],
        category= _mutual_friens[2]
    )

def find_mutual_friens(name1, name2):
    message = None
    category = None
    _employees = get_data('people')
    if name1 and name2:
        employees1 = [employee for employee in _employees if employee['name'] == name1]
        employees2 = [employee for employee in _employees if employee['name'] == name2]
        _mut_fri = []
        if employees1 and employees2:
            for em in [x for x in employees1['friends'] if x in employees2['friends']]:
                __mutfriend =  [employee for employee in get_data('people') if employee['index'] == em['index']][0]
                print(__mutfriend)
                if __mutfriend:
                    if __mutfriend['eyeColor'] == 'brown' and not __mutfriend['has_died']:
                        _mut_fri.append(__mutfriend)
        if employees1 and employees2:
            _mutual_friens = {
                'employees1':{
                    'name':employees1['name'],
                    'age':employees1['age'],
                    'address':employees1['address'],
                    'phone':employees1['phone'],
                },
                'employees2': {
                 'name': employees2['name'],
                 'age': employees2['age'],
                 'address': employees2['address'],
                 'phone': employees2['phone'],
                },
                 'friends':_mut_fri
            }
        else:
            message = 'Wrong name !!'
            category = 'denger'
    else:
        message = 'Two names required !!'
        category = 'denger'

    return _mutual_friens, message, category




