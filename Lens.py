
l1_f = 120.0 #mm
l2_f = 300.0 #mm

obj_height  = 75.0 #mm
obj_width   = 133.0 #mm

l1_x = 5.0 #mm
do_1 = l1_x
di_1 = (l1_f*do_1) / (do_1-l1_f)

mag_1 = -1.0 * di_1 / do_1

i1_height = obj_height * mag_1
i1_width = obj_width * mag_1

l2_x = 200.0 #mm

i1_x = l1_x + di_1

do_2 = l2_x - i1_x
di_2 = (l2_f*do_2) / (do_2-l2_f)

mag_2 = -1.0 * di_2 / do_2

i2_height = mag_2 * i1_height
i2_width = mag_2 * i1_width

i2_x = l2_x + di_2

print(i2_x)
