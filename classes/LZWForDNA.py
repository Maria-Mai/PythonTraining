#todo
class LZWForDNA(object):

    table = {}

    def encode(self, path):
        self.table = {"A": 0, "C": 1, "G": 2, "T": 3}

        text = self.__open_file(path)
        encoded_text = self.__encode_algo(text)
        output_path = self.__save_file(path, encoded_text)
        return output_path

    def decode(self, path):
        self.table = {0: "A", 1: "C", 2: "G", 3: "T"}
        text = self.__open_file(path)
        self.__decode_algo(text)

    def __encode_algo(self, text):
        encoded_text = ""

        current_char = ""
        for i in range(len(text)):
            next_char = text[i]
            if((current_char + next_char) in self.table):
                current_char = current_char + next_char
            else:
                self.table[current_char+next_char] = len(self.table)
                encoded_text = encoded_text + str(self.table[current_char]) + ","
                current_char = next_char

        encoded_text = encoded_text + str(self.table[current_char]) + ","
        return encoded_text

    def __decode_algo(self, text):
        textarray = text.split(",")
        decoded_text = ""

        prev_code = int(textarray[0])
        decoded_text = decoded_text + self.table[prev_code]

        for i in range(1, len(textarray)-1):
            next_code = int(textarray[i])
            table_size = len(self.table)
            if(next_code in self.table):
                self.table[table_size] = self.table[prev_code] + self.table[next_code][0]
            else:
                self.table[table_size] = self.table[prev_code] + self.table[prev_code][0]
            decoded_text = decoded_text + self.table[next_code]
            prev_code = next_code

        print(decoded_text)
        return decoded_text

    def __open_file(self, path):
        text = ""
        with open(path, 'r') as file:
            text = file.read()
        return text

    def __save_file(self, path, text):
        output_path = ""

        #decompress
        if("compress" in path):
            output_path = path.replace(".compress")
            output_path = output_path + ".decompress"
        #compress
        else:
            output_path = path + ".compress"

        with open(output_path, "w") as file:
            file.write(text)

        return output_path