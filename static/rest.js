function getRequestObject()
{
    if ( window.ActiveXObject)
    {
        return ( new ActiveXObject("Microsoft.XMLHTTP"));
    } else if (window.XMLHttpRequest)
    {
        return (new XMLHttpRequest());
    } else
    {
        return (null);
    }
}

function update() {
    request = getRequestObject();
    request.onreadystatechange = function() {
        if (request.readyState == 4)    {
            if(request.status != "200")
                alert("Something went worng!!!");
            else
            {
                var responseTxt = request.response;
                document.getElementById('viewAll').innerHTML = responseTxt;
            }
        }
   }
   request.open("POST", "/update", true);
   request.send(null);

   return true;
}

function addPerson(form) {
    var person = {};
    person.name = form.name.value;
    person.surname = form.surname.value;
    person.country = form.country.value;
    txt = JSON.stringify(person);
    request = getRequestObject() ;
    request.onreadystatechange = function() {
        if (request.readyState == 4)    {
            if(request.status != "200")
                alert("Something went wrong!!!");
        }
   }
   request.open("POST", "/addPerson", true);
   request.send(txt);

   return true;
}

function linkPeople(form)
{
    var people = {};
    people.to = form.to.value;
    people.from = form.from.value;
    people.link = form.link.value;
    txt = JSON.stringify(people);
    request = getRequestObject() ;
    request.onreadystatechange = function() {
        if (request.readyState == 4)    {
            if(request.status != "200")
                alert("Something went worng!!!");
        }
   }
   request.open("POST", "/linkPeople", true);
   request.send(txt);

   return true;
}

function getRelations(form) {
    var person = {};
    person.id = form.person.value;
    person.link = form.link.value;
    txt = JSON.stringify(person);
    request = getRequestObject() ;
    request.onreadystatechange = function() {
        if (request.readyState == 4)    {
            if(request.status != "200")
                alert("Something went worng!!!");
            else
            {
                var responseTxt = request.response;
                document.getElementById('viewRelations').innerHTML = responseTxt;
            }
        }
   }
   request.open("POST", "/getRelations", true);
   request.send(txt);

   return true;
}
