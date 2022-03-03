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

    def __get_medical_data(self, option: str) -> Optional[MedicalData]:
        """
        """
        required_medical_data = None

        for medical_data in self.medicals_data:
            is_start_hierarchy = self.__hierarchy == self.START_LEVEL
            is_part_of_hierarchy_forward = self.__hierarchy in medical_data.__hierarchy
            is_part_of_hierarchy_backward = medical_data.__hierarchy in self.__hierarchy

            is_part_of_hierarchy = is_part_of_hierarchy_forward or is_part_of_hierarchy_backward

            if option == medical_data.__option and (is_start_hierarchy or is_part_of_hierarchy):
                required_medical_data = medical_data
                break

        else:
            required_medical_data = self

        return required_medical_data

    def __set_medical_data(self, option: str) -> None:
        """
        """
        medical_data = self.__get_medical_data(option)
        self.__hierarchy = medical_data.__hierarchy
        self.__option = medical_data.__option
        self.__answer = medical_data.__answer
        self.__link = medical_data.__link

    def __get_next_level_regex(self, option: str) -> re.Pattern:
        """
        """
        medical_data = self.__get_medical_data(option)

        level = medical_data.__hierarchy
        next_level_regex = rf"^{level}.\d+$"

        return next_level_regex

    def __get_back_level(self) -> str:
        """
        """
        level = self.__hierarchy
        previous_level_elements = level.split(self.LEVEL_SEPERATOR)[:-1]
        back_level = self.LEVEL_SEPERATOR.join(previous_level_elements)

        return back_level

    def __get_back_option(self) -> List[str]:
        """
        """
        back_option = None

        back_level = self.__get_back_level()

        for medical_data in self.medicals_data:
            if back_level == medical_data.__hierarchy:
                back_option = medical_data.__option
                break

        return back_option

    def save_to_list(self, medical_data: MedicalData) -> None:
        """
        """
        self.medicals_data.append(medical_data)

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

    def get_options(self, option: str) -> List[str]:
        """
        """
        next_options = list()

        self.__set_medical_data(option)

        next_level_regex = self.__get_next_level_regex(option)

        for medical_data in self.medicals_data:
            possible_level = medical_data.__hierarchy

            if re.match(next_level_regex, possible_level):
                next_option = medical_data.__option
                next_options.append(next_option)

        next_options.append(self.LEVEL_BACK)

        return next_options

    def get_answer(self, option: str) -> str:
        """
        """
        self.__set_medical_data(option)

        return self.__answer

    def get_link(self, option: str) -> str:
        """
        """
        self.__set_medical_data(option)

        return self.__link

    def get_back_options(self) -> List[str]:
        """
        """
        back_options = list()

        option = self.__get_back_option()

        if option:
            back_options = self.get_options(option)
        else:
            self.init_begin_level()
            back_options = self.get_begin_options()

        return back_options

    def get_back_answer(self) -> str:
        """
        """
        option = self.__get_back_option()

        if option:
            self.__set_medical_data(option)
        else:
            pass # Can add introduction 

        return self.__answer

    def get_back_link(self) -> str:
        """
        """
        option = self.__get_back_option()

        if option:
            self.__set_medical_data(option)
        else:
            pass # Can add introduction 

        return self.__link
