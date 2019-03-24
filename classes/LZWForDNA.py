#this class implements the lempel ziv welch algo
#for DNA-strings. The staring table therfore has
#only 4 entries (all nucletids)

class LZWForDNA(object):

    table = {}

    """ this method compresses a file with the lzw algo
    and saves it to a new file"""
    def encode(self, path):
        #initalise table
        self.table = {"A": 0, "C": 1, "G": 2, "T": 3}

        text = self.__open_file(path)
        encoded_text = self.__encode_algo(text)
        output_path = self.__save_file(path, encoded_text)
        return output_path

    """ this method decompresses a file with the lzw algo
    and saves it to a new file"""
    def decode(self, path):
        #initalise table
        self.table = {0: "A", 1: "C", 2: "G", 3: "T"}
        text = self.__open_file(path)
        decoded_text = self.__decode_algo(text)
        output_path = self.__save_file(path, decoded_text)
        return output_path

    """ compression algorithums"""
    def __encode_algo(self, text):
        encoded_text = ""

        current_char = ""
        for i in range(len(text)):
            next_char = text[i]
            #check if pattern already in table
            if((current_char + next_char) in self.table):
                current_char = current_char + next_char
            else:
                #add new pattern to table
                self.table[current_char+next_char] = len(self.table)
                #add compressed pattern to the compression result
                encoded_text = encoded_text + str(self.table[current_char]) + ","
                current_char = next_char

        encoded_text = encoded_text + str(self.table[current_char]) + ","
        return encoded_text

    """ decompression algorithmus """
    def __decode_algo(self, text):
        #get patterns
        textarray = text.split(",")
        decoded_text = ""

        prev_code = int(textarray[0])
        decoded_text = decoded_text + self.table[prev_code]

        for i in range(1, len(textarray)-1):
            next_code = int(textarray[i])
            table_size = len(self.table)
            if(next_code in self.table):
                #add to table
                self.table[table_size] = self.table[prev_code] + self.table[next_code][0]
            else:
                #add to table
                self.table[table_size] = self.table[prev_code] + self.table[prev_code][0]
            decoded_text = decoded_text + self.table[next_code]
            prev_code = next_code

        return decoded_text

    """ open compressed or not compressed file"""
    def __open_file(self, path):
        text = ""
        with open(path, 'r') as file:
            text = file.read()
        return text

    """ save decompressed or compressed file"""
    def __save_file(self, path, text):
        output_path = ""

        #decompress
        if("compress" in path):
            output_path = path.replace(".compress", ".decompress")
        #compress
        else:
            output_path = path + ".compress"

        with open(output_path, "w") as file:
            file.write(text)
        return output_path