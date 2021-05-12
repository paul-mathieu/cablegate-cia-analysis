import cablegate


def main():
    print('=== cablegate data ===')
    # cablegate.display()
    # cablegate.extract_data()
    cablegate.reformat_country_names()
    print('=== cia data ===')
    # cia.convert_data()


if __name__ == "__main__":
    main()
