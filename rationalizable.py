def main():
    matrix = [
        [(2, 4), (2, 5)],
        [(2, 0), (7, 1)],
        [(6, 5), (1, 2)],
        [(5, 6), (3, 0)]
    ]
    p = Rational(matrix)
    p.iterative_eliminate_pure_dominated()
    print(p.get_utility())
    print(p.get_matrix())
    print(p.get_strategies())



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

    def get_matrix(self):
        return self.matrix

    def set_matrix(self):
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

    def iterative_eliminate_pure_dominated(self):
        while True:
            p1_len, p2_len = len(self.p1_utility), len(self.p2_utility)
            self.eliminate_pure_dominated(self.p1_utility, self.p2_utility)
            self.eliminate_pure_dominated(self.p2_utility, self.p1_utility)
            if p1_len == len(self.p1_utility) and p2_len == len(self.p2_utility):
                self.set_matrix()
                break

    def iterative_eliminate_mixed_dominated(self):
        while True:
            p1_len, p2_len = len(self.p1_utility), len(self.p2_utility)
            if p1_len >= 3:
                self.eliminate_mixed_dominated(self.p1_utility, self.p2_utility)
            if p2_len >= 3:
                self.eliminate_mixed_dominated(self.p2_utility, self.p1_utility)
            if p1_len == len(self.p1_utility) and p2_len == len(self.p2_utility):
                self.set_matrix()
                self.set_matrix()
                break

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

    def eliminate_mixed_dominated(self, p_utility, q_utility):
        pass
        


    

if __name__ == "__main__":
    main()