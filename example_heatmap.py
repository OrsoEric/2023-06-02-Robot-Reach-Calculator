# Import sympy library
import sympy as sp
import numpy as np

# Import seaborn and matplotlib libraries
import seaborn as sns
import matplotlib.pyplot as plt

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
    #Construct equations from solutions
    for n_solution_index in solution: #loop over the solutions
        eq_inverse = sp.Eq(theta, n_solution_index[theta] ) 


    #create a nested for loop over x,y over range 0 to 1 step 0.1 in subs
    data = [] #create an empty list to store the angles
    for x in range(0, 10): #loop over x from 0 to 1 with step 0.1
        row = [] #create an empty list to store the angles for each row
        for n_y in range(0, 10): #loop over y from 0 to 1 with step 0.1
            angles = [] #create an empty list to store the angles for each x,y pair
            #evaluate inverse equation on a given point, it's stil an equation
            n_eval = eq_inverse.evalf( subs={y:n_y/10.0, length:2} ) #divide y by 10 to get the decimal value
            #solve the now simple equation and get a number
            n_theta = sp.solve(n_eval, dict=True)
            angles.append(n_theta[0][theta] *360.0 /2 /3.14158) #convert radians to degrees and append to angles list
            row.append(angles) #append the angles list to the row list
        data.append(row) #append the row list to the data list

    data = np.reshape(data, (10, 10) )
    data = data.astype(float)
    print("Shape:", data)
    #create a heatmap of the angles
    plt.figure(figsize=(10,10)) #adjust size
    sns.heatmap(data, cmap="RdYlGn", annot=True) #choose color map and annotate values
    plt.title("Heatmap of the angles for x,y pairs") #add title
    plt.xlabel("x") #add x label
    plt.ylabel("y") #add y label
    plt.show() #show plot

#call the function
inverse_rotate_vector()
