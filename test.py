#this class is a test for the algorithms
#todo mehr comments und mal testen

from classes.DNAConverter import DnaConverter
from classes.LZWForDNA import LZWForDNA

converter = DnaConverter()
compressor = LZWForDNA()

#text with base algo and compression (and back)
converter.encode_with_base_algo("/home/mai/PycharmProjects/pythonUNI/text.txt")
compressor.encode("/home/mai/PycharmProjects/pythonUNI/text.txt.dna")
compressor.decode("/home/mai/PycharmProjects/pythonUNI/text.txt.dna.compress")
converter.decode_with_base_algo("/home/mai/PycharmProjects/pythonUNI/text.txt.dna.decompress")

# text with segment algo (and back)
converter.encode_with_segments("/home/mai/PycharmProjects/pythonUNI/text.txt")
converter.decode_with_segments("/home/mai/PycharmProjects/pythonUNI/text.txt.dna.segments")

#bitmap with base algo and compression (and back)
converter.encode_with_base_algo("/home/mai/PycharmProjects/pythonUNI/icon.bmp")
compressor.encode("/home/mai/PycharmProjects/pythonUNI/icon.bmp.dna")
compressor.decode("/home/mai/PycharmProjects/pythonUNI/icon.bmp.dna.compress")
converter.decode_with_segments("/home/mai/PycharmProjects/pythonUNI/icon.bmp.dna.decompress")

#bitmap with segments (and back)
converter.encode_with_segments("/home/mai/PycharmProjects/pythonUNI/icon.bmp")
converter.decode_with_segments("/home/mai/PycharmProjects/pythonUNI/icon.bmp.dna.segments")

