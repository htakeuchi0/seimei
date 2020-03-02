"""名前情報の構造体を含むモジュール．
"""

# pylint: disable=R0913, R0903

class SeimeiItem:
    """名前情報を保持する構造体．

    Attributes;
        family: 姓
        given: 名
        char_kakusuu_dict: 姓名に含まれる画数の辞書
        gokaku_dict: 五格の辞書
        gogyo_dict: 陰陽五行の辞書
    """
    def __init__(self, family, given, char_kakusuu_dict,
                 gokaku_dict, gogyo_dict):
        self.family = family
        self.given = given
        self.char_kakusuu_dict = char_kakusuu_dict
        self.gokaku_dict = gokaku_dict
        self.gogyo_dict = gogyo_dict

    def show(self):
        """名前情報を標準出力する．
        """
        print(str(self))

    def __str__(self):
        text = ''
        text += '[姓名]\n'
        text += '- 姓: {}\n'.format(self.family)
        text += '- 名: {}\n'.format(self.given)

        text += '\n'
        text += '[画数]\n'
        for key, val in self.char_kakusuu_dict.items():
            text += '- {}: {:2d}\n'.format(key, val)

        text += '\n'
        text += '[姓名判断]\n'
        for key, val in self.gokaku_dict.items():
            text += '- {}: {:2d}\n'.format(key, val)

        text += '\n'
        text += '[陰陽五行]\n'
        for key, val in self.gogyo_dict.items():
            text += '- {}: {:2}\n'.format(key, val)

        return text
