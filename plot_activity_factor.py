import matplotlib.pyplot as plt 


x = [0, 1, 4, 5, 8, 9, 10, 11]
normal_FA_alpha = [160, 160, 144, 160, 136, 148, 164, 192]
modified_FA_alpha = [192, 208, 192, 232, 192, 196, 198, 202]


plt.plot(x, normal_FA_alpha, label="Normal")
plt.plot(x, modified_FA_alpha, label="Modified")
plt.legend()
plt.show()

