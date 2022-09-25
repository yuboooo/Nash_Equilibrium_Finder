import Nash_Equilibrium_Finder.rationalizable as r

def test_get_utility():
    matrix = [
        [(2, 4), (1, 1), (2, 5)],
        [(1, 3), (1, 2), (3, 1)],
        [(0, 5), (6, 3), (4, 6)]
    ]
    p = r.Rational(matrix)
    assert p.get_utility() == (
        [[2, 1, 2], [1, 1, 3], [0, 6, 4]], 
        [[4, 3, 5], [1, 2, 3], [5, 1, 6]]
    )

    matrix = [
        [(2, 4), (1, 1)],
        [(1, 3), (1, 2)],
        [(0, 5), (6, 3)]
    ]
    p = r.Rational(matrix)
    assert p.get_utility() == (
        [[2, 1], [1, 1], [0, 6]], 
        [[4, 3, 5], [1, 2, 3]]
    )

def test_rational_pure_strategies():
    matrix = [
        [(2, 4), (1, 1)],
        [(1, 3), (1, 2)],
        [(0, 5), (6, 3)]
    ]
    p = r.Rational(matrix)
    p.iterative_eliminate_dominated_pure()
    assert p.get_utility() == ([[2]], [[4]])

    matrix = [
        [(2, 4), (1, 1), (2, 3)],
        [(1, 3), (1, 2), (1, 7)],
        [(0, 5), (6, 3), (4, 2)]
    ]
    p = r.Rational(matrix)
    p.iterative_eliminate_dominated_pure()
    assert p.get_utility() == ([[2]], [[4]])

def test_reconstruction_matrix():
    matrix = [
        [(0, 3), (0, 2), (0, 1), (0, 0), (0, -1)],
        [(1, 0), (-1, 2), (-1, 1), (-1, 0), (-1, -1)],
        [(0, 0), (0, -1), (-2, 1), (-2, 0), (-2, -1)],
        [(-1, 0), (-1, -1), (-1, -2), (-3, 0), (-3, -1)],
        [(-2, 0), (-2, -1), (-2, -2), (-2, -3), (-4, -1)]
    ]
    p = r.Rational(matrix)
    p.iterative_eliminate_dominated_pure()
    assert p.reconstruct_matrix() == [
        [(0, 3), (0, 2), (0, 1)], 
        [(1, 0), (-1, 2), (-1, 1)], 
        [(0, 0), (0, -1), (-2, 1)]
    ]
    matrix = [
        [(2, 4), (1, 1), (2, 3)],
        [(1, 3), (1, 2), (1, 7)],
        [(0, 5), (6, 3), (4, 2)]
    ]
    p = r.Rational(matrix)
    p.iterative_eliminate_dominated_pure()
    assert p.reconstruct_matrix() == [[(2, 4)]]