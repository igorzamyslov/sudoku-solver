from copy import deepcopy
from typing import Set

from models import Field, Cell


class SudokuSolver:
    @staticmethod
    def _get_possible_value_tier_1(field: Field, cell: Cell) -> Set[int]:
        """
        Simply intersect all the missing values of a containing
        Column, Row and Square
        """
        if cell.value is not None:
            return set()

        row_missing_values = field.get_row(cell.row).get_missing_values()
        column_missing_values = field.get_column(cell.column).get_missing_values()
        square = field.get_square_from_coordinates(cell.column, cell.row)
        square_missing_values = square.get_missing_values()
        possible_values = row_missing_values & column_missing_values & square_missing_values
        return possible_values

    @staticmethod
    def _get_possible_value_tier_2(field: Field, cell: Cell) -> Set[int]:
        """
        Using the possible values (tier 1), make further assumption on what can be excluded
        """
        if cell.value is not None:
            return set()

        # Check 1:
        # If the Tier 1 possible values in other squares only happen on the
        # same rows / columns as the passed cell: exclude the values
        cell_possible_values = SudokuSolver._get_possible_value_tier_1(field, cell)
        cell_square_column, cell_square_row = cell.square_coords

        # check horizontal squares first:
        for square in field.squares:
            if square.row != cell_square_row or square.column == cell_square_column:
                continue
            # start checking cell's possible values
            for p_value in cell_possible_values.copy():
                p_value_cells_rows = set()
                for square_cell in square.cells:
                    if p_value in SudokuSolver._get_possible_value_tier_1(field, square_cell):
                        p_value_cells_rows.add(square_cell.row)
                if len(p_value_cells_rows) == 1 and next(iter(p_value_cells_rows)) == cell.row:
                    cell_possible_values.remove(p_value)

        # check vertical squares:
        for square in field.squares:
            if square.row == cell_square_row or square.column != cell_square_column:
                continue
            # start checking cell's possible values
            for p_value in cell_possible_values.copy():
                p_value_cells_cols = set()
                for square_cell in square.cells:
                    if p_value in SudokuSolver._get_possible_value_tier_1(field, square_cell):
                        p_value_cells_cols.add(square_cell.column)
                if len(p_value_cells_cols) == 1 and next(iter(p_value_cells_cols)) == cell.column:
                    cell_possible_values.remove(p_value)

        return cell_possible_values

    @staticmethod
    def get_possible_values(field: Field, cell: Cell) -> Set[int]:
        """ Provided a Cell and a field, return possible values for it """
        if cell.value is not None:
            raise ValueError(f"Cell already has a value")

        # possible_values = SudokuSolver._get_possible_value_tier_1(field, cell)
        possible_values = SudokuSolver._get_possible_value_tier_2(field, cell)

        assert len(possible_values) > 0
        return possible_values

    @staticmethod
    def solve(field: Field, with_brute_force: bool = False):
        counter = 0
        updates_found = True
        while updates_found:
            counter += 1
            updates_found = False
            for cell in field.cells:
                if cell.value is not None:
                    continue
                possible_values = SudokuSolver.get_possible_values(field, cell)
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
                    possible_values = SudokuSolver.get_possible_values(current_field, cell)
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
                            return
                break


if __name__ == '__main__':
    # # Medium: Solved
    # field_data = [
    #     [0, 0, 0,  9, 0, 7,  0, 3, 0],
    #     [0, 0, 8,  4, 0, 3,  0, 0, 0],
    #     [0, 0, 7,  0, 2, 0,  0, 5, 4],
    #
    #     [9, 7, 0,  3, 4, 1,  5, 8, 0],
    #     [5, 8, 0,  7, 0, 6,  0, 0, 2],
    #     [6, 3, 0,  2, 8, 5,  0, 9, 1],
    #
    #     [0, 1, 5,  0, 0, 0,  0, 0, 0],
    #     [0, 0, 0,  6, 0, 0,  0, 2, 0],
    #     [0, 0, 0,  5, 7, 0,  0, 0, 0],
    # ]

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

    # Extreme: Solved with brute force
    field_data = [
        [0, 6, 0,  4, 0, 3,  0, 7, 0],
        [7, 5, 1,  0, 0, 0,  0, 0, 0],
        [0, 0, 0,  0, 0, 2,  0, 0, 0],

        [0, 0, 0,  0, 0, 9,  8, 6, 0],
        [0, 0, 0,  0, 8, 1,  0, 0, 7],
        [4, 0, 0,  0, 5, 0,  0, 0, 0],

        [0, 1, 0,  0, 0, 0,  0, 8, 0],
        [0, 2, 0,  0, 0, 0,  1, 0, 0],
        [6, 3, 0,  0, 0, 0,  5, 0, 0],
    ]

    sudoku_field = Field.init_from_data(field_data)
    SudokuSolver.solve(sudoku_field, with_brute_force=True)
