from parse_medical_data.read_medical_data import ReadMedicalData

def main():
    medical_data = ReadMedicalData().get_medical_data()

    medical_data.init_begin_level()
    option_by_hierarchy = medical_data.get_begin_options()
    answer = medical_data.get_answer()
    link = medical_data.get_link()

    medical_data.set_id("1.1")
    option_by_hierarchy = medical_data.get_next_options()
    answer = medical_data.get_answer()
    link = medical_data.get_link()


    """
    #Нажато страт
    medical_data.init_begin_level()

    # Функціонал кнопки
    g1 = medical_data.get_begin_options()
    #begin_options містить кнопки першого рівня

    #Нажато трерю кнопку "Кровотеча"
    button1 = g1[3]

    #Функціонал кнопки
    medical_data.select_next_option(button1)
    e1 = medical_data.get_next_options()
    e2 = medical_data.get_answer()
    e3 = medical_data.get_link()

    # Нажато кнопку "Так"
    button2 = e1[0]

    # Функціонал кнопки
    medical_data.select_next_option(button2)
    q1 = medical_data.get_next_options()
    q2 = medical_data.get_answer()
    q3 = medical_data.get_link()

    button3 = q1[0]
    medical_data.select_next_option(button3)
    d1 = medical_data.get_next_options()
    d2 = medical_data.get_answer()
    d3 = medical_data.get_link()

    # Назад 1
    medical_data.select_back_option()
    a1 = medical_data.get_back_options()
    a2 = medical_data.get_answer()
    a3 = medical_data.get_link()

    # Назад 2
    medical_data.select_back_option()
    s1 = medical_data.get_back_options()
    s2 = medical_data.get_answer()
    s3 = medical_data.get_link()

    medical_data.select_back_option()
    s21 = medical_data.get_back_options()
    s22 = medical_data.get_answer()
    s23 = medical_data.get_link()

    button23 = s21[0]
    medical_data.select_next_option(button23)
    d21 = medical_data.get_next_options()
    d22 = medical_data.get_answer()
    d23 = medical_data.get_link()
    """

    break_point = 1


if __name__ == "__main__":
    main()

# is it all functions?
# yes, all public
# 

# TODO: 1. get_next_element