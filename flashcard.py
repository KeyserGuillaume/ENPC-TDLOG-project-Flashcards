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
    def nature(self):
        return self._nature
    @property
    def prononciation(self):
        return self._pronounciation
    @property
    def tablename(self):
        return self._tablename
    
    def register(self):
        print("name : ", self.name)
        print("mot : ", self.word)
        print("traduction : ", self.trad)
        print("exemple :", self.exemple)
        print("theme : ", self.thema)
        print("difficulte : ", self.howhard)
        print("niveau de maitrise : ", self.level)
        print("nature : ", self.nature)
        print("langue : ", self.tablename)
        print("image : ", self.image)
        print("son : ", self.prononciation)
        # reste a afficher l'image et le son
        
