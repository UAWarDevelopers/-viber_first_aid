from __future__ import annotations

import re
from typing import Dict


class MedicalData:
    """
    """

    LEVEL_SEPERATOR = "."
    START_LEVEL = "0"

    medicals_data = list()

    def __init__(self, hierarchy: str, option: str, answer: str, link: str) -> None:
        """
        """
        self.__hierarchy = hierarchy
        self.__option = option
        self.__answer = answer
        self.__link = link

    def __set_medical_data(self, hierarchy: str, option: str, answer: str, link: str) -> None:
        """
        """
        self.__hierarchy = hierarchy
        self.__option = option
        self.__answer = answer
        self.__link = link

    def __get_next_level_regex(self) -> str:
        """
        """
        next_level_regex = rf"^{self.__hierarchy}.\d+$"

        return next_level_regex

    """
    def __get_back_level(self) -> str:
        previous_level_elements = self.__hierarchy.split(self.LEVEL_SEPERATOR)[:-1]
        back_level = self.LEVEL_SEPERATOR.join(previous_level_elements)

        return back_level
    """

    def __init_begin_level(self) -> None:
        self.__hierarchy = self.START_LEVEL
        self.__option = None
        self.__answer = "Що трапилось?"
        self.__link = None

    def __get_begin_options(self) -> Dict[str, str]:
        """
        """
        option_by_hierarchy = dict()

        for medical_data in self.medicals_data:
            if self.LEVEL_SEPERATOR not in medical_data.__hierarchy:
                option_by_hierarchy[medical_data.__hierarchy] = medical_data.__option

        return option_by_hierarchy

    def is_valid_hierarchy(self, hierarchy: str) -> bool:
        """
        """
        is_valid_hierarchy = False

        if hierarchy == self.START_LEVEL:
            is_valid_hierarchy = True
        else:
            for medical_data in self.medicals_data:
                if hierarchy == medical_data.__hierarchy:
                    is_valid_hierarchy = True

        return is_valid_hierarchy

    def set_medical_data(self, hierarchy: str) -> None:
        """
        """
        if hierarchy == self.START_LEVEL:
            self.__init_begin_level()
        else:
            for medical_data in self.medicals_data:
                if hierarchy == medical_data.__hierarchy:
                    self.__set_medical_data(
                        medical_data.__hierarchy,
                        medical_data.__option,
                        medical_data.__answer,
                        medical_data.__link
                    )

    def get_options(self) -> Dict[str, str]:
        """
        """
        option_by_hierarchy = dict()

        if self.__hierarchy == self.START_LEVEL:
            option_by_hierarchy = self.__get_begin_options()
        else:
            next_level_regex = self.__get_next_level_regex()

            for medical_data in self.medicals_data:
                if re.match(next_level_regex, medical_data.__hierarchy):
                    option_by_hierarchy[medical_data.__hierarchy] = medical_data.__option

        return option_by_hierarchy

    """
    def select_back_option(self):
        back_level = self.__get_back_level()

        for medical_data in self.medicals_data:
            is_same_hierarchy = back_level == medical_data.__hierarchy and back_level in self.__hierarchy

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
    """

    """
    def get_back_options(self) -> List[str]:
        if self.__hierarchy == self.START_LEVEL:
            back_options = self.get_begin_options()
        else:
            back_options = self.get_next_options()

        return back_options
    """

    def get_answer(self) -> str:
        """
        """
        return self.__answer

    def get_link(self) -> str:
        """
        """
        link = None
        if isinstance(self.__link, str):
            link = self.__link

        return link

    def save_to_list(self, medical_data: MedicalData) -> None:
        """
        """
        self.medicals_data.append(medical_data)
