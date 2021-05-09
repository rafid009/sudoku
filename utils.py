def set_bit(b, i):
    return b | (1 << i)

def reset_bit(b, i):
    return b & ~(1 << i)

def test_bit(b, i):
    return (b & (1 << i)) != 0

def flip_bit(b, i):
    return b ^ (1 << i)

def flip_all(b):
    return ~b

def bits_to_string(b, limit=9):
    return [str(i + 1) for i in range(0, limit) if (b & (1 << i)) != 0]

def is_empty_bit(b):
    return b == 0

def set_all_bits(limit=9):
    b = 0
    for i in range(limit):
        b |= 1 << i
    return b

def count_set_bits(b, limit=9):
    count = 0
    for i in range(limit):
        if test_bit(b, i):
            count += 1
    return count

def get_block_index(row, col):
    return (row // 3) * 3 + col // 3