def is_mutant(dna):
    """
    Detects whether the given DNA sequence belongs to a mutant or not.
    A mutant has more than one sequence of four identical letters either
    diagonally, horizontally, or vertically.

    Parameters:
    dna (list of str): A list of strings representing each row of an NxN DNA matrix.

    Returns:
    bool: True if the DNA belongs to a mutant, False otherwise.

    To use this function from another script, you can import it as follows:
    from mutant_detector import is_mutant
    """
    N = len(dna)
    mutant_sequences = 0

    #The directions are: right, down, down/right, down/left
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

    def count_sequences(i, j, delta_i, delta_j):
        """This function counts consecutive identical letters from position (i, j) in the direction specified by delta_i, delta_j.
           IMPORTANT: This function is internal for encapsulation and to avoid space contamination."""
        base = dna[i][j]
        count = 0
        while 0 <= i < N and 0 <= j < N and dna[i][j] == base:
            count += 1
            i += delta_i
            j += delta_j
            if count == 4:
                return True
        return False

    #Scan the DNA matrix in all directions for sequences of 4 identical characters
    for i in range(N):
        for j in range(N):
            #At the case, skip invalid characters
            if dna[i][j] not in {'A', 'T', 'C', 'G'}:
                continue
            #Check all four possible directions
            for delta_i, delta_j in directions:
                if (0 <= i + 3 * delta_i < N) and (0 <= j + 3 * delta_j < N) and count_sequences(i, j, delta_i, delta_j):
                    mutant_sequences += 1
                #If the code find more than one sequence, the code confirm it is a mutant
                if mutant_sequences > 1:
                    return True

    return False
