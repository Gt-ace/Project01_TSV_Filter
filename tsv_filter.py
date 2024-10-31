import os

def main():
    input_filename, output_filename = user_input()

    with open(input_filename, 'r') as file_object:  # Opens the input file and reads all the lines
        lines = file_object.readlines()

    check_output_file(output_filename)

    is_file_empty = empty_file_check(lines,output_filename)
    if is_file_empty == "true":
        return None

    column_names, data_types, column_values, records = read_input_file(lines)

    print_column_names(column_names, data_types)
    
    excluded_columns = get_unique_integers_from_user("Numbers of the columns to exclude (seperated by commas): ", len(column_names[0]), 0)

    output_columns = output_columns_converter(excluded_columns, column_names)

    print_column_names(column_names,data_types)

    filtered_columns = get_unique_integers_from_user("Numbers of the colums to filter for (seperated by commas): ", len(column_names[0]), 0)

    columns_to_filter_for, filters = filter(filtered_columns, column_names, column_values)

    print_operations(column_names, columns_to_filter_for, filters)
    
    write_output_file(f"{output_filename}.tsv", column_names, records, excluded_columns, filters)

def user_input():
    """
    Gets the users input for the input TSV filename, printing the corresponding errors and otherwise returning a valid filename.
    Gets the users input for a output TSV filename, if it already exists it asks for a new name.
    """
    while True:     # While true keeps the loop running until a break command is executed
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

    output_filename = input("Please enter an output TSV filename: ")

    return input_filename, output_filename

def empty_file_check(lines, output_filename):
    """
    This function checks if the input file is empty. If it is empty, it will create the output file and return None in the main function.
    """
    if len(lines) > 1:
        is_file_empty = "false"
    else:
        output_file = open(output_filename, 'w')
        is_file_empty = "true"
    return is_file_empty

def remove_line_breaks(input_file_records,lenght_column_names):
    """
    This function removes any line breaks that may be in the tsv input file. It does this by checking
    that the lenght is equal to the amount of column names. If this is not the case, the function adds
    the next line to that line which has too few columns. It also removes any double quotes that may
    appear when concatenating two strings.
    """
    x = 0
    corrected_file_records = []

    while x < len(input_file_records):
        if lenght_column_names != len(input_file_records[x]):
            input_file_records[x][-1] = input_file_records[x][-1].replace('"','') + ' ' + input_file_records[x + 1][0].replace('"', '')
            # The last element of record x is extented with the next records first element, both removing 
            # any double quotes.
            
            input_file_records[x].extend(input_file_records[x + 1][1:])
            corrected_file_records.append(input_file_records[x])

            x += 2  # Skips the next line since it has been added to line x

        else:
            corrected_file_records.append(input_file_records[x])
            x += 1

    return corrected_file_records

def read_input_file(lines):
    """
    Puts the column names from the first line into a list.
    Takes the second line and puts the data type for each element into a list.
    Creates the records from each line. Calls the remove_line_breaks function to remove line breaks
    Creates a list for the column values.
    The function prints and returns these four lists.
    """
    if lines[0].strip() in {'', '/'}:       # If first line in lines is empty or only contains '/', return 4 empty lists
        return [], [], [], []

    column_names = lines[0].rstrip("\n").split()        # The column names are the first line in lines. The newline character is removed using strip

    lines_column_names_removed = lines[1:]              # Lines without the column names.
    records = []                                        # Creating an empty list for the records

    for line in lines_column_names_removed:                 # This loop strips each line of the newline character and appends
        records.append(line.rstrip("\n").split(sep="\t"))   # each line to the records list, seperating elements with the tab character ("\t")

    corrected_records = remove_line_breaks(records,len(column_names)) 

    data_types_list = lines[1].split(sep="\t")      # Create a list of the first record in lines
    data_types = []                                 # Empty list to append the data types to

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

    number_columns = len(corrected_records[0])  # The number of columns is the lenght of any record
    column_values = []

    for i in range(number_columns):         # This loop goes through each column and row to check for distinct column values
        column = []
        for rows in corrected_records:
            column.append(rows[i])
        column_values.append(column)

    for index in range(number_columns):     # Sorts the column values alphabetically, numerically and false before true
        column_index = column_values[index]
        column_index.sort()

    check_list = []
    for i in range(len(column_values)):         # This loops checks for duplicates by removing any element
        current_column = column_values[i]       # that it has seen before, and adding new elements to the
                                                # check list.
        for num in current_column[:]:
            if num in check_list:
                current_column.remove(num)
            else:
                check_list.append(num)

    return [column_names], [data_types], [column_values], [corrected_records]

def print_column_names(column_names, data_types):
    print("\nThe TSV input file has the following columns:")
    for index in range(len(column_names[0])):
        print(f"{index+1}. {column_names[0][index]} ({data_types[0][index]})")

def get_unique_integers_from_user(description, max_value, min_length):
    """
    The user is asked for a comma seperated list of unique integers. The function checks that the elements of that list are within 1 and the max value.
    It also checks for duplicates and for the minimum lenght. Any invalid input will raise a ValueError and ask for a new input by the user.
    The function returns the valid list of integers given by the user.
    """
    while True:
        try:
            user_input_integers = input(f"{description}")

            if not user_input_integers.strip(): # Returns an empty list if the input is empty
                return []
            
            user_input_integers_list = user_input_integers.split(",")

            integers_list = []

            for num in user_input_integers_list:
                integers_list.append(int(num))

            for num in integers_list:               # Checking for numbers higher than the max value
                if num > max_value:
                    raise ValueError
                
            for num in integers_list:               # Checking for numbers lower than 1
                if num < 1:
                    raise ValueError

            integers_list_check = []                # Checking for duplicates
            for num in integers_list:
                if num in integers_list_check:
                    raise ValueError
                integers_list_check.append(num)

            if len(integers_list) < min_length:     # Checking for the minimum required lenght of the input
                raise ValueError
            else:
                break

        except EOFError:
            return []

        except ValueError:
            print("Invalid input, please try again.")
        
    return [integers_list]

def output_columns_converter(integers_list, column_names):
    """
    This function converts the colums which the user wishes to exclude to a list with the 
    column for the output file, basically an inverse of the user's input.
    """
    output_columns = []
    for i in range(1, len(column_names[0]) + 1):
        if i in integers_list[0]:
            pass
        else:
            output_columns.append(i)
    return output_columns

def check_output_file(output_file):
    """
    Checks that the given argument is a valid file name for the output file.
    Raises an exception if it's not the case, and returns none.
    """
    try:   
        output_file_test = open(f"{output_file}.tsv", 'x')
        output_file_test.close()

    except FileExistsError:
        print(f"The file {output_file} already exists.")
        raise FileExistsError

    return None

def filter(filtered_columns_input,column_names,column_values):
    """
    The way in which things are printed was copied from the example execution from the project01.pdf file. 
    This function portrays which column names the file contains. It first asks for the columns to exclude,
    and then the values of those columns to exclude. The values the user wishes to exclude are put into
    a list (final filter list) which is then used for the print operations and for writing the output file.
    """
    values_to_exclude = []
    individual_column_value = []
    processed_column_names = []
    final_filter_list = []

    filter_columns = [x - 1 for x in filtered_columns_input[0]]    # The user input starts at 1, list numberings start at 0 which  
    for index in filter_columns:                             # is why we subtract 1 from each entry.
        print(f"\n'{column_names[0][index]}' contains the following values:")     
        processed_column_names.append(column_names[0][index])     
        column_filter = []              
                                                                                
        for i in range(len(column_values[0][index])):
            print(f"{i+1}. {column_values[0][index][i]}")
            individual_column_value.append(column_values[0][index][i])
        
        values_input = get_unique_integers_from_user("Numbers of the values to exclude for seperated by commas: ", len(column_values[0][index]), 1)
        values_to_exclude.append(values_input[0])

        column_filter = [column_values[0][index][i - 1] for i in values_input[0]]
        final_filter_list.append(column_filter)

    return processed_column_names, final_filter_list

def write_output_file(output_file, column_names, records, output_columns_input, filters):
    """
    This function writes the tsv file with the filename output_file. First the column names are written into the output file, seperated by tab characters. Then the records are
    filtered and also written into the tsv file, seperating elements by tab and records with newline characters. 
    """

    with open(output_file, 'w') as output_tsv:
        output_columns = []                             # Since output_columns_input contain the numbers of the columns we want to exclude we
        if len(column_names) == 0 and len(records) == 0:
            output_tsv.write("")
            return
        
        for i in range(1, len(column_names[0]) + 1):    # convert that to the column we want to write into our output file
            if i in output_columns_input[0]:
                pass
            else:
                output_columns.append(i)

        for element in output_columns:  # Printing all the column names the user wanted, seperating them with tab characters
            output_tsv.write(f"{column_names[0][element-1]} \t")
        output_tsv.write("\n")

        output_records = []
        for i in range(len(records[0])):    # These nested loops remove the columns in the records that are excluded by the user
            new_record = []
            for element in output_columns:
                new_record.append(records[0][i][element-1])
            output_records.append(new_record)

        filters_list = []
        for element in filters: # This loop converts the 2D list of the filters into a 1D list
            filters_list.extend(element)

        filtered_records = []
        for record in output_records:   # Filteres the records by removing records containing the values which the user wants to exclude
            exclude_record = False
            for element in record:
                if element in filters_list:
                    exclude_record = True
                    break

            if exclude_record == False:
                filtered_records.append(record)

        if len(filtered_records) == 0:  # If there are no records after applying the filters, the function returns none, otherwise the filtered records are written to the output file
            return None
        else:
            for record in filtered_records:
                for i in range(len(record)):
                    output_tsv.write(record[i] + "\t")
                output_tsv.write("\n")
        
def print_operations(column_names, output_columns, filters):
    """
    This function prints a summary of the operations that are applied to the input file. The output columns already contain the column names that are not
    excluded in the output file, so the argument column_names here is redundant.  
    """
    print("\nProcessing", end = " ")

    if len(output_columns) == 0:
        return

    if len(output_columns) > 1:
        for i in range(len(output_columns)-2):              # This loop prints the column names in a correct
            print(f"'{output_columns[i]}',", end = " ")     # sentence, it's more for aesthetics than functionality.

        print(f"'{output_columns[-2]}' and '{output_columns[-1]}' where:")
    else:
        print(f"'{output_columns[0]}' where:")


    for i in range(len(output_columns)):
        print(f"'{output_columns[i]}' != {filters[i][0]} ", end = " ")       # Each column name that the user wants to filter for is stated including each value that is excluded. 

        if len(filters[i]) > 1:                                                          
            for element in filters[i][1:]:
                print(f"or {element}", end = " ")    # We do element - 1 because the user input started at 1 and list numbering starts at 0

            print() # Executes an empty print which automatically adds a newline character
        else:
            print() # Executes an empty print which automatically adds a newline character

if __name__ == '__main__':
    main()