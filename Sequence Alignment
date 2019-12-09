import fileinput

def return_score(letter_one, letter_two):
    if letter_one == letter_two:
        return 3
    elif letter_one == '-' or letter_two == '-':
        return -2
    else:
        return -3

def find_alignment(sequence_one, sequence_two):
    s1_length = len(sequence_two)
    s2_length = len(sequence_one)
    max_score = 0
    score_matrix = [[0 for x in range(s1_length+1)] for y in range(s2_length+1)]
    final_alignment1 = ''
    final_alignment2 = ''
    i = s2_length
    j = s1_length
    
    for x in range(s1_length+1):
        score_matrix[0][x] = -2 * x
    
    for x in range(s2_length+1):
        score_matrix[x][0] = -2 * x
    
    for x in range(1, s2_length + 1):
        for y in range(1, s1_length + 1):
            diag = score_matrix[x-1][y-1] + return_score(sequence_one[x-1], sequence_two[y-1])
            delete = score_matrix[x-1][y] + -2
            insert = score_matrix[x][y-1] + -2
            score_matrix[x][y] = max(diag, delete, insert)

    while i > 0 and j > 0:
        current = score_matrix[i][j]
        current_up_left = score_matrix[i-1][j-1]
        current_left = score_matrix[i][j-1]
        current_up = score_matrix[i-1][j]
        

        if current == current_up_left + return_score(sequence_one[i-1], sequence_two[j-1]):
            second_letter = sequence_two[j-1]
            first_letter = sequence_one[i-1]
            i -= 1
            j -= 1
        elif current == current_up + -2:
            second_letter = '-'
            first_letter = sequence_one[i-1]
            i -= 1
        elif current == current_left + -2:
            second_letter = sequence_two[j-1]
            first_letter = '-'
            j -= 1
        final_alignment1 += first_letter
        final_alignment2 += second_letter
            

    while j > 0:
        second_letter = sequence_two[j-1]
        first_letter = '-'
        final_alignment1 += first_letter
        final_alignment2 += second_letter
        j -= 1

    while i > 0:
        second_letter = '-'
        first_letter = sequence_one[i-1]
        final_alignment1 += first_letter
        final_alignment2 += second_letter
        i -= 1
    
    seqN = len(final_alignment1)
    for i in range(seqN):
        first_letter = final_alignment1[i]
        second_letter = final_alignment2[i]
        if first_letter == second_letter:
            max_score += return_score(first_letter, second_letter)
    
        else: 
            max_score += return_score(first_letter, second_letter)
        
    print(max_score)
    print(final_alignment1[::-1])
    print(final_alignment2[::-1])

inputlist = [] # original input list
for line in fileinput.input():
    inputlist.append(line.strip())

alignment_one = inputlist[0]
alignment_two = inputlist[1]

find_alignment(alignment_one,alignment_two)
