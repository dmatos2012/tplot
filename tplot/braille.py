from typing import Iterable


def get_braille(s):
    """
    `s` specifies which dots in the desired braille character must be on ('1') and which must be off ('0').
    Dots in the 2x8 braille matrix are ordered top-down, left-to-right.
    The order of the '1's and '0's in `s` correspond to this.
    Schematic example:
    ▪    10
     ▪   01
    ▪▪ = 11
     ▪   01
    ⢵ = '10100111'

    More examples:
    '10000000' = ⠁ (only top left dot)
    '11001111' = ⢻
    '11111111' = ⣿
    '00000000' = ⠀ (empty braille character)
    """
    s = s[:3] + s[4:7] + s[3] + s[7]  # rearrange ISO/TR 11548-1 dot order to something more suitable
    return chr(0x2800 + int(s[::-1], 2))


def braille_bin(char):
    """ Inverse of get_braille() """
    s = ord(char) - 0x2800
    s = format(s, "b").rjust(8, "0")
    s = s[::-1]
    s = s[:3] + s[6] + s[3:6] + s[7]  # rearrange ISO/TR 11548-1 dot order to something more suitable
    return s


def is_braille(char: str):
    """ Return True if provided unicode character is a braille character. """
    return isinstance(char, str) and 0x2800 <= ord(char[0]) <= 0x28FF


def braille_from_xy(x: int, y: int):
    """
    Returns braille character with dot at x, y position filled in.
    Example: braille_from_xy(x=1, y=0) returns "⠈" (top right dot filled in)
    """
    if not 0 <= x <= 2 or not 0 <= y <= 3:
        raise ValueError("Invalid braille dot position.")
    s = ["0"]*8
    s[x*4+y] = "1"
    s = "".join(s)
    return get_braille(s)


def combine_braille(braille: Iterable[str]):
    """
    Returns braille character that combines dots of input braille characters.
    Example: combine_braille("⠁⠂") returns "⠃"
    """
    out_bin = 0b00000000
    for char in braille:
        braille_b = braille_bin(char)
        out_bin |= int(braille_b, 2)
    s = format(out_bin, "b").rjust(8, "0")
    return get_braille(s)


def draw_braille(x: float, y: float, canvas_str=None):
    """
    Returns braille character for given x, y position.
    If canvas_str is already a braille character, the new braille dot will be added to it.
    """
    print(x, y)
    x -= int(x)
    x = round(x + 0.5)  # 0 or 1
    y = round(y) - y
    print(y)
    y = round((y + 0.5) * 3)  # 0, 1, 2, or 3
    print(x, y)
    print("--")
    out = braille_from_xy(x, y)
    if is_braille(canvas_str):
        out = combine_braille([out, canvas_str])
    return out
