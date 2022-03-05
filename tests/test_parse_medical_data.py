from parse_medical_data.read_medical_data import ReadMedicalData

def main():
    medical_data = ReadMedicalData().get_medical_data()

    medical_data.set_medical_data("1")
    option_by_hierarchy = medical_data.get_options()
    answer = medical_data.get_answer()
    link = medical_data.get_link()

    medical_data.set_medical_data("1.1.1")
    option_by_hierarchy = medical_data.get_options()
    answer = medical_data.get_answer()
    link = medical_data.get_link()

    break_point = 1


if __name__ == "__main__":
    main()