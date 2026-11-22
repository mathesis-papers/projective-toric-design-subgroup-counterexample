import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path


def determinant(matrix):
    first, second, third = matrix
    return (
        first[0] * (second[1] * third[2] - second[2] * third[1])
        - first[1] * (second[0] * third[2] - second[2] * third[0])
        + first[2] * (second[0] * third[1] - second[1] * third[0])
    ) % 3


def quadratic(matrix, vector):
    return sum(
        vector[row] * matrix[row][column] * vector[column]
        for row in range(3)
        for column in range(3)
    ) % 3


def dot(first, second):
    return sum(left * right for left, right in zip(first, second)) % 3


def squared_norm(counts):
    first, second, third = [counts[index] for index in range(3)]
    return first**2 + second**2 + third**2 - first * second - first * third - second * third


def check(condition, name):
    if not condition:
        raise ValueError(name)


def main():
    source = Path(__file__).with_name("matrices.json")
    data = json.loads(source.read_text())
    matrices = data["matrices"]
    check(data["field_modulus"] == 3 and len(matrices) == 27, "matrix count")
    for matrix in matrices:
        check(len(matrix) == 3 and all(len(row) == 3 for row in matrix), "matrix shape")
        check(all(type(entry) is int and 0 <= entry < 3 for row in matrix for entry in row), "field entries")
        check(all(matrix[row][column] == matrix[column][row] for row in range(3) for column in range(3)), "symmetry")
    check(matrices[0] == [[0] * 3 for row in range(3)], "zero matrix")
    determinants = Counter()
    for first, second in itertools.combinations(matrices, 2):
        difference = [[(first[row][column] - second[row][column]) % 3 for column in range(3)] for row in range(3)]
        value = determinant(difference)
        check(value != 0, "invertible differences")
        determinants[value] += 1
    witness = [[(matrices[1][row][column] + matrices[3][row][column]) % 3 for column in range(3)] for row in range(3)]
    check(witness not in matrices, "nonclosure witness")
    vectors = list(itertools.product(range(3), repeat=3))
    quadratics = [[quadratic(matrix, vector) for vector in vectors] for matrix in matrices]
    linear = [[dot(parameter, vector) for vector in vectors] for parameter in vectors]
    points = {
        tuple((form[index] + character[index]) % 3 for index in range(27))
        for form in quadratics
        for character in linear
    }
    check(len(points) == 729, "distinct phase functions")
    check(all(point[0] == 0 for point in points) and (0,) * 27 in points, "anchoring and identity")
    overlap_counts = Counter()
    for first, second in itertools.combinations(range(27), 2):
        for character in linear:
            counts = Counter((quadratics[first][index] - quadratics[second][index] + character[index]) % 3 for index in range(27))
            value = squared_norm(counts)
            check(value == 27, "cross-matrix overlaps")
            overlap_counts[value] += 1
    for character in linear[1:]:
        value = squared_norm(Counter(character))
        check(value == 0, "within-matrix overlaps")
        overlap_counts[value] += 1
    coordinate_pairs = list(itertools.combinations_with_replacement(range(27), 2))
    pair_sums = {
        pair: tuple((vectors[pair[0]][index] + vectors[pair[1]][index]) % 3 for index in range(3))
        for pair in coordinate_pairs
    }
    pair_forms = {
        pair: [(form[pair[0]] + form[pair[1]]) % 3 for form in quadratics]
        for pair in coordinate_pairs
    }
    pair_histograms = Counter()
    for first in coordinate_pairs:
        for second in coordinate_pairs:
            if pair_sums[first] != pair_sums[second]:
                counts = (243, 243, 243)
            else:
                histogram = Counter((left - right) % 3 for left, right in zip(pair_forms[first], pair_forms[second]))
                counts = tuple(27 * histogram[index] for index in range(3))
            check(counts == ((729, 0, 0) if first == second else (243, 243, 243)), "second moments")
            pair_histograms["diagonal" if first == second else "off_diagonal"] += 1
    point_witness = tuple((quadratics[1][index] + quadratics[3][index]) % 3 for index in range(27))
    check(point_witness not in points, "phase nonclosure")
    result = {
        "status": "pass",
        "arithmetic": "integer arithmetic modulo 3 and exact Eisenstein norms",
        "matrix_data_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "symmetric_matrices": 27,
        "invertible_unordered_differences": sum(determinants.values()),
        "determinant_histogram": dict(sorted(determinants.items())),
        "distinct_anchored_phase_functions": len(points),
        "identity_present": True,
        "nonclosure_indices": [1, 3],
        "missing_matrix_sum": witness,
        "overlap_exponent_cases": dict(sorted(overlap_counts.items())),
        "coordinate_pair_moment_cases": dict(pair_histograms),
        "ordered_coordinate_quadruples_covered": 27**4,
        "ordered_distinct_phase_pairs_covered": 729 * 728,
        "moment_method": "For unequal coordinate sums, the 27 linear characters have residues 9,9,9; for equal sums, all 27 quadratic residues are enumerated. Coordinate-pair symmetry covers every ordered quadruple.",
        "overlap_method": "Every cross-matrix difference is enumerated for all 27 linear terms; all 26 nonzero linear differences are enumerated for equal matrices. Reversing a difference conjugates the sum.",
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
