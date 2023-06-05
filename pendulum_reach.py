import numpy as lib_numpy
# Import sympy library
import sympy as lib_sympy
#Display
import matplotlib.pyplot as plt

#create a symbolic 2D rotation matrix (2x2)
def create_rotation_matrix_2d( theta : lib_sympy.Symbol):
    return lib_sympy.Matrix([[lib_sympy.cos(theta), -lib_sympy.sin(theta)], [lib_sympy.sin(theta), lib_sympy.cos(theta)]])

#create a symbolic 2D vector 2x1 vertical x, y
def create_vector_2d( x : lib_sympy.Symbol, y : lib_sympy.Symbol ):
    return lib_sympy.Matrix([[x, y]])

#A segment is composed by a joint connected to a link
def create_segment( in_phi : lib_sympy.Symbol, in_theta : lib_sympy.Symbol, in_length : lib_sympy.Symbol ):
    #joints
    nnn_rotation_matrix = create_rotation_matrix_2d( in_phi +in_theta )
    #link from this joint to the next joint to come
    nn_link_vector = create_vector_2d( in_length, 0 )
    #equation of the link
    return nn_link_vector *nnn_rotation_matrix

def system():
    #---------------------------------------------------
    #   WORLD - J1
    #---------------------------------------------------

    eq_link_w_1 = create_segment( 0, 0, 0 )

    #---------------------------------------------------
    #   J1 - EE
    #---------------------------------------------------

    n_theta_1 = lib_sympy.Symbol('T1')
    n_length_1_e = lib_sympy.Symbol('L1E')
    eq_link_1_e = create_segment( 0, n_theta_1, n_length_1_e )

    #---------------------------------------------------
    #   END EFFECTOR
    #---------------------------------------------------
    #spawn the output of the system (referred to world)
    n_x = lib_sympy.Symbol('x')
    n_y = lib_sympy.Symbol('y')
    nn_end_effector = create_vector_2d( n_x, n_y )

    #---------------------------------------------------
    #   EQUATION
    #---------------------------------------------------
    #build the equation
    eq = lib_sympy.Eq( nn_end_effector, eq_link_w_1 +eq_link_1_e )
    print("Equation: ", eq )

    solution_forward = lib_sympy.solve( eq, [n_x, n_y], dict = True )
    print("num solutions: ", len(solution_forward))
    print("Forward Solution theta->x,y: ", solution_forward )

    #Construct equations from solutions
    for n_solution_index in solution_forward: #loop over the solutions
        #equation from solution so I can substitute
        equation_forward_x = lib_sympy.Eq( n_x, n_solution_index[n_x] ) 
        equation_forward_y = lib_sympy.Eq( n_y, n_solution_index[n_y] ) 

    print("Equation X: ", equation_forward_x )
    print("Equation Y: ", equation_forward_y )

    #---------------------------------------------------
    #   MAP THE REACH
    #---------------------------------------------------
    #   I initialize a "result" array. it contains the X and Y output
    #   I decide the minimum and maximum angle range of the joints
    #   for each solution
    #       first I set the length of the link, a parameter
    #       I replace the angle of the joints in the equation
    #       I solve the equation, and record the result

    #I initialize a “result” array. it contains the X and Y output
    result = []
    #Angles J1
    min = -lib_numpy.pi
    max = lib_numpy.pi
    steps = 10
    n_angles = lib_numpy.linspace( min, max, steps )
    #scan angles for J1
    for angle in n_angles:
        #first I set the length of the link, a parameter
        length = 10
        #I replace the angle of the joints in the equation
        n_eval_x = equation_forward_x.evalf( subs={n_theta_1: angle, n_length_1_e: length} )
        sol_x = lib_sympy.solve(n_eval_x, dict=True)
        n_eval_y = equation_forward_y.evalf( subs={n_theta_1: angle, n_length_1_e: length} )
        sol_y = lib_sympy.solve(n_eval_y, dict=True)
        sol = [ sol_x[0][n_x], sol_y[0][n_y] ]
        #solve the now simple equation and get a number
        print("solution: ", sol )
        #I solve the equation, and record the result
        result.append( sol )

    #---------------------------------------------------
    #   PRINT XY
    #---------------------------------------------------
    #   Print a scatter XY chart showing all the X,Y points
    #---------------------------------------------------

    #Print a scatter XY chart showing all the X,Y points
    x_values = [r[0] for r in result]
    y_values = [r[1] for r in result]
    plt.scatter(x_values, y_values)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Reachable points for a single link")
    plt.show()

#if execution detected
if __name__ == '__main__':
    system()