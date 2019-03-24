#this script is the ui for the DNAConverter and the
# LempelZiv-Compression algorithm

from classes.DNAConverter import DnaConverter
from classes.LZWForDNA import LZWForDNA
import sys, os

""" displays the main menu after start"""
def main_menu():

    # after start
    print("Willkommen zu Ihrem ganz persoenlichen DNA-Konvertierungsprogramm. "
          "Was möchten Sie tun? \n")
    print("Konvertieren - Geben Sie k ein. \n")
    print("Konvertierung rückgängig machen - Geben Sie r ein.\n")
    print("Beenden. Geben Sie b ein. \n")

    choice = input("Eingabe: ")
    exec_menu(choice)

""" starts the right  method after input  """
def exec_menu(choice):
    os.system("clear")
    try:
        menu_actions[choice]()
    except KeyError:
        print("Sie haben eine falsche Eingabe gemacht. Probieren Sie es nocheinmal")
        menu_actions["menu"]()

""" method for converting into dna-string, can be with compression  """
def convert():
    print("Möchten Sie die Datei mit dem Basis-Algorithmus oder "
          "dem kompletten Algorithmus konvertieren? \n")
    print("Basis-Algorithmus - Geben Sie basis ein. \n")
    print("Kompletter Algorithmus mit Segmenten - Geben Sie segmente ein. \n")
    choice = input("Eingabe: ")

    if(choice != "basis" and choice != "segmente"):
        print("Sie haben eine flasche Eingabe getaetigt.\n")
        main_menu()

    # consol input BMP or ASCII-Text
    print("Geben Sie den absoluten Pfad zur Datei an, die Sie konvertieren möchten. "
          "Achten Sie bitte darauf, dass Ihre Datei das korrekte Format hat. (Entweder ASCII oder Bitmap)")
    path = input("Pfad: ")

    #check if file exists and check input format
    check_input_format(path)

    #start converting to dna string
    converter = DnaConverter()

    #basis algortihmus
    if(choice == "basis"):
        new_path = converter.encode_with_base_algo(path)
        print("Moechten Sie diese Datei noch komprimieren?")
        compression = input("Eingabe: ")

        #with compression
        if(compression == "ja"):
            compressor = LZWForDNA()
            new_compressed_path = compressor.encode(new_path)
            print("Fertig. Sie finden beide Dateien in ihrem aktuellen Verzeichnis.\n")
            print(new_path)
            print(new_compressed_path)
            main_menu()
        else:
            print("Fertig. Sie finden die Datei in ihrem aktuellen Verzeichnis.")
            print(new_path)
            main_menu()

    #algo with segments
    elif(choice == "segmente"):
        new_path = converter.encode_with_segments(path)
        print("Fertig. Sie finden die Datei in ihrem aktuellen Verzeichnis.\n")
        print(new_path)
        main_menu()

    else:
        print("Falsche Eingabe. Neustart")
        main_menu()

""" deconverting dna-string into previous input """
def reverse():
    print("Geben Sie den absoluten Dateipfad an \n")
    path = input("Pfad: ")

    # check if file exists
    exists = os.path.isfile(path)
    if exists:
        pass
    else:
        print("Der Pfad ist falsch.")
        main_menu()

    converter = DnaConverter()

    # deconvert basealgo with compression
    if("compress" in path):
        compressor = LZWForDNA()
        output_path = compressor.decode(path)
        unconverted_path = converter.decode_with_base_algo(output_path)
        print("Fertig. Sie finden beide Dateien in ihrem aktuellen Verzeichnis.\n")
        print(output_path)
        print(unconverted_path)
        main_menu()
    #with segments
    elif("segments" in path):
        output_path = converter.decode_with_segments(path)
        print("Fertig. Sie finden die Datei in ihrem aktuellen Verzeichnis.\n")
        print(output_path)
        main_menu()
    #base algo
    else:
        try:
            output_path = converter.decode_with_base_algo()
            print("Fertig. Sie finden die Datei in ihrem aktuellen Verzeichnis.")
            print(output_path)
            main_menu()
        except:
            print("Falsche Datei.")
            main_menu()

""" ends the programm """
def quit_programm():
    sys.exit()

""" handle general input mistakes """
def check_input_format(path):
    #check if file exists
    exists = os.path.isfile(path)
    if exists:
        pass
    else:
        print("Der Pfad ist falsch.")
        main_menu()

    #check format
    if (path.endswith(".txt") == False and path.endswith(".bmp") == False and path.endswith(".dib") == False):
        main_menu()

    #check ascii for text files
    elif (path.endswith(".txt")):
        try:
            with open(path, "r",  encoding = 'ascii') as file:
                input_file = file.read()
        except UnicodeDecodeError:
            print("Textdatei hat kein ASCII-Format.")
            main_menu()

#menu options
menu_actions = {
    "menu" : main_menu,
    "k" : convert,
    "r": reverse,
    "b" : quit_programm
}

#start
main_menu()