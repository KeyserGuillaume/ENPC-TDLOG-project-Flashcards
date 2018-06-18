######### definition de la class flash card

## il faut encore gerer quand les objects sont multiples (liste de traduction par exemple)

class FlashCards:
    """
    defining flashcards
    name : nombre genere automatiquement ; cle primaire
    word : chaine de caractere
    trad : chaine de caractere
    exemple : chaine de caractere
    thema : chaine de caractere
    howhard : nombre entre 0 et 9
    level : nombre entre 0 et 9
    image : chaine de caractere
    pronounciation : chaine de caractere
    nature : chaine de caractere
    tablename : langue de la traduction (chaine de caractere)
    """
    def __init__(self, name="", mot="",traduction="", phrase="", theme="", difficulte=0,
                 maitrise=0, illustrationpath="", soundfile="", nature="", langue=""):
        self._name = name
        self._word = mot
        self._trad = traduction
        self._exemple = phrase
        self._thema = theme
        self._howhard = difficulte
        self._level = maitrise
        self._image = illustrationpath
        self._pronounciation = soundfile
        self._nature = nature
        self._tablename = langue 
    @property
    def name(self):
        return self._name
    @property
    def word(self):
        return self._word
    @property
    def trad(self):
        return self._trad
    @property
    def exemple(self):
        return self._exemple
    @property
    def thema(self):
        return self._thema
    @property
    def howhard(self):
        return self._howhard
    @property
    def level(self):
        return self._level
    @property
    def image(self):
        return self._image
    @property
    def pronounciation(self):
        return self._pronounciation
    @property
    def nature(self):
        return self._nature
    @property
    def tablename(self):
        return self._tablename
    
    def __str__(self):
        result= " name : "+str(self.name)+"\n mot : "+self.word+"\n traduction : "+self.trad+"\n exemple : "
        #si la phrase d'exemple est trop longue, je la coupe en deux pour qu'elle se voit dans l'interface de viewCard.py
        if len(self._exemple) > 20:
            splitExemple=self._exemple.split()
            moitie=len(splitExemple)//2
            partie1=" ".join(splitExemple[:moitie])
            partie2=" ".join(splitExemple[moitie:])
            result+=partie1+"\n "+partie2
        else:
            result+=self.exemple
        result+="\n theme : "+self.thema+"\n difficulte : "+str(self.howhard)+"\n niveau de maitrise : "+str(self.level)+"\n image : "+self.image+"\n son : "+self.prononciation+"\n nature : "+self.nature+"\n langue : "+self.tablename
        return result
        
    #l'affichage de la carte sans les chemins vers le fichier son et le fichier image
    def shortStr(self):
        result= " name : "+str(self.name)+"\n mot : "+self.word+"\n traduction : "+self.trad+"\n exemple :\n"
        if len(self._exemple) > 20:
            splitExemple=self._exemple.split()
            moitie=len(splitExemple)//2
            partie1=" ".join(splitExemple[:moitie])
            partie2=" ".join(splitExemple[moitie:])
            result+=partie1+"\n "+partie2
        else:
            result+=self.exemple
        result+="\n theme : "+self.thema+"\n difficulte : "+str(self.howhard)+"\n niveau de maitrise : "+str(self.level)+"\n nature : "+self.nature
        return result
        
