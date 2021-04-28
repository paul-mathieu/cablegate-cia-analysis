import cablegate
import cia

def main():
    print('=== cablegate data ===')
    cablegate.convert_data()
    print('=== cia data ===')
    cia.convert_data()

if __name__ == "__main__":
    main()
