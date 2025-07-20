def desimal_to_binari(x):
    if x == 0:
        return "0"
    y = []
    while x > 0:
        y.insert(0,x&1)
        x = x>>1
    return "".join(str(bit) for bit in y)

def mashlim_le_shtaim(binary_str):
    inverted_bits = []
    for bit in binary_str:
        if bit == '0':
            inverted_bits.append('1')
        elif bit == '1':
            inverted_bits.append('0')
        else:
            inverted_bits.append(bit) 
            
    return "".join(inverted_bits)
        
def add_one_to_binary(binary_str):
    binary_list = list(binary_str)
    n = len(binary_list)
    carry = 1

    for i in range(n - 1, -1, -1):
        if binary_list[i] == '0':
            binary_list[i] = '1'
            carry = 0
            break
        else:
            binary_list[i] = '0'
            carry = 1
            
    if carry == 1:
        binary_list.insert(0, '1')
        
    return "".join(binary_list)
        
        
print(add_one_to_binary(mashlim_le_shtaim(desimal_to_binari(5))))