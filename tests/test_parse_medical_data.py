from parse_medical_data.read_medical_data import ReadMedicalData

def main():
    medical_data = ReadMedicalData().get_medical_data()

    #Нажато страт
    medical_data.init_begin_level()

    # Функціонал кнопки
    begin_options = medical_data.get_begin_options()
    #begin_options містить кнопки першого рівня

    #Нажато трерю кнопку "Кровотеча"
    third_button = begin_options[3]

    #Функціонал кнопки
    options = medical_data.get_options(third_button)
    # options містить кнопки рівня "Кровотеча"
    answer = medical_data.get_answer(third_button)
    link = medical_data.get_link(third_button)

    # Нажато кнопку "Так"
    button = options[0]

    # Функціонал кнопки
    options = medical_data.get_options(button)
    # options містить кнопки рівня "Так"
    answer = medical_data.get_answer(button)
    link = medical_data.get_link(button)

    # Назад 1
    back_options = medical_data.get_back_options()
    back_answer = medical_data.get_back_answer()
    back_link = medical_data.get_back_link()

    # Назад 2
    back_options = medical_data.get_back_options()
    back_answer = medical_data.get_back_answer()
    back_link = medical_data.get_back_link()

    break_point = 1

if __name__ == "__main__":
    main()

# is it all functions?
# yes, all public
# 

# TODO: 1. get_next_element