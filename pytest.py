#! /bin/python3
import sys, itertools, csv, os, collections

# Asks the ueser how they what to enter the sudoku
# Returns the bool because it runs the checksudoku funktion that returns true if it was correct
# Exits the program if it was not right
def ask() -> bool:
    # Makes the global varibel in this function
    size = sudoku = gridSize = False
    
    # Asks the size of the sudoku
    try:
        size = int(input("Enter how many rows there are (default 9): "))
    except ValueError:
        size = 9
    # And the grid size
    try:
        gridSize = int(input("Enter how many rows there are in a grid(default 3): "))
    except ValueError:
        gridSize = 3

    # Asks how you want to read in the sudoku or if you are done
    while True:
        userInput = input("""To import sudoku from csv file type the path to the fil,
To mannually type in the rows type input
To exit type exit
: """)

        if userInput.lower() == "exit":
            # Returns then the while loop running the program will be broken
            return True
        elif userInput.lower() == "input":
            sudoku = inputSudoku("Enter row 1 with a space between each number:", size, sudoku=[])
            break
        elif os.path.exists(userInput) and userInput[-4:] == ".csv":
            sudoku = importFromCSV(userInput, size=size)
            if sudoku:
                break
        else:
            print("New try.......")

    # Returns False if its solved correctly
    return checkSudoku(sudoku, gridSize, size)


# Imports from csv
# YES I KNOW THAT ICLOUD run the checkrow function in here but i think the code i more clear if
# The chcking happens from the check sudoku funktion
def importFromCSV(path, size=3):
    sudoku = []
    # Opens and reads the csv file
    with open(path, newline='') as csvfile:
        rows = csv.reader(csvfile, delimiter=' ', quotechar='|')

        # Appends the rows to the sudoku array
        for row in rows:
            # Checks that all of the inputed numbers are numbers
            # Else i throws the Value error
            try:
                row = map(int, row[0].split(","))
                row = list(map(str, row))
            except ValueError:
                size = -1
            # If the isn't the correct amount of numbers in the import you will be asked how to
            # Import the data again
            if len(row) == size:
                sudoku.append(row)
            else:
                print("There is not the correct amount of colums there is only: " + str(len(row)))
                return False

        # Checks that there is the correct amount of rows
        if rows.line_num != size:
            print("There is not the correct amount of rows there is only: " + str(len(rows)))
            return False
    
    # Return the 2D array that is the sudoku
    return sudoku
            

# The function that adds the row to the sudoku array if it's the correct length
# Same thing as importFromCSV function I know I cloud run the checkrow for every row
def addToSudoku(sudoku, row, rowNumber, size) -> None:
    ending = False
    # If there is a char in the row 
    # The map function will raise an error if ther are anything else then numbers
    try:
        row = map(int, row.split(" "))
        row = list(map(str, row))
    except ValueError:
        ending = " again with only spaces between the numbers:"

    else:
        # Checks the the row is the correct size
        if len(row) == size:
            sudoku.append(row)
            rowNumber += 1
            ending = ":"
        else:
            ending = " again with the correct amount of numbers:"
    
    # Dose not return anything becouse it calls the function insted
    finally:
        message = "Enter row " + str(rowNumber) + ending
        inputSudoku(message, size, sudoku=sudoku, rowNumber=rowNumber)


# Asks that you input the same or the next row
# Sepends on if you enter the last one correctly
# Returns the sudoku when all rows are inputed
def inputSudoku(message, size, sudoku=[], rowNumber=1):
    if len(sudoku) != size:
        rowInput = input(message)
        addToSudoku(sudoku, rowInput, rowNumber, size)

    return sudoku


# Checks if the row that is a 1D array has the same number more then one time in it
def check(row, message, size):
    # The set function makes an array of the array but every number will one appere one time
    # Here are many ways to do it I did the first one becouse it's the fastest one I cloud think of
    # If we would whan't to speed it up we cloud take away the check that the number is between
    # 0 and the size of the array 

    # This is the absolute fastes way to check true the row
    numbers = collections.defaultdict(bool)
    for number in row:
        if numbers[number] or 0 > int(number) < size:
            sys.exit(message)
        else:
            numbers[number] = True

    '''
    # Alternative
    This is what I would use because it's the nices one and code should be clean and nice
    (It's not a slow but i think the code would be rund as O(N*2))

    if not len(set(row)) == size:
        sys.exit(message)


    # Allternative
    Works just like the example above just more ugly
    numbers = {}
    for number in row:
        numbers[number] = 0
    
    if not len(numbers) == size:
        sys.exit(message)
    '''
    return row


# Gose true every row, column and grid and checks and calls the check function to make the check
def checkSudoku(sudoku, grSize, size) -> bool:
    # Gose true all of the rows
    for i, row in enumerate(sudoku):
        check(row, "Row " + str(i+1) + " has same numbers", size)

    # Flipps the array so ever the array insed is now the coulmn
    flipped = list(zip(*sudoku))

    # Gose true and checks all of the colums
    for i, col in enumerate(sudoku):
        check(col, "Col " + str(i+1) + " has same numbers", size)

    grids = []
    # Makes the grids
    for i in range(0, size, grSize):
        for j in range(0, size, grSize):
            # Assuming the grid size is 3
            # It takes 3 colums and loops over each one
            # Then it take the first 3 numbers from the column and make it in to a list
            # That is stord in an array
            # The array then that is a 2D array gets pased true the itertoolschain
            # That makes it in to a 1D array that then gets added to the grids
            grid = itertools.chain.from_iterable(col[j:j+grSize] for col in flipped[i:i+grSize])
            grids.append(list(grid))

    # Checks that the grids are okej
    for grid in grids:
        check(grid, "One or more squares have the same number in it", size)

    # Returns False so you can add in a new sudoku
    return False


# Runs until there is bad sudoku or the user stops
while True:
    if ask():
        break
    else:
        print("The sudoku is correctly solved")
        print("Let's do it again")
