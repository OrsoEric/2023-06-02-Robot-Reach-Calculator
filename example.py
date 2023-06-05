# Import sympy library
import sympy as sp

from numbers import Real

def test_quadratic():
    # Define symbols for the equation
    x = sp.Symbol('x')
    a = sp.Symbol('a')
    b = sp.Symbol('b')
    c = sp.Symbol('c')

    # Define the equation
    eq = sp.Eq(a*x**2 + b*x + c, 0)
    print("Equation: ", eq)
    # Solve the equation for x
    sol = sp.solve(eq, x)
    return sol

# Define a test bench function that takes an angle as input and returns a 2D rotation matrix
def test_bench(angle):
    print("Test bench angle: Rotation matrix")
    # Define symbols for the angle and the matrix
    theta = sp.Symbol('theta')
    R = sp.Matrix([[sp.cos(theta), -sp.sin(theta)], [sp.sin(theta), sp.cos(theta)]])

    # Substitute the angle for theta
    R = R.subs(theta, angle)

    # Return the matrix
    return R

# Define a function that takes a length and an angle as input
def inverse_rotate_vector():
    print("Test bench angle: rotate vector")
    # Define symbols for the angle and the matrix
    theta = sp.Symbol('theta')
    matrix_rotation = sp.Matrix([[sp.cos(theta), -sp.sin(theta)], [sp.sin(theta), sp.cos(theta)]])

    # Define a 2D vector with the given length
    length = sp.Symbol('length')
    vector_position = sp.Matrix([[length, 0]])

    #define the output vector
    x = sp.Symbol('x')
    y = sp.Symbol('y')
    vector_output = sp.Matrix([[x, y]])

    eq = sp.Eq( vector_output, vector_position *matrix_rotation)
    print("Rotate by tetha a vector of length L and load it into X,Y",eq)

    #invert and extract tetha,L to get an X,Y
    solution = sp.solve( eq, theta, dict=True)
    print("Solution 0T:", solution[0][theta])
    print("Solution 1T:", solution[1][theta])

    print("num solutions: ", len(solution))
    for n_solution_index in solution:
        #Construct equations from solutions
        eq_inverse = sp.Eq(theta, n_solution_index[theta] ) 
        #evaluate inverse equation on a given point, it's stil an equation
        n_eval = eq_inverse.evalf( subs={y:1, length:2} )
        #solve the now simple equation and get a number
        n_theta = sp.solve(n_eval, dict=True)
        print("eval", n_theta[0][theta] *360.0 /2 /3.14158)

    
    #
    
    #

    #next step is to use seaborn to show the domain of the transformation



    # Return equation
    return eq


# Define the main function
def main():
    # Call the test bench function with 45 degrees as input
    result = test_bench(sp.pi/4)
    # Print the result
    print(result)
    
    inverse_rotate_vector()
    return


# Execute the main function if this file is run as a script
if __name__ == '__main__':
    main()
