from lxml import etree
### on part d'un xml deja existant avec des réglages de base et on permet de les modifier via interface

################################## chargement du fichier XML

### charger un xml
def getXmlTree(path):
    return etree.parse(path)

### chargement du xmk de settings
#filename = "AppSettings.xml"
filename = "view/AppSettings.xml"
tree = getXmlTree(filename)

################################## fonctions d'acces generales

### modifier une zone donnée (par tag xpath) du xml (avec nouvelle valeur donnee)
def changeSettings(Tag_xpath, newData):
    # ex : Tag_xpath = "/user/game/nbCards"
    global tree
    global filename
    root = tree.getroot()
    chosenSetting = tree.xpath(Tag_xpath)
    if chosenSetting:
        for data in chosenSetting:
            # replace
            data.text=newData
            # save
            etree.ElementTree(root).write(filename, pretty_print=True)

### lire une zone donnée (par tag xpath) du xml
def readSettings(Tag_xpath):
    global tree
    chosenSetting = tree.xpath(Tag_xpath)
    if chosenSetting:
        return chosenSetting[0].text

################################## chargement du fichier XML
def getDefaultLanguage():
    return readSettings("/user/default/language")
    
def getUserName():
    return readSettings("/user/default/username")

def getPixabayKey():
    return readSettings("/user/default/pixabay_api_key")

def getAllGameNames():
    return ["dragdrop","memory","hotcold","pointto","rightwrong"]

### acces a une liste de tous les settings
def getAllSettings():
    defaultLangage = readSettings("/user/default/language")
    username = readSettings("/user/default/username")
    pixabay_api_key = readSettings("/user/default/pixabay_api_key")
    allGameNames = getAllGameNames()
    nbCards = [readSettings("/user/game[name='"+gamename+"']/nbCards") for gamename in allGameNames]
    timerChrono = [readSettings("/user/game[name='"+gamename+"']/chrono") for gamename in allGameNames]
    return [defaultLangage, username, pixabay_api_key, nbCards, timerChrono]

### access aux parametres d'un jeux donné
def getGameSettings(gamename,require):
    if require==0:
        nbCards = readSettings("/user/game[name='" + gamename + "']/nbCards")
        return int(nbCards)
    elif require==1:
        timer = readSettings("/user/game[name='" + gamename + "']/chrono")
    return int(timer)

### modifications specifiques
def changeUser(newdata):
    changeSettings("/user/default/username", newdata)
def changeLangage(newdata):
    changeSettings("/user/default/language", newdata)
def changeKey(newdata):
    changeSettings("/user/default/pixabay_api_key", newdata)
def changeNbCards(newdata,gamename):
    changeSettings("/user/game[name='"+gamename+"']/nbCards", newdata)
def changeChrono(newdata,gamename):
    changeSettings("/user/game[name='"+gamename+"']/chrono", newdata)