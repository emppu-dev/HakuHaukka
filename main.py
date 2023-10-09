import telegram.ext
import json, re
import requests

with open('config.json') as f:
    config = json.load(f)

TOKEN = str(config.get("TOKEN"))
db = str(config.get('db'))

def start(update, context):
    update.message.reply_text("""Hei!
Olen ilmainen botti, jonka avulla voit hakea tietoa ihmisistä heidän nimien tai puhelinnumeroidensa perusteella.

Komentoni ovat:
/start - Tämä komento.
/toiminta - Tietoa meidän toiminnasta.
/lahjoitus - Jos haluat tukea toimintaamme.
/nimi <kokonimi> - Hakee tietoja valitsemastasi henkilöstä etu ja suku nimen avulla.
/numero <puhelinnumero> - Hakee tietoja valitsemastasi henkilöstä puhelinnumeron avulla.
/kilpi <rekisterinumero> - Hakee tietoja valitsemastasi ajoneuvosta""")

def toiminta(update, context):
    update.message.reply_text("""OSINT eli avointen lähteiden tiedustelu on laillinen tapa kerätä tietoa julkisista lähteistä. Se perustuu julkisesti saatavilla oleviin tietoihin, joita käyttäjät ovat jakaneet itse internetissä.
Emme kerää, tallenna tai säilytä käyttäjien tietoja. Tietoturva ja yksityisyys ovat meille ensisijaisen tärkeitä, ja noudatamme soveltuvaa lainsäädäntöä ja eettisiä periaatteita.""")
    
def lahjoitus(update, context):
    update.message.reply_text("""Jos haluat tukea toimintaamme, voit tehdä lahjoituksen joihinkin näistä crypto osoitteista:
Bitcoin: bc1qus66hrsm43gag3nt2xuff73hg3g7pjsx628a2f
Ethereum: 0xDE423E0A222CBD20A81468Ea4d931F82476377c9
Litecoin: LXy8qud6vhzmA1fQFyd2iCAH3sZfzcLnPG
""")

def numero(update, context):
    chat_id = '@hakuhaukka'
    user_id = update.message.from_user.id
    member = context.bot.get_chat_member(chat_id=chat_id, user_id=user_id)
    if member.status in ['member', 'administrator', 'creator']:
        pass
    else:
        update.message.reply_text(f"Sinun pitää liittyä {chat_id} kanavaan käyttääksesi tätä komentoa.")
        return
    teksti = update.message.text
    nro = teksti.replace('/numero ', '')
    match = re.match("^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$", nro)
    hitit = 0
    if match:
        with open(db, "r", encoding="utf-8") as f:
            for line in f:
                parsed = line.split(":")
                if str(parsed[0]) in str(nro):
                    reply = []
                    if parsed[2] and parsed[3]:
                        reply.append(f"Nimi: {parsed[2]} {parsed[3]}")
                    if parsed[0]:
                        reply.append(f"Puhelin: +{parsed[0]}")
                    if parsed[4]:
                        reply.append(f"Sukupuoli: {parsed[4]}")
                    if parsed[5]:
                        reply.append(f"Paikkakunta: {parsed[5]}")
                    if parsed[8]:
                        reply.append(f"Työ: {parsed[8]}")
                    if parsed[9]:
                        reply.append(f"Syntymävuosi: {parsed[9]}")
                    if parsed[10]:
                        reply.append(f"Sähköposti: {parsed[10]}")
                    if reply:
                        update.message.reply_text("\n".join(reply))
                    hitit += 1
            if hitit == 0:
                update.message.reply_text(f"Numerolla `{nro}` ei löytynyt yhtäkään hakutulosta.")
    else:
        update.message.reply_text(f"Teit mahdollisesti jotain väärin.\n\nNäin käytät tätä komentoa oikein:\n/numero <puhelinnumero> (esim. +358400000000)")

def nimi(update, context):
    chat_id = '@hakuhaukka'
    user_id = update.message.from_user.id
    member = context.bot.get_chat_member(chat_id=chat_id, user_id=user_id)
    if member.status in ['member', 'administrator', 'creator']:
        pass
    else:
        update.message.reply_text(f"Sinun pitää liittyä {chat_id} kanavaan käyttääksesi tätä komentoa.")
        return
    try:
        nmi = [context.args[0],context.args[1]]
    except:
        update.message.reply_text(f"Teit mahdollisesti jotain väärin.\n\nNäin käytät tätä komentoa oikein:\n/nimi <kokonimi> (esim. Erkki Esimerkki)")
        return
    hitit = 0
    try:
        if len(nmi) == 2:
            with open(db, "r", encoding="utf-8") as f:
                for line in f:
                    parsed = line.split(":")
                    if nmi[0].lower() in parsed[2].lower() and nmi[1].lower() == parsed[3].lower():
                        reply = []
                        if parsed[2] and parsed[3]: reply.append(f"Nimi: {parsed[2]} {parsed[3]}")
                        if parsed[0]: reply.append(f"Puhelin: +{parsed[0]}")
                        if parsed[4]: reply.append(f"Sukupuoli: {parsed[4]}")
                        if parsed[5]: reply.append(f"Paikkakunta: {parsed[5]}")
                        if parsed[8]: reply.append(f"Työ: {parsed[8]}")
                        if parsed[9]: reply.append(f"Syntymävuosi: {parsed[9]}")
                        if parsed[10]: reply.append(f"Sähköposti: {parsed[10]}")
                        if reply: update.message.reply_text("\n".join(reply))
                        hitit += 1
                if hitit == 0:
                    update.message.reply_text(f"Nimellä `{nmi[0]} {nmi[1]}` ei löytynyt yhtäkään hakutulosta.")
        else:
            update.message.reply_text(f"Teit mahdollisesti jotain väärin.\n\nNäin käytät tätä komentoa oikein:\n/nimi <kokonimi> (esim. Erkki Esimerkki)")
    except:
        pass

def kilpi(update, context):
    chat_id = '@hakuhaukka'
    user_id = update.message.from_user.id
    member = context.bot.get_chat_member(chat_id=chat_id, user_id=user_id)
    if member.status in ['member', 'administrator', 'creator']:
        pass
    else:
        update.message.reply_text(f"Sinun pitää liittyä {chat_id} kanavaan käyttääksesi tätä komentoa.")
        return
    teksti = update.message.text
    rekisterikilpi = teksti.replace('/kilpi ', '')
    plate_pattern = r'^[A-Za-z]{3}-\d{3}$'
    if re.match(plate_pattern, rekisterikilpi):
        url = f'https://reko2.biltema.com/VehicleInformation/licensePlate/{rekisterikilpi}?market=3&language=FI'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            id = data["id"]
            manufacturer = data["manufacturer"]
            modelName = data["modelName"]
            producedFrom = data["producedFrom"]
            producedTo = data["producedTo"]
            description = data["description"]
            modelSeriesName = data["modelSeriesName"]
            drive = data["drive"]
            body = data["body"]
            valves = data["valves"]
            fuelMixtureFormation = data["fuelMixtureFormation"]
            fuel = data["fuel"]
            fuelTypeId = data["fuelTypeId"]
            engine = data["engine"]
            cylinders = data["cylinders"]
            cylinderVolumeCc = data["cylinderVolumeCc"]
            cylinderVolumeLiters = data["cylinderVolumeLiters"]
            motorCodes = data["motorCodes"]
            update.message.reply_text(f"Valmistaja: {manufacturer}\nMallin nimi: {modelName}\nTuotettu: {producedFrom} - {producedTo}\nKuvaus: {description}\nMallisarjan nimi: {modelSeriesName}\nVeto: {drive}\nRunko: {body}\nVenttiilit: {valves}\nPolttoaine: {fuel}\nMoottori: {engine}\nSylinterit: {cylinders}\nSylinteritilavuus (cm³): {cylinderVolumeCc}\nSylinteritilavuus (litrat): {cylinderVolumeLiters}\nMoottorikoodit: {motorCodes}")
        else:
            update.message.reply_text(f"Kilvellä `{rekisterikilpi}` ei löytynyt yhtäkään hakutulosta. {response.status_code}")
    else:
        update.message.reply_text("Teit mahdollisesti jotain väärin.\n\nNäin käytät tätä komentoa oikein:\n/kilpi <rekisterikilpi> (esim. ABC-123)")

updater = telegram.ext.Updater(TOKEN, use_context=True)
disp = updater.dispatcher

disp.add_handler(telegram.ext.CommandHandler("start", start))
disp.add_handler(telegram.ext.CommandHandler("toiminta", toiminta))
disp.add_handler(telegram.ext.CommandHandler("lahjoitus", lahjoitus))
disp.add_handler(telegram.ext.CommandHandler("nimi", nimi))
disp.add_handler(telegram.ext.CommandHandler("numero", numero))
disp.add_handler(telegram.ext.CommandHandler("kilpi", kilpi))

updater.start_polling()
print('Käynnissä!')
updater.idle()
