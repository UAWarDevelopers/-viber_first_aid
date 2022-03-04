from __future__ import annotations

import re
from typing import List, Optional


class MedicalData:
    """
    """

    LEVEL_SEPERATOR = "."
    LEVEL_BACK = " < "
    START_LEVEL = "0"

    medicals_data = list()

    def __init__(self, hierarchy: str, option: str, answer: str, link: str) -> None:
        """
        """
        self.__hierarchy = hierarchy
        self.__option = option
        self.__answer = answer
        self.__link = link

    def __set_medical_data_new(self, hierarchy: str, option: str, answer: str, link: str) -> None:
        """
        """
        self.__hierarchy = hierarchy
        self.__option = option
        self.__answer = answer
        self.__link = link

    def __get_next_level_regex_new(self) -> str:
        """
        """
        next_level_regex = rf"^{self.__hierarchy}.\d+$"

        return next_level_regex

    def __get_back_level_new(self) -> str:
        """
        """
        previous_level_elements = self.__hierarchy.split(self.LEVEL_SEPERATOR)[:-1]
        back_level = self.LEVEL_SEPERATOR.join(previous_level_elements)

        return back_level

    def init_begin_level(self) -> None:
        """
        """
        self.__hierarchy = self.START_LEVEL
        self.__option = None
        self.__answer = "Що трапилось?"
        self.__link = None

    def get_begin_options(self) -> List[str]:
        """
        """
        begin_options = list()

        for medical_data in self.medicals_data:
            if self.LEVEL_SEPERATOR not in medical_data.__hierarchy:
                begin_option = medical_data.__option
                begin_options.append(begin_option)

        return begin_options

    def select_next_option(self, option: str):
        """
        """
        next_level_regex = self.__get_next_level_regex_new()

        for medical_data in self.medicals_data:
            is_part_of_hierarchy = re.match(next_level_regex, medical_data.__hierarchy) or self.__hierarchy == self.START_LEVEL

            is_same_option = option == medical_data.__option

            if is_part_of_hierarchy and is_same_option:
                self.__set_medical_data_new(
                    medical_data.__hierarchy,
                    medical_data.__option,
                    medical_data.__answer,
                    medical_data.__link
                )

    def get_next_options(self) -> List[str]:
        """
        """
        next_options = list()

        next_level_regex = self.__get_next_level_regex_new()

        for medical_data in self.medicals_data:
            if re.match(next_level_regex, medical_data.__hierarchy):
                next_option = medical_data.__option
                next_options.append(next_option)

        next_options.append(self.LEVEL_BACK)

        return next_options

    def select_back_option(self):
        """

        """
        is_same_hierarchy = False
        back_level = self.__get_back_level_new()

        for medical_data in self.medicals_data:
            is_same_hierarchy = back_level == medical_data.__hierarchy

            if is_same_hierarchy:
                self.__set_medical_data_new(
                    medical_data.__hierarchy,
                    medical_data.__option,
                    medical_data.__answer,
                    medical_data.__link
                )
                break

        else:
            self.init_begin_level()

    def get_back_options(self) -> List[str]:
        """
        """
        if self.__hierarchy == self.START_LEVEL:
            back_options = self.get_begin_options()
        else:
            back_options = self.get_next_options()

        return back_options

    def get_answer(self) -> str:
        """
        """
        return self.__answer

    def get_link(self) -> str:
        """
        """
        return self.__link

    def save_to_list(self, medical_data: MedicalData) -> None:
        """
        """
        self.medicals_data.append(medical_data)
