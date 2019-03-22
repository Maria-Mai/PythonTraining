#this programm TODO

from classes.dnaConverter import DnaConverter
import sys, os

def main_menu():

    #todo test mit bild und text jeweils beide algos und dann auskommentieren
    convert = DnaConverter()
    #convert.encode_with_segments("/home/mai/PycharmProjects/pythonUNI/icon.bmp")
    convert.decode_with_segments("/home/mai/PycharmProjects/pythonUNI/icon.bmp.dna.segments")

    #convert.encode_with_base_algo("/home/mai/PycharmProjects/pythonUNI/text.txt")


    """
    # after start
    print("Willkommen zu Ihrem ganz persoenlichen DNA-Konvertierungsprogramm. "
          "Was möchten Sie tun? \n")
    print("Konvertieren - Geben Sie k ein. \n")
    print("Beenden. Geben Sie b ein. \n")

    #choice = input("Eingabe: ")
    #TODO exec_menu(choice) """

def exec_menu(choice):
    os.system("clear")
    try:
        menu_actions[choice]()
    except KeyError:
        print("Sie haben eine falsche Eingabe gemacht. Probieren Sie es nocheinmal")
        menu_actions["menu"]()

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

    # handle general input mistakes
    if(path.endswith(".txt") == False and path.endswith(".bmp") == False):
        #input has wrong format
        print("Sie haben ein falsches Format eingegeben. "
          "Versuchen Sie es nocheinmal von vorne.")
        main_menu()

    converter = DnaConverter()

    if(choice == "basis"):
        converter.encode_with_base_algo(path)
        print("Moechten Sie diese Datei noch kompriieren?\n")
        compress = input("ja oder nein: ")

        if(compress is "ja"):
            return 0 #TODO

    elif(choice == "segmente"):
        converter.encode_with_segments(path)
    else:
        print("Etwas ist schiefgegangen. Neustart")
        main_menu()

    print("Fertig. Sie finden die Datei in ihrem aktuellen Verzeichnis.")

def quit_programm():
    sys.exit()

menu_actions = {
    "menu" : main_menu,
    "k" : convert,
    "b" : quit_programm
}

main_menu()