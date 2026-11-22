import itertools
import json
from fractions import Fraction


def require(condition, label):
    if not condition:
        raise ValueError(label)


def cyclotomic36_remainder(coefficients):
    result = list(coefficients)
    for degree in range(len(result) - 1, 11, -1):
        coefficient = result[degree]
        result[degree] = 0
        result[degree - 6] += coefficient
        result[degree - 12] -= coefficient
    return result[:12]


def translated_design(modulus, coordinates, translation):
    dimension = len(coordinates)
    pairs = list(itertools.combinations_with_replacement(range(dimension), 2))
    sums = [(coordinates[first] + coordinates[second]) % modulus for first, second in pairs]
    require(len(set(sums)) == len(pairs), 'distinct unordered coordinate sums')
    points = {
        tuple((Fraction(parameter * coordinate, modulus) + offset) % 1 for coordinate, offset in zip(coordinates, translation))
        for parameter in range(modulus)
    }
    require(len(points) == modulus, 'distinct translated points')
    require(all(point[0] == 0 for point in points), 'anchored points')
    require((Fraction(0),) * dimension not in points, 'identity absent')
    require(any(tuple((first[index] + second[index]) % 1 for index in range(dimension)) not in points for first in points for second in points), 'nonclosure')
    for first in pairs:
        for second in pairs:
            frequency = (coordinates[first[0]] + coordinates[first[1]] - coordinates[second[0]] - coordinates[second[1]]) % modulus
            require((frequency == 0) == (first == second), 'moment frequency')
    return {'dimension': dimension, 'cardinality': len(points), 'coordinates': coordinates, 'cyclic_modulus': modulus,
            'translation_in_turns': [str(value) for value in translation], 'unordered_coordinate_pair_sums': sorted(sums),
            'ordered_coordinate_quadruples_covered': dimension**4, 'identity_present': False, 'nonclosure': True}


def main():
    coordinates = [0, 1, 3, 8, 23, 27]
    dimension_six = translated_design(36, coordinates, [Fraction(0), Fraction(1, 72), *[Fraction(0)] * 4])
    overlap_polynomial = [0] * 36
    for first in coordinates:
        for second in coordinates:
            overlap_polynomial[(first - second) % 36] += 1
    remainder = cyclotomic36_remainder(overlap_polynomial)
    require(remainder != [0] * 12 and remainder != [6] + [0] * 11, 'overlap violates zero-or-six condition')
    dimension_six['overlap_at_parameter_difference_one'] = {'cyclotomic_polynomial': 'x^12-x^6+1', 'squared_norm_remainder_coefficients_ascending': remainder, 'belongs_to_zero_or_six': False}
    minimal = translated_design(3, [0, 1], [Fraction(0), Fraction(1, 6)])
    require(minimal['cardinality'] == 2 * (2 - 1) + 1, 'minimal cardinality')
    result = {'status': 'pass', 'arithmetic': 'exact rational turns, modular coordinate sums and integer polynomial remainders',
              'dimension_six': dimension_six, 'minimal_dimension_two': minimal,
              'scope': 'Finite premises for the translation corollaries; the all-dimension translation argument is a written proof.'}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
