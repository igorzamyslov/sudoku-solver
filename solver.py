from copy import deepcopy

from models import Field


class SudokuSolver:
    @staticmethod
    def solve(field: Field, with_brute_force: bool = False):
        updates_found = True
        counter = 0
        while updates_found:
            counter += 1
            updates_found = False
            for cell in field.cells:
                if cell.value is not None:
                    continue
                possible_values = field.get_possible_values(cell)
                if len(possible_values) == 1:
                    cell.value = next(iter(possible_values))
                    updates_found = True

        if field.is_valid:
            print(f"Solved in {counter} cycles:")
            field.print()
        else:
            print(f"Not solved with logic, state after {counter} cycles:")
            field.print()
            if with_brute_force:
                SudokuSolver.brute_force(field)

    @staticmethod
    def brute_force(field: Field):
        fields_to_check = [deepcopy(field)]
        counter = 0
        while fields_to_check:
            counter += 1
            current_field = fields_to_check.pop()
            for cell in current_field.cells:
                if cell.value is not None:
                    continue

                try:
                    possible_values = current_field.get_possible_values(cell)
                except AssertionError:
                    break

                for value in possible_values:
                    field_copy = deepcopy(current_field)
                    field_copy.get_cell(cell.column, cell.row).value = value
                    if field_copy.has_empty_cells:
                        fields_to_check.append(field_copy)
                    else:
                        if field_copy.is_valid:
                            print(f"Solved with brute force on {counter}'th iteration:")
                            field_copy.print()
                break


if __name__ == '__main__':
    # Medium: Solved
    field_data = [
        [0, 0, 0,  9, 0, 7,  0, 3, 0],
        [0, 0, 8,  4, 0, 3,  0, 0, 0],
        [0, 0, 7,  0, 2, 0,  0, 5, 4],

        [9, 7, 0,  3, 4, 1,  5, 8, 0],
        [5, 8, 0,  7, 0, 6,  0, 0, 2],
        [6, 3, 0,  2, 8, 5,  0, 9, 1],

        [0, 1, 5,  0, 0, 0,  0, 0, 0],
        [0, 0, 0,  6, 0, 0,  0, 2, 0],
        [0, 0, 0,  5, 7, 0,  0, 0, 0],
    ]

    # # Hard: Solved with brute force
    # field_data = [
    #     [0, 0, 8,  0, 5, 0,  0, 0, 2],
    #     [0, 2, 0,  0, 9, 0,  0, 4, 1],
    #     [0, 0, 4,  0, 3, 0,  0, 0, 9],
    #
    #     [0, 0, 0,  0, 0, 0,  0, 1, 8],
    #     [0, 0, 0,  0, 0, 0,  0, 0, 0],
    #     [5, 7, 0,  4, 0, 0,  2, 0, 0],
    #
    #     [0, 0, 0,  0, 0, 7,  0, 0, 3],
    #     [0, 0, 7,  0, 6, 0,  4, 0, 0],
    #     [0, 6, 1,  3, 0, 0,  0, 9, 0],
    # ]

    # # Extreme: Solved with brute force
    # field_data = [
    #     [0, 6, 0,  4, 0, 3,  0, 7, 0],
    #     [7, 5, 1,  0, 0, 0,  0, 0, 0],
    #     [0, 0, 0,  0, 0, 2,  0, 0, 0],
    #
    #     [0, 0, 0,  0, 0, 9,  8, 6, 0],
    #     [0, 0, 0,  0, 8, 1,  0, 0, 7],
    #     [4, 0, 0,  0, 5, 0,  0, 0, 0],
    #
    #     [0, 1, 0,  0, 0, 0,  0, 8, 0],
    #     [0, 2, 0,  0, 0, 0,  1, 0, 0],
    #     [6, 3, 0,  0, 0, 0,  5, 0, 0],
    # ]

    sudoku_field = Field.init_from_data(field_data)
    SudokuSolver.solve(sudoku_field, with_brute_force=True)
