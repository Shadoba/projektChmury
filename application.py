from flask import Flask, render_template
from flask import request, redirect, url_for, flash, Response
from neo4j import GraphDatabase, basic_auth
import json
app = Flask(__name__)

driver = GraphDatabase.driver("bolt://hobby-ggmjfgnijmdigbkefdlcnfdl.dbs.graphenedb.com:24787", auth=basic_auth("projekt", "b.wIrJQavCY0en.BT8QhbmncyKgimYn"))

def add_person(tx, name, surname, country):
    tx.run("MERGE (a:Person {name: $name, surname: $surname, country: $country}) ",
           name=name, surname=surname, country=country)

def link_people(tx, to, ffrom, link):
    query = "MATCH (a:Person), (b:Person) WHERE ID(a) = "+to+" AND ID(b) = "+ffrom+" MERGE (a)-[:"+link+"]->(b)"
    tx.run(query)

def exterminate_person(tx, idx):
    query = "MATCH (a:Person) WHERE ID(a) = "+idx+" DETACH DELETE (a)"
    tx.run(query)

def print_all_people_table(tx):
    rtnstr = ""
    for record in tx.run("MATCH (a:Person)"
                         "RETURN a.name as name, a.surname as surname, a.country as country"):
        rtnstr = rtnstr + "<tr><td>" + record["name"] + "</td>" + "<td>" + record["surname"] + "</td>" + "<td>" + record["country"] + "</td></tr>\n"
    return rtnstr

# UNUSED
# def print_all_people_select(tx):
#     rtnstr = "<select>"
#     for record in tx.run("MATCH (a:Person) RETURN a.name, a.surname, a.country"):
#         rtnstr = rtnstr + "<option value = {name: " + record["a.name"] + ", surname: " + record["a.surname"] + ", country: " + record["a.country"] + "}>" + record["a.name"] + ", " + record["a.surname"] + ", " + record["a.country"] + "</option>"
#     return rtnstr+"</select>"
# UNUSED
# def print_all_people(tx):
#     rtnstr = "["
#     for record in tx.run("MATCH (a:Person) RETURN a.name, a.surname, a.country, ID(a) as idx"):
#         rtnstr = rtnstr + "{name: " + record["a.name"] + ", surname: " + record["a.surname"] + ", country: " + record["a.country"] + ", id: " + record["idx"] + "},"
#     if rtnstr.endswith(','):
#         rtnstr = rtnstr[0:-2]
#     return rtnstr+"]"

def print_all_people_list(tx):
    rtn = []
    for record in tx.run("MATCH (a:Person) RETURN a.name, a.surname, a.country, ID(a) as idx"):
        rtn.append([record["a.name"], record["a.surname"], record["a.country"], record["idx"]])
    return rtn

#DEBUG
# def action():
#     # with driver.session() as session:
#     #     session.write_transaction(add_person, "Arthur", "Pentragon", "England")
#     #     session.write_transaction(add_person, "Tata", "Muminka", "Japan")
#     #     session.write_transaction(add_person, "Jan", "Paweł", "Poland")
#     rtnstr = print_all_people_table(driver.session())
#     return rtnstr

def get_linked_people(tx, idx, link):
    rtnstr = ""
    query = "MATCH (a:Person)-[:" +link+ "]->(friend) WHERE ID(a) = " +idx+ " RETURN friend.name as name, friend.surname as surname, friend.country as country"
    for record in tx.run(query):
        rtnstr = rtnstr + "<tr><td>" + record["name"] + "</td>" + "<td>" + record["surname"] + "</td>" + "<td>" + record["country"] + "</td></tr>\n"
    return rtnstr

@app.route("/")
def main():
    table = print_all_people_list(driver.session())
    return render_template('index.html', table=table)

@app.route("/addPerson", methods=['POST'])
def addPerson():
    form = json.loads(request.data)
    passed = True
    try:
        print(form["name"])
        print(form["surname"])
        print(form["country"])
    except:
        passed = False

    if not passed:
        return Response("Invalid JSON", status=418 , mimetype='html/text')

    add_person(driver.session(), form["name"], form["surname"], form["country"])
    return Response("Record inserted", status=200 , mimetype='html/text')


@app.route("/linkPeople", methods=['POST'])
def linkPeople():
    form = json.loads(request.data)
    passed = True
    try:
        print(form["to"])
        print(form["from"])
        print(form["link"])
    except:
        passed = False

    if not passed:
        return Response("Invalid JSON", status=418 , mimetype='html/text')

    link_people(driver.session(), form["to"], form["from"], form["link"])
    return Response("Link inserted", status=200 , mimetype='html/text')

@app.route("/getRelations", methods=['POST'])
def getRelations():
    form = json.loads(request.data)
    passed = True
    try:
        print(form["id"])
        print(form["link"])
    except:
        passed = False

    if not passed:
        return Response("Invalid JSON", status=418 , mimetype='html/text')

    content = get_linked_people(driver.session(), form["id"], form["link"])
    return content

@app.route("/deletePerson", methods=['POST'])
def deletePerson():
    form = json.loads(request.data)
    passed = True
    try:
        print(form["id"])
    except:
        passed = False

    if not passed:
        return Response("Invalid JSON", status=418 , mimetype='html/text')

    exterminate_person(driver.session(), form["id"])
    return Response("Person deleted", status=200 , mimetype='html/text')

@app.route("/update", methods=['POST'])
def update():
    table = print_all_people_table(driver.session())
    return table