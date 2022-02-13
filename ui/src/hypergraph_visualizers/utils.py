from typing import Iterable

from matplotlib import colors, cm
from matplotlib.cm import ScalarMappable

COLOR_SCHEME = cm.jet


def create_color_mapping(a: Iterable[int]):
    """
    :param a: последовательность целых чисел
    :return: список цветов
    """
    try:
        low, *_, high = sorted(a)
    except ValueError:
        low, high = 1, 1
    norm = colors.Normalize(vmin=low, vmax=high, clip=True)
    mapper = ScalarMappable(norm=norm, cmap=COLOR_SCHEME)
    return [
        mapper.to_rgba(n)
        for n in a
    ]
