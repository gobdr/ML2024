import warnings
warnings.simplefilter(action='ignore', category=DeprecationWarning)

from scanner import ImageScanner, Language
from parser import Parser

from person_info import PersonInfo, Goal, ActivityLevel, Gender

import pandas as pd
from regressor import Regressor


def main():
    person_info = PersonInfo(age=23,
                             gender=Gender.MALE.value,
                             height=180,
                             weight=85,
                             activity_level=ActivityLevel.MINIMAL.value,
                             goal=Goal.EXTREME_GAIN.value)
    path = "../data/img/IMG_25.png"
    product_info = Parser().parse(ImageScanner([Language.RUSSIAN]).scan_image(path))
    print(product_info)
    print(person_info)

    regressor = Regressor(pd.read_csv("../data/dataset/dataset.csv"))
    regressor.prepare_model()
    regressor.predict(person_info, product_info)


if __name__ == '__main__':
    main()
