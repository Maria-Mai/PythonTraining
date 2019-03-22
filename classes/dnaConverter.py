#todo

import binascii
import csv
import random

class DnaConverter(object):

    huffmanDict = {}
    huffmanComplementDict = {}
    dnaDict = {"A":["C", "G", "T"], "C": ["G", "T", "A"], "G" : ["T", "A", "C"], "T": ["A", "C", "G"]}
    dnaComplementDict = {"A" : "T", "T" : "A", "C" : "G", "G" : "C"}
    dnaOffset = 25

    def __init__(self):
        huffmannTextFile = open("huffmanCode.dict", "r")
        csv_reader = csv.reader(huffmannTextFile, delimiter=",")
        for row in csv_reader:
            self.huffmanDict[row[0]] = row[1]
            self.huffmanComplementDict[row[1]] = row[0]

    """ encode without overlapping segments """
    def encode_with_base_algo(self, path):
        s1 = self.__S0_S1(path)
        s2 = self.__S1_S2(s1)
        s3 = self.__S2_S3(s1, s2)
        s4 = self.__S3_S4(s1, s2, s3)
        s5 = self.__S4_S5(s4, "A")
        open(path + ".dna", "w").write(s5)

    """ encoding with overlaping segemnts """
    def encode_with_segments(self, path):
        s1 = self.__S0_S1(path)
        s2 = self.__S1_S2(s1)
        s3 = self.__S2_S3(s1, s2)
        s4 = self.__S3_S4(s1, s2, s3)
        s5 = self.__S4_S5(s4, "A")

        segments = self.__split_S5(s5)
        finished_segments = self.__segment_i(segments, "12") #TODO get ID
        self.__save_segments_to_files(finished_segments, path)

        return finished_segments

    def decode_with_base_algo(self, path):
        s5 = self.__getS5(path)
        s4 = self.__S5_S4(s5, "A")
        s1 = self.__S4_S1(s4)
        bytes = self.__S1_Bytes(s1)

        # bmp todo in methode auslagern
        if(path.endswith("bmp.dna")):
            with open(path + ".reverse", "wb") as image: #todo ausgabe pfad .bmp am ende dmait öffnen
                image.write(bytearray(bytes))
        # text
        else:
            print(bytes) #TODO

    def decode_with_segments(self, path):

        finishedSegments = self.__getFinishedSegments(path)
        segments = self.__getSegments(finishedSegments)

        s5 = self.__segments_S5(segments)

        s4 = self.__S5_S4(s5, "A")
        s1 = self.__S4_S1(s4)
        bytes = self.__S1_Bytes(s1)

        # bmp todo in methode auslagern
        if ((".bmp" in path) or (".dib" in path)):
            with open(path + ".reverse", "wb") as image:  # todo ausgabe pfad .bmp am ende dmait öffnen
                image.write(bytearray(bytes))
        # text
        else:
            print(bytes)  # TODO


    #### private methods encoding #####

    """ file into byte string """ #TODO
    def __S0_S1(self, path):
        s1 = ""

        #bmp
        if (path.endswith(".bmp") == True):
            with open(path, 'rb') as image:
                f = image.read()
                imageByteArray = bytearray(f)

            for i in range(len(imageByteArray)):
                s1 = s1 + self.huffmanDict[str(imageByteArray[i])]

        #text
        else:
            with open(path, 'rb') as file:
                byte = file.read(1)
                while byte:
                    s1 = s1 + self.huffmanDict[str(int(binascii.hexlify(byte), 16))]
                    byte = file.read(1)

        return s1

    """ convert to base-3 using Huffman code """
    def __S1_S2(self, s1):
        n = len(s1)
        n_base3 = self.__decimal_base3(n)
        n_base3_length = len(n_base3)

        s2 = ""
        for i in range(20 - n_base3_length):
            s2 = s2 + "0"
        return (s2 + n_base3)

    """ make length multiple of 25 """
    def __S2_S3(self, s1, s2):
        s3 = ""
        n_s1_s2 = len(s1 + s2)
        #make it divisible integer by 25
        while (n_s1_s2 % 25) != 0:
            s3 = s3 + "0"
            n_s1_s2 += 1
        return s3

    """ set strings together """
    def __S3_S4(self, s1, s2, s3):
        s4 = s1 + s3 + s2
        return s4

    """ Convert into DNA """
    def __S4_S5(self, s4, start):
        #first element is from the A row per definition
        s5 = "" + self.dnaDict[start][int(s4[0])]
        #other elements depend on their previous element, which
        #defines the row
        for i in range(1, len(s4)):
            s5 = s5 + self.dnaDict[s5[i - 1]][int(s4[i])]
        return s5

    """ split into blocks of 100 nt with offset 25 (rest is overlapping) 
    build the reverse complement if i is odd"""
    def __split_S5(self, s5):
        n = len(s5) #length of s5
        numberOfSegments = int(n/self.dnaOffset)

        segments = []
        for i in range(numberOfSegments-3): #todo warum -3?
            segment = s5[i*25:i*25 + 100]
            print(len(segment))

            # not odd
            if((i % 2) == 0):
                segments.append(segment)
            #odd - need of complement
            else:
                segments.append(self.__reverse_complement(segment))

        return segments

    """  """
    def __segment_i(self, segments, id):

        appended_segments = []

        for i in range(len(segments)):

            i3 = self.__decimal_base3(i)
            while(len(i3) < 12):
                i3 = "0" + i3

            parity = 0
            for j in range(1,len(i3)):
                # sum all odd elements of i3
                if((j % 2 )!= 0):
                    parity = parity + int(i3[j-1])

            for k in range(1, len(id)):
                # sum all odd elemens of id
                if((j  % 2) != 0):
                    parity = parity + int(id[k-1])

            parity = parity % 3
            ix = id + i3 + str(parity)
            appended_segment = segments[i] + self.__S4_S5(ix, segments[i][-1])

            #surrond appended_segment to find reverse complement
            if(appended_segment[0] == "A"):
                appended_segment = "T" + appended_segment
            elif(appended_segment[0] == "T"):
                appended_segment = "A" + appended_segment
            else:
                if(random.randint(0,1) == 0):
                    appended_segment = "A" + appended_segment
                else:
                    appended_segment = "T" + appended_segment

            if(appended_segment[-1] == "C"):
                appended_segment = appended_segment + "G"
            elif(appended_segment[-1] == "G"):
                appended_segment = appended_segment + "C"
            else:
                if(random.randint(0,1) == 0):
                    appended_segment = appended_segment + "G"
                else:
                    appended_segment = appended_segment + "C"

            appended_segments.append(appended_segment)

        return appended_segments

    """ saving the overlapping segments """
    def __save_segments_to_files(self, finished_segments, path):
        with open(path + ".dna.segments", "w") as file:
            for segment in finished_segments:
                file.write(segment + "\n")

    ### private methods for decoding

    """ get segments from file """
    def __getFinishedSegments(self, path):
        finishedSegments = []
        with open(path, 'r') as file:
            for line in file:
                line = line.rstrip('\n')
                finishedSegments.append(line)

        return finishedSegments

    """ get segments without parity, but with their index """
    def __getSegments(self, finishedSegments):
        segments = {}

        for j in range(len(finishedSegments)):
            segment =  finishedSegments[j][1:101]
            # you could use the parity bit to check whether the data is broken
            ix = (finishedSegments[j][101:116])

            id = ix[0:2]
            i = ix[2:14]

            idBase3 = self.__S5_S4(id, segment[-1])
            iBase3 = self.__S5_S4(i, id[-1])

            iDecimal = self.__base3_decimal(iBase3)
            segments[iDecimal] = segment

        return segments

    """ make overlappping segments to s5 (one string wihtout overlapping)"""
    def __segments_S5(self, segments):
        s5 = ""

        for j in range(len(segments)):
            segment = segments[j]

            #odd
            if(j % 2 == 1):
                segment = self.__reverse_complement(segment)

            # here u could also check if the overlapping is correct
            if(j == 0):
                s5 = s5 + segment
            else:
                #remove overlapping
                s5 = s5 + segment[-25:]

        return s5

    """ open dna encoded file without segments"""
    def __getS5(self, path):
        s5 = ""
        with open(path, 'r') as file:
            s5 = file.read()
        return s5

    """ make s5 to s4, dna to base 3"""
    def __S5_S4(self, s5, start):
        s4 = ""

        #first element
        s4 = s4 + str(self.dnaDict[start].index(s5[0]))

        for i in range(1, len(s5)):
            s4 = s4 + str(self.dnaDict[s5[i-1]].index(s5[i]))

        return s4

    """ convert s4 to s1 """
    def __S4_S1(self, s4):
        s2 = s4[-20:]
        decimalNumber = self.__base3_decimal(s2)
        s1 = s4[0:decimalNumber]
        return s1

    """ base 3 to hex using complement huffman code """
    def __S1_Bytes(self, s1):
        bytes = ""

        i = 0
        while( i < len(s1)):
            if(s1[i:i+5] in self.huffmanComplementDict.keys()):
                bytes = bytes + "".join("%02x" % int(self.huffmanComplementDict[s1[i:i+5]]))
                i = i +5
            else:
                bytes = bytes + "".join("%02x" % int(self.huffmanComplementDict[s1[i:i + 6]]))
                i = i + 6

        bytes = binascii.unhexlify(bytes)
        return bytes

    ### private methods for encoding and decoding

    """ build the reverse complement of a dna string """
    def __reverse_complement(self, segment):
        reverseComplementSegment = ""
        #reverse string
        reverseSegment = segment[::-1]
        #build the complement
        for i in range(len(reverseSegment)): #todo check hinweg
            reverseComplementSegment = reverseComplementSegment + self.dnaComplementDict[reverseSegment[i]]
        return reverseComplementSegment

    """ converts a decimal number into base3-String"""
    def __decimal_base3(self, number):
        if(number == 0):
            return "0"

        base3String = ""

        while(number != 0):
            base3String = str((number % 3)) + base3String
            number = number//3

        return base3String

    """ convert a base3-string into a decimal number"""
    def __base3_decimal(self, base3String):
        base3 = int(base3String)

        if(base3 == 0):
            return 0

        number = 0
        expo = 1

        while base3 != 0:
            number = number + (base3 % 10) * expo
            base3 = base3//10
            expo = 3 * expo
        return number

