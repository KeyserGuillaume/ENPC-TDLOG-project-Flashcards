from lxml import etree
### on part d'un xml deja existant avec des réglages de base et on permet de les modifier via interface

################################## chargement du fichier XML

### charger un xml
def getXmlTree(path):
    return etree.parse(path)

### chargement du xmk de settings
#filename = "AppSettings.xml"
filename = "controller/AppSettings.xml"
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

def getAllGameNames():
    return ["dragdrop","memory","hotcold","pointto","rightwrong"]

### acces a une liste de tous les settings
def getAllSettings():
    defaultLangage = readSettings("/user/default/langage")
    username = readSettings("/user/default/username")
    allGameNames = getAllGameNames()
    nbCards = [readSettings("/user/game[name='"+gamename+"']/nbCards") for gamename in allGameNames]
    timerChrono = [readSettings("/user/game[name='"+gamename+"']/chrono") for gamename in allGameNames]
    return [defaultLangage,username,nbCards,timerChrono]

### modifications specifiques
def changeUser(newdata):
    changeSettings("/user/default/username", newdata)
def changeLangage(newdata):
    changeSettings("/user/default/langage", newdata)
def changeNbCards(newdata,gamename):
    changeSettings("/user/game[name='"+gamename+"']/nbCards", newdata)
def changeChrono(newdata,gamename):
    changeSettings("/user/game[name='"+gamename+"']/chrono", newdata)