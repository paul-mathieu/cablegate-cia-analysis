import cablegate
import cia_archive

def main():
    print('=== cablegate data ===')
    # cablegate.download_data()
    print('=== cia data ===')
    cia_archive.download_collection()

if __name__ == "__main__":
    main()
