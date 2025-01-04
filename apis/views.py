from django.shortcuts import render, redirect
import http.client
import json
import math
import requests

# Create your views here.

def apis(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    
    if x_forwarded_for:
        data = x_forwarded_for.split(",")
    else:
        data = "Veri yok"

    return render(request, "apis/apis.html", {"data": data})


def soccer(request):
    # teams = ["Galatasaray", "Fenerbahçe", "Beşiktaş", "Trabzonspor", "Başakşehir", "Sivasspor", "Alanyaspor", "Göztepe", "Konyaspor", "Gaziantep", "Antalyaspor", "Malatyaspor", "Rizespor", "Denizlispor", "Kayserispor", "Ankaragücü", "Kasımpaşa", "Gençlerbirliği", "Erzurumspor", "Karagümrük"]

    result = league()

    teams, number, matches = result

    combined = zip(teams, number, matches)

    return render(request, "apis/soccer.html", {"combined": combined})


def matches(request):
    result = soccer2()

    home_teams, away_teams, scores, dates = result

    combined = zip(home_teams, away_teams, scores, dates)

    return render(request, "apis/matches.html", {"combined": combined})


def weather(request):
    if request.method == "POST":
        city = request.POST["city"]
        result = hava(city)

        date, day, degree, description = result
        description = [i.capitalize() for i in description]
        degree = round_float(degree)
        degree = [str(i) + "°C" for i in degree]

        combined = zip(date, day, degree, description)

        return render(request, "apis/weather.html", {"combined": combined})
    return render(request, "apis/weather.html")


def currency(request):
    conn = http.client.HTTPSConnection("api.collectapi.com")

    headers = {
        'content-type': "application/json",
        'authorization': "apikey 5oGAiwnuaBuT0Ghvkoty59:7hXU2RIQRKz3T01zv33R1X"
        }

    conn.request("GET", "/economy/currencyToAll?int=1&base=USD", headers=headers)

    res = conn.getresponse()
    data = res.read()
    data = json.loads(data.decode("utf-8"))

    if data["success"]:
        for i in range(len(data["result"]["data"])):
            if data["result"]["data"][i]["code"] == "TRY":
                usd = data["result"]["data"][i]['calculatedstr']
                eur = float(usd) / float(eur_usd)
            elif data["result"]["data"][i]["code"] == "EUR":
                eur_usd = data["result"]["data"][i]['calculatedstr']
            else:
                pass

        return render(request, "apis/currency.html", {'usd': usd, 'eur': str(round(eur, 2))})
    else:
        pass


def soccer2():
    conn = http.client.HTTPSConnection("api.collectapi.com")

    headers = {
        "content-type": "application/json",
        "authorization": "apikey 5oGAiwnuaBuT0Ghvkoty59:7hXU2RIQRKz3T01zv33R1X",
    }

    conn.request("GET", "/football/results?data.league=super-lig", headers=headers)

    res = conn.getresponse()
    data = res.read()
    veri = json.loads(data.decode("utf-8"))
    dates = []
    home_teams = []
    away_teams = []
    scores = []

    result = ""

    for i in range(len(veri["result"])):
        dates.append(
            f"{str(veri['result'][i]['date'])[8:10]}-{str(veri['result'][i]['date'])[5:7]}-{str(veri['result'][i]['date'])[:4]} {str(int(veri['result'][i]['date'][11:13])+3)}:{str(veri['result'][i]['date'])[14:16]}"
        )
        home_teams.append(veri["result"][i]["home"])
        away_teams.append(veri["result"][i]["away"])
        if str(veri["result"][i]["skor"]) == "undefined-undefined":
            scores.append("Maç Sonucu Yok")
        else:
            scores.append(veri["result"][i]["skor"])

    for i in range(len(veri["result"])):
        if True:
            dates.append(
                f"{str(veri['result'][i]['date'])[8:10]}-{str(veri['result'][i]['date'])[5:7]}-{str(veri['result'][i]['date'])[:4]} {str(int(veri['result'][i]['date'][11:13])+3)}:{str(veri['result'][i]['date'])[14:16]}"
            )
            if str(veri["result"][i]["skor"]) == "undefined-undefined":
                result += f"{str(veri['result'][i]['home'])} - {str(veri['result'][i]['away'])}\n\n"
            else:
                result += f"{str(veri['result'][i]['home'])} {str(veri['result'][i]['skor'])} {str(veri['result'][i]['away'])}\n\n"
    return home_teams, away_teams, scores, dates


def league():
    conn = http.client.HTTPSConnection("api.collectapi.com")

    headers = {
        "content-type": "application/json",
        "authorization": "apikey 5oGAiwnuaBuT0Ghvkoty59:7hXU2RIQRKz3T01zv33R1X",
    }

    conn.request("GET", "/football/league?data.league=super-lig", headers=headers)

    res = conn.getresponse()
    data = res.read()
    veri = json.loads(data.decode("utf-8"))
    name = []
    number = []
    match = []

    for i in range(len(veri["result"])):
        name.append(veri["result"][i]["team"])

    for i in range(len(veri["result"])):
        number.append(veri["result"][i]["point"])

    for i in range(len(veri["result"])):
        match.append(veri["result"][i]["play"])

    return name, number, match


def hava(city):
    conn = http.client.HTTPSConnection("api.collectapi.com")

    headers = {
        "content-type": "application/json",
        "authorization": "apikey 5oGAiwnuaBuT0Ghvkoty59:7hXU2RIQRKz3T01zv33R1X",
    }

    conn.request(
        "GET", f"/weather/getWeather?data.lang=en-US&data.city={city}", headers=headers
    )

    res = conn.getresponse()
    data = res.read()
    data = data.decode("utf-8")
    veri = json.loads(data)
    date = []
    day = []
    degree = []
    description = []

    for i in range(0, 7):
        date.append(veri["result"][i]["date"])
        day.append(veri["result"][i]["day"])
        degree.append(veri["result"][i]["degree"])
        description.append(veri["result"][i]["description"])

    return date, day, degree, description


def round_float(values):
    new_values = []
    for value in values:
        if float(value) % 1 >= 0.5:
            new_values.append(math.ceil(float(value)))
        else:
            new_values.append(math.floor(float(value)))
    
    return new_values


    

# def get_location(ip):
#     url = f"http://api.ipstack.com/{ip}?access_key=YOUR_ACCESS_KEY"
#     response = requests.get(url)
#     data = response.json()
#     city = data.get('city', 'Bilinmiyor')
#     return city