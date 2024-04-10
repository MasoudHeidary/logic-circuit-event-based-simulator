
"""
import matplotlib.pyplot as plt

# Data for the line chart
x_values = [1, 2, 3, 4, 5]
y_values = [2, 3, 5, 7, 11]

# Data for the bar chart
categories = ['A', 'B', 'C', 'D', 'E']
values = [20, 35, 30, 25, 40]

# Plotting the line chart
plt.figure(figsize=(8, 4))  # Optional: Adjusting figure size
plt.subplot(1, 2, 1)  # Creating a subplot for the first chart
plt.plot(x_values, y_values, marker='o', color='b')
plt.title('Line Chart')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')

# Plotting the bar chart
plt.subplot(1, 2, 2)  # Creating a subplot for the second chart
plt.bar(categories, values, color='r')
plt.title('Bar Chart')
plt.xlabel('Categories')
plt.ylabel('Values')

plt.tight_layout()  # Adjust layout to prevent overlap
plt.show()

"""

import matplotlib.pyplot as plt

x = [1,2,3,4,5]


x1 = [0,0,1,2,3,3,4,5]
y1 = [0,1,1,1,1,0,0,0]
x2 = [0,1,2,3,3,4,5]
y2 = [1,1,1,1,0,0,0]

plt.subplot(2,1,1)
plt.plot(x1, y1)
plt.subplot(2,1,2)
plt.plot(x2, y2)


plt.show()
