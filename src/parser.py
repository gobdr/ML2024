from product_info import ProductInfo
from fuzzywuzzy import fuzz

TEXT_DELIMITER = ' '
NUMBER_DELIMITER = ','
DOT_DELIMITER = '.'


class Parser:

    def __init__(self):
        self.protein_keywords = ["белок", "белка", "белки", "белков"]
        self.fats_keywords = ["жир", "жиры", "жира", "жиров"]
        self.carbo_keywords = ["углевод", "углеводы", "углевода", "углеводов"]

    @staticmethod
    def __is_valid_char(char: str) -> bool:
        return char.isdigit() or char == NUMBER_DELIMITER

    def __find_next_number(self, tokens: list[str], start_position: int) -> str:
        number = ""
        for token in tokens[start_position:]:
            for char in token:
                if self.__is_valid_char(char):
                    number += char
                elif number:
                    return number
        return number

    @staticmethod
    def __validate_number(raw_str: str) -> float:
        processed_str = raw_str.replace(NUMBER_DELIMITER, DOT_DELIMITER)
        return float(processed_str)

    def __find_close_word(self, tokens: list[str], word: str) -> int:
        for i, token in enumerate(tokens):
            if fuzz.ratio(word, token.lower()) > 60:
                return i
        return -1

    def parse(self, text: list[str]) -> ProductInfo:
        protein, fats, carbo = 0.0, 0.0, 0.0
        for paragraph in text:
            tokens = paragraph.split(TEXT_DELIMITER)
            for keyword_list, value in [(self.protein_keywords, protein), (self.fats_keywords, fats), (self.carbo_keywords, carbo)]:
                for keyword in keyword_list:
                    index = self.__find_close_word(tokens, keyword)
                    if index != -1:
                        raw_number = self.__find_next_number(tokens, index + 1)
                        if raw_number:
                            validated_number = self.__validate_number(raw_number)
                            if keyword == keyword_list[0]:  # Присваиваем значение только если это первое ключевое слово
                                if keyword_list == self.protein_keywords:
                                    protein = validated_number
                                elif keyword_list == self.fats_keywords:
                                    fats = validated_number
                                elif keyword_list == self.carbo_keywords:
                                    carbo = validated_number
                            break  # Прерываем цикл после нахождения первого совпадения
        return ProductInfo(protein, fats, carbo)
