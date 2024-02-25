import random as r
import sys

freq = []
with open("freq", 'r') as file:
    for line in file:
        freq.append(float(line))

# print("Loading dictionary...")
words = []
num_words = 0
with open("2of12inf.txt", 'r') as file:
    for line in file:
        if line[-2] != '%':
            words.append(line.rstrip())
            if len(words) == 14:
                print(words)
num_words = len(words)

width = 12
init_depth = 6
total_depth = 11

board = [[]] * total_depth
for i in range(len(board)):
    board[i] = [''] * width
    
positions = [-1] * (2 * width)
    
def get_random_letter():
    val = r.random()
    for l in range(len(freq)):
        if val < freq[l]:
            return chr(l + 97)

def init_board():
    for i in range(init_depth):
        for j in range(width):
            add_letter_to_pos(get_random_letter(), i, j)


# if i is even, possible neighbors will be
#   (i-1, j-1), (i-1, j), (i, j-1), (i, j+1), (i+1, j-1), (i+1, j)
# if i is odd, possible neighbors will be
#   (i-1, j), (i-1, j+1), (i, j-1), (i, j+1), (i+1, j), (i+1, j+1)
def get_neighbor_indices(i, j):
    neighbors = []
    w = width - 1
    d = total_depth - 1
    if ((j != 0) and (board[i][j-1] != '')):
        neighbors.append((i, j-1))   # L
    if ((j != w) and (board[i][j+1] != '')):
        neighbors.append((i, j+1))   # R
    if (i != 0):
        if (board[i-1][j] != ''):
            neighbors.append((i-1, j))  # UL if odd or UR if even
        if ((i % 2 != 0) and (j != w) and (board[i-1][j+1] != '')):
            neighbors.append((i-1, j+1)) # UR if odd
        if ((i % 2 == 0) and (j != 0) and (board[i-1][j-1] != '')):
            neighbors.append((i-1, j-1)) # UL if even
    if (i != d):
        if (board[i+1][j] != ''):
            neighbors.append((i+1, j))  # LL if odd or LR if even
        if ((i % 2 != 0) and (j != w) and (board[i+1][j+1] != '')):
            neighbors.append((i+1, j+1)) # LR if odd
        if ((i % 2 == 0) and (j != 0) and (board[i+1][j-1] != '')):
            neighbors.append((i+1, j-1)) # LL if even
    return neighbors

def get_upper_neighbor_indices(i, j):
    neighbors = []
    w = width - 1
    if (i != 0):
        neighbors.append((i-1, j))  # UL if odd or UR if even
        if ((i % 2 != 0) and (j != w)):
            neighbors.append((i-1, j+1)) # UR if odd
        elif ((i % 2 == 0) and (j != 0)):
            neighbors.append((i-1, j-1)) # UL if even
    return neighbors
    
def is_neighbor(t1, t2):
    i1 = t1[0]
    i2 = t2[0]
    j1 = t1[1]
    j2 = t2[1]
    if ((i1 == i2) and (j1 == j2)):
        return False
    if (abs(i1 - i2) > 1):
        return False
    if (abs(j1 - j2) > 1):
        return False
    if (i1 % 2 == 0):
        if (j1 == j2 + 1):
            return False
    else:
        if (j1 == j2 - 1):
            return False
    return True
    
def add_letter_to_pos(l, i, j):
    board[i][j] = l
    
def find_positions(rows):
    # -1: position is not set
    #  0: position is at depth 0
    #  d: position will not appear
    rows = [-1] * (2 * width)
    for i in range(total_depth - 1, -1, -1):
        for j in range(width):
            pos_i = j * 2 + i % 2
            if (rows[pos_i] == -1):
                # setting a position (from the bottom up):
                #   keep going up until there is a neighbor above
                if (board[i][j] != ''):
                    # print(f"Already full at {i}, {j}, position {pos_i}")
                    rows[pos_i] = total_depth
                elif (i == 0):
                    # print(f"Reached the top at {i}, {j}, position {pos_i}")
                    rows[pos_i] = 0
                else:
                    neighbors = get_upper_neighbor_indices(i, j)
                    ni1 = neighbors[0][0]
                    nj1 = neighbors[0][1]
                    if (len(neighbors) == 2):
                        ni2 = neighbors[1][0]
                        nj2 = neighbors[1][1]
                        # print(f"{i}, {j}, checking {ni1}, {nj1} and {ni2}, {nj2}")
                        if ((board[ni1][nj1] != '') or (board[ni2][nj2] != '')):
                            # print(f"Edge space found at {i}, {j}, position {pos_i}")
                            rows[pos_i] = i
                    elif (board[ni1][nj1] != ''):
                        # print(f"Middle space found at {i}, {j}, position {pos_i}")
                        rows[pos_i] = i
    # print(rows)
    return rows

def positions_open(rows):
    for val in rows:
        if (val != -1 and val != total_depth):
            return True
    return False

def print_board():
    for i in range(total_depth):
        if (i % 2):
            print(" ", end='')
        for j in range(width):
            print (board[i][j].upper() + " ", end='')
        print()

def print_options_board(rows):
    elim_cols = [False] * (width * 2)
    rows = find_positions(rows)
    # option_rows = [total_depth] * (width * 2)
    print("0       10        20")
    for i in range(total_depth):
        if (i % 2):
            print(" ", end='')
        for j in range(width):
            elim_i = j * 2 + (i % 2)
            if (board[i][j] != ''):
                print (board[i][j].upper() + " ", end='')
            elif (rows[elim_i] == i):
                print ("\u001b[31m" + str((elim_i + 1) % 10) + "\u001b[0m ", end='')
            else:
                print ("  ", end='')
        print()
    return rows

# How to determine what the biggest word is, starting from a given position?
# Some letters can be part of multiple paths
# We can discard paths if they do not prefix an existing word
# We note down words that can be formed, where words[i] = search_word_prefix(seq, last_index)
# If none of the neighbors can form a prefix, we remove the 

# determines if word starts with prefix
def can_form_prefix(prefix, word):
    prefix_length = len(prefix)
    return (word[:prefix_length] == prefix)
    
# gives the index of the first word that starts with the sequence 
def search_word_prefix(sequence, index=0):
    # uses a binary search
    lower = index
    upper = num_words - 1
    i = int((lower + upper) / 2)
    found_i = -1
    while (lower <= i and i <= upper):
        if (sequence == words[i]):
            found_i = i
            break
        elif can_form_prefix(sequence, words[i]):
            found_i = i
            upper = i - 1
        elif sequence < words[i]:
            upper = i - 1
        else:
            lower = i + 1
        i = int((lower + upper) / 2)
    return found_i
    
def chain_into_prefix(a):
    prefix = ''
    for letter in a:
        prefix = prefix + board[letter[0]][letter[1]]
    return prefix
    
def select_possibility(all_sequences):
    length = len(all_sequences) 
    if length == 0:
        return []
    elif length == 1:
        return all_sequences[0]
    else:
        print(all_sequences)
        return all_sequences[0]
    
def find_new_word_from(start_i, start_j):
    chains = [[(start_i,start_j)]]
    found = []
    prefix = chain_into_prefix(chains[0])
    search_index = search_word_prefix(prefix)
    while (len(chains) > 0):
        new_chains = []
        # found new word possibilities for each chain
        for current_chain in chains:
            last = current_chain[-1]
            immediate = get_neighbor_indices(last[0], last[1])
            # for each neighbor, check if this neighbor is not in the current chain,
            #   then if it can form a new prefix
            #   and then, if it can form a new word, add the chain to found
            for neighbor in immediate:
                if current_chain.count(neighbor) == 0:
                    new_chain = current_chain.copy()
                    new_chain.append(neighbor)
                    prefix = chain_into_prefix(new_chain)
                    print("searching...", prefix)
                    search_index = search_word_prefix(prefix)
                    if (search_index != -1):
                        print(prefix, "starts a word, index", search_index)
                        new_chains.append(new_chain)
                        if (words[search_index] == prefix and len(prefix) >= 3):
                            print(words[search_index], "is a word")
                            if (len(found) > 0):
                                found = [new_chain]
                            else:
                                found.append(new_chain)
        # once every chain is searched, reset chains
        chains = new_chains
    # out of the loop, found list now contains all the longest possibilities
    chosen = select_possibility(found)
    if (chosen):
        print(chain_into_prefix(chosen).upper())
    for letter in chosen:
        i = letter[0]
        j = letter[1]
        board[i][j] = ''

def input_letter(rows):
    pos = None
    letter = get_random_letter()
    print("    - - > " + letter.upper())
    while True:
        try:
            pos = int(input("Where to add this letter? ")) - 1
            if (pos == -1):
                sys.exit()
            if (rows[pos] > -1 and rows[pos] < total_depth):
                break
        except Exception:
            pass
        print("Invalid input")
    i = rows[pos]
    j = int(pos / 2)
    add_letter_to_pos(letter, i, j)
    find_new_word_from(i, j)

init_board()
positions = print_options_board(positions)
while(positions_open(positions)):
    input_letter(positions)
    positions = print_options_board(positions)
print("YOU WIN!")
# print(num_words)
# prefices = ["radix", "prestidigit", "xacara", "dog", "cata"]
# for prefix in prefices:
    # index = search_word_prefix(prefix)
    # print(prefix, index, words[index])
    
# print(chain_into_prefix([ (1,1), (2,2), (3,2), (3,3), (3,4), (2,5), (1,5) ]))


print([(0,1), (1,1), (2,1)].count((1,1)))
