import itertools
import json


FIELD = list(itertools.product(range(3), repeat=3))
ZERO = (0, 0, 0)
ONE = (1, 0, 0)


def add(first, second):
    return tuple((left + right) % 3 for left, right in zip(first, second))


def negate(value):
    return tuple(-entry % 3 for entry in value)


def multiply(first, second):
    coefficients = [0] * 5
    for row in range(3):
        for column in range(3):
            coefficients[row + column] += first[row] * second[column]
    for degree in [4, 3]:
        coefficients[degree - 2] += coefficients[degree]
        coefficients[degree - 3] += coefficients[degree]
    return tuple(entry % 3 for entry in coefficients[:3])


def power(value, exponent):
    result = ONE
    for index in range(exponent):
        result = multiply(result, value)
    return result


def trace(value):
    result = add(add(value, power(value, 3)), power(value, 9))
    require(result[1:] == (0, 0), 'prime-field trace')
    return result[0]


def require(condition, label):
    if not condition:
        raise ValueError(label)


def main():
    nonzero = FIELD[1:]
    require(all(power(value, 26) == ONE for value in nonzero), 'nonzero multiplicative orders')
    squares = {power(value, 2) for value in nonzero}
    nonsquares = [value for value in nonzero if value not in squares]
    require(len(squares) == len(nonsquares) == 13, 'square classes')
    maps = [(ZERO,) * 27]
    for parameter in nonsquares:
        maps.append(tuple(add(multiply(parameter, power(value, 9)), multiply(power(parameter, 3), power(value, 3))) for value in FIELD))
    for parameter in nonzero:
        image = tuple(add(multiply(power(parameter, 2), value), negate(add(multiply(power(parameter, 4), power(value, 3)), multiply(power(parameter, 10), power(value, 9))))) for value in FIELD)
        if image not in maps:
            maps.append(image)
    require(len(maps) == len(set(maps)) == 27, 'spread map cardinality')
    field_indices = {value: index for index, value in enumerate(FIELD)}
    for spread_map in maps:
        for first in FIELD:
            for second in FIELD:
                require(spread_map[field_indices[add(first, second)]] == add(spread_map[field_indices[first]], spread_map[field_indices[second]]), 'linear maps')
                require(trace(multiply(first, spread_map[field_indices[second]])) == trace(multiply(second, spread_map[field_indices[first]])), 'trace self-adjointness')
    difference_count = 0
    for first, second in itertools.combinations(maps, 2):
        require(len({add(left, negate(right)) for left, right in zip(first, second)}) == 27, 'invertible map differences')
        difference_count += 1
    minus_one = negate(ONE)
    require(minus_one in nonsquares, 'minus one is nonsquare')
    witness = tuple(add(multiply(minus_one, power(value, 9)), multiply(power(minus_one, 3), power(value, 3))) for value in FIELD)
    require(witness in maps and tuple(negate(value) for value in witness) not in maps, 'negation obstruction')
    output = {'status': 'pass', 'field': 'F_3[u]/(u^3-u-1)', 'source': 'Abdukhalikov, arXiv:1306.3478v3, Section 3.3, Corollary 3.7',
              'distinct_linear_trace_self_adjoint_maps': len(maps), 'invertible_unordered_differences': difference_count,
              'nonclosure_witness': 'T_{-1} belongs to K and -T_{-1}=T_1 does not belong to K',
              'scope': 'Exact finite verification of the classical spread formulas; phase-design conclusions follow from the written character-sum proof.'}
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
