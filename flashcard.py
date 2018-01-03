######### definition de la class falsh card

## il faut encore gerer quand les objects sont multiples (liste de traduction par exemple)

class FlashCards:
    ''' definition des flashcards'''
    def __init__(self, name, mot,traduction, phrase, theme, difficulte, maitrise, illustrationpath, soundpath, nature, langue):
        self._name=name  #nombre genere automatiquement ; cle primaire
        self._word=mot   #chaine de caractere
        self._trad=traduction   #chaine de caractere
        self._exemple=phrase   #chaine de caractere
        self._thema=theme    #chaine de caractere
        self._howhard=difficulte   #nombre entre 0 et 9
        self._level=maitrise     #nombre entre 0 et 9
        self._image=illustrationpath   #chaine de caractere
        self._pronounciation=soundpath   #chaine de caractere
        self._nature=nature     #chaine de caractere
        self._tablename=langue #langue de la traduction  #chaine de caractere
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
    def prononciation(self):
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
        result= " name : "+str(self.name)+"\n mot : "+self.word+"\n traduction : "+self.trad+"\n exemple : "
        if len(self._exemple) > 20:
            splitExemple=self._exemple.split()
            moitie=len(splitExemple)//2
            partie1=" ".join(splitExemple[:moitie])
            partie2=" ".join(splitExemple[moitie:])
            result+=partie1+"\n "+partie2
        else:
            result+=self.exemple
        result+="\n theme : "+self.thema+"\n difficulte : "+str(self.howhard)+"\n niveau de maitrise : "+str(self.level)
        return result
        