
class FalshCards:
    ''' definition des flashcards'''
    def __init__(self, mot,traduction, phrase, theme, difficulte, maitrise, illustrationpath, soundpath):
        self._word=mot
        self._trad=traduction
        self._exemple=phrase
        self._thema=theme
        self._howhard=difficulte
        self._level=maitrise
        self._image=illustrationpath
        self._pronounciation=soundpath
    @property
    def world(self):
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
