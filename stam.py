milim_nefotzot = ["12345678", "admin", "password", "11111111"]
x = "12345678S"
milim_nefotzot_t_o_f = False
for i in range(len(milim_nefotzot)):
    if x in milim_nefotzot[i]:
        milim_nefotzot_t_o_f = True
    break
print(milim_nefotzot_t_o_f)