from typing import Tuple, List

def input_sudoku() -> List[List[int]]:
    """Function to take input a sudoku from stdin and return
    it as a list of lists.
    Each row of sudoku is one line.
    """
    sudoku = list()
    for _ in range(9):
        row = list(map(int, input().rstrip(" ").split(" ")))
        sudoku.append(row)
    return sudoku


def print_sudoku(sudoku: List[List[int]]) -> None:
    """Helper function to print sudoku to stdout
    Each row of sudoku in one line.
    """
    for i in range(9):
        for j in range(9):
            print(sudoku[i][j], end=(""))
        print()


def get_block_num(sudoku: List[List[int]], pos: Tuple[int, int]) -> int:
    """This function takes a parameter position and returns
    the block number of the block which contains the position.
    """
    if pos[0] % 10 in range(1, 4):
        if pos[1] % 10 in range(1, 4):
            return 1
        elif pos[1] % 10 in range(4, 7):
            return 2
        else:
            return 3
    if pos[0] % 10 in range(4, 7):
        if pos[1] % 10 in range(1, 4):
            return 4
        elif pos[1] % 10 in range(4, 7):
            return 5
        else:
            return 6
    if pos[0] % 10 in range(7, 10):
        if pos[1] % 10 in range(1, 4):
            return 7
        elif pos[1] % 10 in range(4, 7):
            return 8
        else:
            return 9
    return 0


def get_position_inside_block(sudoku: List[List[int]], pos: Tuple[int, int]) -> int:
    """This function takes parameter position
    and returns the index of the position inside the corresponding block.
    """
    if pos[1] in range(1,10):
        return (pos[1]-1)%3+1


def get_block(sudoku: List[List[int]], x: int) -> List[int]:
    """This function takes an integer argument x and then
    returns the x^th block of the Sudoku. Note that block indexing is
    from 1 to 9 and not 0-8.
    """
    blocklist = []
    for i in range(len(sudoku)):
        for j in range(len(sudoku[i])):
            pos = (i+1, j+1)
            if get_block_num(sudoku, pos) == x:
                blocklist.append(sudoku[i][j])

    return blocklist


def get_row(sudoku: List[List[int]], i: int) -> List[int]:
    """This function takes an integer argument i and then returns
    the ith row. Row indexing have been shown above.
    """
    return sudoku[i-1]


def get_column(sudoku: List[List[int]], x: int) -> List[int]:
    """This function takes an integer argument i and then
    returns the ith column. Column indexing have been shown above.
    """
    collist = []
    for i in range(9):
        collist.append(sudoku[i][x-1])

    return collist


def find_first_unassigned_position(sudoku: List[List[int]]) -> Tuple[int, int]:
    """This function returns the first empty position in the Sudoku.
    If there are more than 1 position which is empty then position with lesser
    row number should be returned. If two empty positions have same row number then the position
    with less column number is to be returned. If the sudoku is completely filled then return `(-1, -1)`.
    """
    for i in range(len(sudoku)):
        for j in range(len(sudoku[i])):
            if sudoku[i][j] == 0:
                return (i+1, j+1)
                

    return (-1, -1)


def valid_list(lst: List[int]) -> bool:
    """This function takes a lists as an input and returns true if the given list is valid.
    The list will be a single block , single row or single column only.
    A valid list is defined as a list in which all non empty elements doesn't have a repeating element.
    """
    m = []
    for i in lst:
        if i != 0:
            a = lst.count(i)
            if a > 1:
                m.append(i)
    if len(m) == 0:
        return True
    else:
        return False

    return True


def valid_sudoku(sudoku: List[List[int]]) -> bool:
    """This function returns True if the whole Sudoku is valid.
    """
    for i in range(len(sudoku)):
        if valid_list(sudoku[i]) == True:
            if valid_list(get_column(sudoku, i+1)) == True:
                if valid_list(get_block(sudoku, i+1)) == True:
                    pass
                else:
                    return False
            else:
                return False
        else:
            return False

    return True


def get_candidates(sudoku: List[List[int]], pos: Tuple[int, int]) -> List[int]:
    """This function takes position as argument and returns a list of all the possible values that
    can be assigned at that position so that the sudoku remains valid at that instant.
    """
    getlist = []
    for i in range(1, len(sudoku)+1):
        if get_row(sudoku, pos[0])[pos[1]-1] == 0 and i not in get_row(sudoku, pos[0]) and i not in get_column(sudoku, pos[1]) and i not in get_block(sudoku, get_block_num(sudoku, pos)):
            getlist.append(i)

    return getlist

def make_move(sudoku: List[List[int]], pos: Tuple[int, int], num: int) -> List[List[int]]:
    """This function fill `num` at position `pos` in the sudoku and then returns
    the modified sudoku.
    """
    sudoku[pos[0]-1][pos[1]-1] = num

    return sudoku


def undo_move(sudoku: List[List[int]], pos: Tuple[int, int]):
    """This function fills `0` at position `pos` in the sudoku and then returns
    the modified sudoku. In other words, it undoes any move that you 
    did on position `pos` in the sudoku.
    """
    sudoku[pos[0]-1][pos[1]-1] = 0
    return sudoku



def sudoku_solver(sudoku: List[List[int]]) -> Tuple[bool, List[List[int]]]:
    """ This is the main Sudoku solver. This function solves the given incomplete Sudoku and returns 
    true as well as the solved sudoku if the Sudoku can be solved i.e. after filling all the empty positions the Sudoku remains valid.
    It return them in a tuple i.e. `(True, solved_sudoku)`.

    However, if the sudoku cannot be solved, it returns False and the same sudoku that given to solve i.e. `(False, original_sudoku)`
    """

    empty_pos = find_first_unassigned_position(sudoku)
    if empty_pos == (-1, -1):
        return (True, sudoku)

    row, col = empty_pos
    candidates = get_candidates(sudoku, empty_pos)

    for num in candidates:
        make_move(sudoku, empty_pos, num) #make changes to the sudoku list
        if sudoku_solver(sudoku)[0]:
            return (True, sudoku)
        undo_move(sudoku, empty_pos) #backtracking step

    return (False, sudoku)
    


if __name__ == "__main__":

    # Input the sudoku from stdin
    sudoku = input_sudoku()

    # Try to solve the sudoku
    possible, sudoku = sudoku_solver(sudoku)


    # Check if it could be solved
    if possible:
        print("Found a valid solution for the given sudoku :)")
        print_sudoku(sudoku)

    else:
        print("The given sudoku cannot be solved :(")
        print_sudoku(sudoku)

# sudoku = [[5, 3, 0, 0, 7, 0, 0, 0, 0], [6, 0, 0, 1, 9, 5, 0, 0, 0], [0, 9, 8, 0, 0, 0, 0, 6, 0], [8, 0, 0, 0, 6, 0, 0, 0, 3], [
#     4, 0, 0, 8, 0, 3, 0, 0, 1], [7, 0, 0, 0, 2, 0, 0, 0, 6], [0, 6, 0, 0, 0, 0, 2, 8, 0], [0, 0, 0, 4, 1, 9, 0, 0, 5], [0, 0, 0, 0, 8, 0, 0, 7, 9]]
# print(get_block_num(sudoku, (5,2)))
# print(get_position_inside_block(sudoku,(4,8)))
# print(get_block(sudoku, 3))
# print(get_row(sudoku,5))
# print(get_column(sudoku,2))
# print(find_first_unassigned_position(sudoku))
# print(valid_list(sudoku[4]))
# print(valid_sudoku(sudoku))
# print(get_candidates(sudoku,(5,2)))
# print(make_move(sudoku,(5,2),(get_candidates(sudoku,(5,2)))[0]))
# print(undo_move(sudoku,(5,2)))
# print(sudoku_solver(sudoku))
