\* PLNE - Affectation avec contrainte sur k premiers choix *\
Minimize
 obj: 0
Subject To
 c_assign_0: x_0_5 + x_0_7 + x_0_6 = 1
 c_assign_1: x_1_6 + x_1_5 + x_1_0 = 1
 c_assign_2: x_2_4 + x_2_0 + x_2_7 = 1
 c_assign_3: x_3_6 + x_3_5 + x_3_7 = 1
 c_assign_4: x_4_1 + x_4_6 + x_4_7 = 1
 c_assign_5: x_5_0 + x_5_7 + x_5_4 = 1
 c_assign_6: x_6_5 + x_6_7 + x_6_6 = 1
 c_assign_7: x_7_7 + x_7_0 + x_7_4 = 1
 c_assign_8: x_8_5 + x_8_7 + x_8_6 = 1
 c_assign_9: x_9_2 + x_9_6 + x_9_5 = 1
 c_assign_10: x_10_6 + x_10_4 + x_10_0 = 1
 c_capacity_0: x_1_0 + x_2_0 + x_5_0 + x_7_0 + x_10_0 <= 2
 c_capacity_1: x_4_1 <= 1
 c_capacity_2: x_9_2 <= 1
 c_capacity_3:  <= 1
 c_capacity_4: x_2_4 + x_5_4 + x_7_4 + x_10_4 <= 1
 c_capacity_5: x_0_5 + x_1_5 + x_3_5 + x_6_5 + x_8_5 + x_9_5 <= 1
 c_capacity_6: x_0_6 + x_1_6 + x_3_6 + x_4_6 + x_6_6 + x_8_6 + x_9_6 + x_10_6 <= 1
 c_capacity_7: x_0_7 + x_2_7 + x_3_7 + x_4_7 + x_5_7 + x_6_7 + x_7_7 + x_8_7 <= 1
 c_capacity_8:  <= 2
Binary
 x_0_5
 x_0_7
 x_0_6
 x_1_6
 x_1_5
 x_1_0
 x_2_4
 x_2_0
 x_2_7
 x_3_6
 x_3_5
 x_3_7
 x_4_1
 x_4_6
 x_4_7
 x_5_0
 x_5_7
 x_5_4
 x_6_5
 x_6_7
 x_6_6
 x_7_7
 x_7_0
 x_7_4
 x_8_5
 x_8_7
 x_8_6
 x_9_2
 x_9_6
 x_9_5
 x_10_6
 x_10_4
 x_10_0
End
