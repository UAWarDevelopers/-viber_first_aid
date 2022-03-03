from parse_medical_data.read_medical_data import ReadMedicalData

def main():
    medical_data = ReadMedicalData().get_medical_data()

    # button = "Start"
    # button = "Серцево-легенева реанімація"
    #button = "Так"
    # button = "Дитина 1-8 років"
    button = "Back"
    try_back_option = "Підвищення цукру в крові"


    if button == "Start":
        begin_options = medical_data.get_begin_options()
        print(begin_options)
    elif button == "Back":
        next_options = medical_data.get_answer(try_back_option)
        back_options = medical_data.get_back_options()
        # return only on 1 level
        back_answer = medical_data.get_back_answer()
        back_link = medical_data.get_back_link()
    else:
        next_options = medical_data.get_next_options(button)
        # answer from bot
        # in table - column 'answer'
        answer = medical_data.get_answer(button)
        link = medical_data.get_link(button)
        print(next_options)
        print(answer)
        print(link)

    break_point = 1

if __name__ == "__main__":
    main()

# is it all functions?
# yes, all public
# 

# TODO: 1. get_next_element