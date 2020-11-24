import sys, os, csv
import main

def filepath_conv(filepath):
    filepath = filepath.replace("\\","/")
    return filepath

def build_input_dict(image_dir_path):
    input_dict = {}
    # directory = os.fsencode(r'../data/tinysample1')
    directory = os.fsencode(image_dir_path)
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        input_dict.update({filename : image_dir_path + '/' + filename})
    return input_dict

def dump_csv(result_dict):
    csv_file = open('../dump/word_processing_output.csv', 'w')
    writer = csv.writer(csv_file)
    for key, val in result_dict.items():
        writer.writerow([key, val])

def word_processing(image_dict):
    '''
    Parse images of handwritten words into digital text strings.
    Parameters: image_dict, a dictionary of handwritten words. 
                    keys: database schema column name (TODO)
                    values: file path for the image
    Returns: result_dict, a dictionary of text resulting from the parsing.
                keys: database schema column name (TODO)
                values: text string of the word
    '''
    result_dict = {}
    for i in image_dict:
        img_loc = i
        img_path = filepath_conv(image_dict[i])
        img_word = main.main(img_path)
        result_dict.update({img_loc : img_word})

    return result_dict

# uncomment the following line for manual testing
# input_dict = build_input_dict('../data/tinysample1')

if len(sys.argv) == 2:
    input_dict = build_input_dict(sys.argv[1])
    print(input_dict)
    result_dict = word_processing(input_dict)
    dump_csv(result_dict)
else:
    print('Oops! Did you forget to pass in a command line argument?')
    print('Usage: python3 word_processing.py <filepath>')