######### definition de la class falsh card

class FalshCards:
    ''' definition des flashcards'''
    def __init__(self, name, mot,traduction, phrase, theme, difficulte, maitrise, illustrationpath, soundpath):
        self._name=name
        self._word=mot
        self._trad=traduction
        self._exemple=phrase
        self._thema=theme
        self._howhard=difficulte
        self._level=maitrise
        self._image=illustrationpath
        self._pronounciation=soundpath
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
    def prononciation(self):
        return self._pronounciation
    def __str__(self):
        print("name : ", self.name)
        print("mot : ", self.word)
        print("traduction : ", self.trad)
        print("exemple :", self.exemple)
        print("theme : ", self.thema)
        print("difficulte : ", self.howhard)
        print("niveau de maitrise : ", self.level)
        # reste a afficher l'image et le son
        
