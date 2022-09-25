def main():
    matrix = [
        [(0, 3), (0, 2), (0, 1), (0, 0), (0, -1)],
        [(1, 0), (-1, 2), (-1, 1), (-1, 0), (-1, -1)],
        [(0, 0), (0, -1), (-2, 1), (-2, 0), (-2, -1)],
        [(-1, 0), (-1, -1), (-1, -2), (-3, 0), (-3, -1)],
        [(-2, 0), (-2, -1), (-2, -2), (-2, -3), (-4, -1)]
    ]
    p = Rational(matrix)
    p.iterative_eliminate_pure_dominated()
    print(p.reconstruct_matrix())

class Rational(object):

    def __init__(self, matrix):
        self.matrix = matrix
        self.p1_stratigies = len(matrix)
        self.p2_stratigies = len(matrix[0])

        # Set p1, p2's utility
        self.p1_utility = [[] for _ in range(self.p1_stratigies)]
        self.p2_utility = [[] for _ in range(self.p2_stratigies)]
        for row in range(len(self.matrix)):
            for i in range(2 * self.p2_stratigies):
                if i % 2 == 0:
                    self.p1_utility[row].append(self.matrix[row][i // 2][i % 2])
                else:
                    self.p2_utility[i // 2].append(self.matrix[row][i // 2][i % 2])

    def get_utility(self):
        return self.p1_utility, self.p2_utility

    def get_strategies(self):
        return self.p1_stratigies, self.p2_stratigies

    # Eliminated strictly dominated pure strategy for one round
    def one_round_pure_dominated_elimination(self):
        self.eliminate_pure_dominated(self.p1_utility, self.p2_utility)
        self.eliminate_pure_dominated(self.p2_utility, self.p1_utility)
        return self.p1_utility, self.p2_utility

    # Iterative elimination
    def iterative_eliminate_pure_dominated(self):
        while True:
            p1_len, p2_len = len(self.p1_utility), len(self.p2_utility)
            self.one_round_pure_dominated_elimination()
            if p1_len == len(self.p1_utility) and p2_len == len(self.p2_utility):
                break

    # Helper function to eliminate strictly dominated pure strategies
    def eliminate_pure_dominated(self, p_utility, q_utility):

        # While one strategy for player p is eliminated, q's value should also be eliminated
        def eliminate_q(q_utility, position):
            for row in q_utility:
                row.remove(row[position])
        
        # Check if one strategy is strictly dominated by others
        def check_eliminate(i, j, len):
            remove_i, remove_j = True, True
            for k in range(len):
                if p_utility[i][k] <= p_utility[j][k]:
                    remove_j = False
                if p_utility[i][k] >= p_utility[j][k]:
                    remove_i = False
            return remove_i, remove_j

        # Permutational check to eliminate all the strictly dominated pure strategies
        for i in range(len(p_utility)):
            for j in range(i, len(p_utility)):
                if i < len(p_utility) and j < len(p_utility):
                    remove_i, remove_j = check_eliminate(i, j, len(p_utility[0]))
                    if remove_j:
                        p_utility.remove(p_utility[j])
                        eliminate_q(q_utility, j)
                    elif remove_i:
                        p_utility.remove(p_utility[i])
                        eliminate_q(q_utility, i)


    def one_round_mixed_dominated_strategy_elimination(self):
        if len(self.p1_utility) > 3:
            self.eliminate_mixed_dominated(self.p1_utility, self.p2_utility)
        if len(self.p2_utility) > 3:
            self.eliminate_mixed_dominated(self.p2_utility, self.p1_utility)
        return self.p1_utility, self.p2_utility

    def eliminate_mixed_dominated(self, p_utility, q_utility):
        pass
        


    # Reconstruct matrix after elimination
    def reconstruct_matrix(self):
        p1_utility, p2_utility = self.get_utility()
        p2_utility = list(map(list, zip(*p2_utility)))
        matrix = [[] for _ in range(len(p1_utility))]
        for row in range(len(p1_utility)):
            for col in range(len(p1_utility[0])):
                pair = p1_utility[row][col], p2_utility[row][col]
                matrix[row].append(pair)

        # Update matrix information
        self.matrix = matrix
        self.p1_stratigies = len(matrix)
        self.p2_stratigies = len(matrix[0])
        return self.matrix

if __name__ == "__main__":
    main()