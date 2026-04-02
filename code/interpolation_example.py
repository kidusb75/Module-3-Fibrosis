import numpy as np
import matplotlib.pyplot as plt

"""LINEAR INTERPOLATION"""

# Known points
x_points = [1, 3]
y_points = [1, 3]

x1, x2 = 1, 3
y1, y2 = 1, 3

# Make the Z and Y matrices
Z = np.array([[1, x1], [1, x2]])

Y = np.array([y1, y2])

# Compute the A matrix and print it
A = np.linalg.solve(Z, Y) # -- matrix inversion to solve for A.
# syntax fror the function is np.linalg.solve(Z, Y) where Z is the matrix of coefficients and Y is the vector of constants. The function returns the solution vector A, which contains the coefficients of the linear equation that fits the known points. Linear Algebra application!

print("A = ", A)

# # Compute one specific point (x=2)
a1, a2 = A # unpack the A matrix into its components a1 and a2, which are the coefficients of the linear equation. The value x = 2 is the point at which we want to find the corresponding y value using the linear equation defined by a1 and a2. The formula used is y = a1 + a2 * x, where x is the input value (in this case, 2) and y is the output value that we want to calculate. By substituting x = 2 into the equation, we can compute the corresponding y value based on the coefficients a1 and a2 obtained from solving the linear system.
x_value = 2 # the x value at which we want to interpolate a point. In this case, we are interested in finding the corresponding y value when x is equal to 2.
y_value = a1 + a2 * x_value
print("At x = 2, y =", y_value)

# # Plot the line
x = np.linspace(0, 5, 100)
y = a1 + a2 * x 
plt.plot(x, y)

# # Plot known points (as blue circles)
plt.scatter(x_points, y_points, color='blue', s=60, label='Known Points')

# # Plot the interpolated point (in red)
plt.scatter(x_value, y_value, color='red', zorder=5, label=f'Interpolated Point (x={x_value}, y={y_value:.2f})')

# # Add labels and grid
plt.title('Line with Interpolated Point (red)')
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True)
plt.legend()
plt.show()

"""QUADRATIC INTERPOLATION"""

# Known points
x_points = [1, 3, 5]
y_points = [1, 3, 2]

x1, x2, x3 = 1, 3, 5
y1, y2, y3 = 1, 3, 2

Z = np.array([[1, x1, x1 ** 2],  # recall that ** is exponentiation in Python, so x1 ** 2 is x1 squared.)
              [1, x2, x2 ** 2], 
              [1, x3, x3 ** 2]])

Y = np.array([y1, y2, y3])

A = np.linalg.solve(Z, Y)

print("A = ", A)

a1, a2, a3 = A # unpack the A matrix into its components a1, a2, and a3, which are the coefficients of the quadratic equation. The value x = 4 is the point at which we want to find the corresponding y value using the quadratic equation defined by a1, a2, and a3. The formula used is y = a1 + a2 * x + a3 * x^2, where x is the input value (in this case, 4) and y is the output value that we want to calculate. By substituting x = 4 into the equation, we can compute the corresponding y value based on the coefficients a1, a2, and a3 obtained from solving the quadratic system.


# A "Coefficients": (calculated above)
a1, a2, a3 = -1.125, 2.5, -0.375

# Define x values (for the full parabola)
x = np.linspace(-10, 10, 400)
# y = a1 + a2 * x + a3 * x**2


# Plot known points (as blue circles)
plt.scatter(x_points, y_points, color='blue', s=60, label='Known Points')

# Compute one specific point (x=4)
x_value = 4 # the x value at which we want to interpolate a point. In this case, we are interested in finding the corresponding y value when x is equal to 4.
y_value = a1 + a2 * x_value + a3 * x_value**2 # the formula used is y = a1 + a2 * x + a3 * x^2, where x is the input value (in this case, 4) and y is the output value that we want to calculate. By substituting x = 4 into the equation, we can compute the corresponding y value based on the coefficients a1, a2, and a3 obtained from solving the quadratic system.
print("At x = 4, y =", y_value)

# Plot the parabola
plt.plot(x, y, label='y = -1.125 + 2.5x -0.375x²')

# Plot the specific point (in red)
plt.scatter(x_value, y_value, color='red', zorder=5, label=f'Interpolated Point (x={x_value}, y={y_value:.2f})')

# Add labels and grid
plt.title('Parabola with Interpolated Point (red)')
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True)
plt.legend()
plt.show()