import os


def main():
    input_filename, output_filename = user_input()
    read_input_file(input_filename)
    

def user_input():
    """
    Gets the users input for the input TSV filename, printing the corresponding errors and otherwise returning a valid filename.
    Gets the users input for a output TSV filename, if it already exists it asks for a new name.
    """
    while True:     # While true keeps the loop running until a valid input is received
        try:
            input_filename = input("Please enter the input TSV filename: ")
            input_file_test = open(input_filename, 'r')
            input_file_test.close()
            print("Valid input file.")
            break       #Exits the loop as soon as a valid input filename has been entered
        
        except FileNotFoundError:
            print("File not found, please try again: ")
        except ValueError:
            print("ValueError, please try again: ")

    while True:
        try:   
            output_filename = input("Please enter an output TSV filename: ")
            output_file_test = open(output_filename, 'x')
            output_file_test.close()
            break

        except FileExistsError:
            print("This output file already exists, please enter a new output Filename: ")
    return input_filename, output_filename

# Reads the TSV file with the name given as argument. If successful, returns the
# a tuple of four lists: The column names, column types, distinct column values
# (list of lists) and the records (list of lists). Otherwise, raises an
# exception.
def read_input_file(input_file):
    """
    Puts the column names from the first line into a tuple.
    Takes the second line and puts the data type for each element into a tuple.
    Creates a tuple for each individual line and creates the records from the lines.
    Creates a tuple for the column values.
    The function prints and returns these four tuples.
    """
    file_object = open(input_file, 'r')     # Open the input file in read mode
    
    column_names = file_object.readline().strip()       # Read and strip the newline characters
    column_names_tuple = tuple(column_names.split())    # Convert it to a tuple and split 

    line2 = file_object.readline().strip()         # Read the 2nd line and strip the newline characters         
    data_types_list = line2.split(sep="\t")              # Create a list and split
    data_types = []                                # Empty list to append the data types to

    for element in data_types_list:
        if element.lower() == "true":               # Check for boolean in the list, removing case sensitivity
            data_types.append("true")
        elif element.lower() == "false":
            data_types.append("false")
        else:

            try:                                    # Check if it's an integer
                integer_value = int(element)
                data_types.append("int")
            except ValueError:

                try:
                    string = str(element)           # Check if it's a string
                    data_types.append("string")
                except ValueError:
                    data_types.append("No data type found") # In case no data type fits
                    raise TypeError
        
    data_types_tuple = tuple(data_types)    # Convert the list to a tuple


    lines = open(input_file,'r').read().splitlines()
    lines_column_names_removed = lines[1:]
    records = []

    for line in lines_column_names_removed:
        records.append(line.split(sep="\t"))

    number_columns = len(records[0])
    column_values = []

    for i in range(number_columns-1):
        column = []
        for rows in records:
            column.append(rows[i])
        column_values.append(column)

    column_values_tuple = tuple(column_values)
    records_tuple = tuple(records)

    
    print(f"{column_names_tuple},{data_types_tuple},{column_values_tuple},{records_tuple}")

    return [column_names_tuple], [data_types_tuple], [column_values], [records]


# Asks the user to input a comma-seperated list of unique integers between 1 and
# the given maximum value with the given minimum length using the given
# description, and returns the list of integers. Repeatedly asks the user upon
# invalid input.
def get_unique_integers_from_user(description, max_value, min_length):
    return []


# Checks that the given argument is a valid output file name. If this is not
# the case, raises an exception. Returns None.
def check_output_file(output_file):
    pass


# Writes the column names and the given records to the TSV file with the given
# name, only taking into account the given column indices in output columns and
# filters (a list of pairs of column indices and a list of corresponding values
# to exclude).
def write_output_file(output_file, column_names, records, output_columns, filters):
    with open(output_file, 'w') as output_tsv:
        pass


# Prints a summary of the copying and filtering operations to be applied to
# generate the TSV file for the given column names, the column indices provided
# as output columns to be copied and the filters (a list of pairs of column
# indices and a list of corresponding values to exclude).
def print_operations(column_names, output_columns, filters):
    pass


if __name__ == '__main__':
    main()