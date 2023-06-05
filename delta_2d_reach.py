#restructure the equations, I want a system, and I want to take into account of the chain angle for the links
#the output of a link, should include a vector where the link is pointing, and chain from there
#J1 = W+SEGMENT1
#JA = 

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
    #   DELTA 2D
    #---------------------------------------------------
    #   Two segments originating from two point, two lever converge on end effector
    #   W   -   J1  -   A   -   EE
    #       |               |
    #       -   J2  -   B   -

    #---------------------------------------------------
    #   WORLD - J1
    #---------------------------------------------------
    #   J1 is offset right by distance D from origin world

    n_offset = lib_sympy.Symbol('D')
    eq_link_w_1 = create_segment( lib_numpy.pi/2, 0, n_offset )

    #---------------------------------------------------
    #   J1 - A
    #---------------------------------------------------

    n_theta_1 = lib_sympy.Symbol('T1')
    n_length_1_a = lib_sympy.Symbol('L1A')
    eq_link_1_a = create_segment( 0, n_theta_1, n_length_1_a )

    #---------------------------------------------------
    #   A - EE
    #---------------------------------------------------
    #   passive link, it's not driven

    n_theta_a = lib_sympy.Symbol('TA')
    n_length_a_e = lib_sympy.Symbol('LAE')
    eq_link_a_e = create_segment( 0, n_theta_1 +n_theta_a, n_length_a_e )

    #---------------------------------------------------
    #   WORLD - J2
    #---------------------------------------------------
    #   J2 is offset left by distance D from origin world

    n_offset = lib_sympy.Symbol('D')
    eq_link_w_2 = create_segment( -lib_numpy.pi/2, 0, n_offset )

    #---------------------------------------------------
    #   J2 - B
    #---------------------------------------------------

    n_theta_2 = lib_sympy.Symbol('T2')
    n_length_2_b = lib_sympy.Symbol('L2B')
    eq_link_2_b = create_segment( 0, n_theta_2, n_length_2_b )

    #---------------------------------------------------
    #   B - EE
    #---------------------------------------------------
    #   passive link, it's not driven

    n_theta_b = lib_sympy.Symbol('TB')
    n_length_b_e = lib_sympy.Symbol('LBE')
    eq_link_b_e = create_segment( 0, n_theta_a +n_theta_b, n_length_b_e )

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
    #I have two equations driven by T1 and T2
    #Forcing them to have the same result XY is what set the value for TA and TB

    eq_w_1_a_e = lib_sympy.Eq( nn_end_effector, eq_link_w_1 +eq_link_1_a +eq_link_a_e )
    print("Equation W 1 A E: ", eq_w_1_a_e )
    eq_w_2_b_e = lib_sympy.Eq( eq_link_w_1 +eq_link_1_a +eq_link_a_e, eq_link_w_2 +eq_link_2_b +eq_link_b_e )
    print("Equation W 2 B E: ", eq_w_2_b_e )
    solution_forward = lib_sympy.solve( [eq_w_1_a_e, eq_w_2_b_e], [n_x, n_y], dict = True,)
    print("num solutions: ", len(solution_forward))
    print("Forward Solution theta->x,y: ", solution_forward )
    lib_sympy.simplify([eq_w_1_a_e, eq_w_2_b_e])

    #Construct equations from solutions
    for n_solution_index in solution_forward: #loop over the solutions
        #equation from solution so I can substitute
        equation_forward_x = lib_sympy.Eq( n_x, n_solution_index[n_x] ) 
        equation_forward_y = lib_sympy.Eq( n_y, n_solution_index[n_y] ) 

    print("Equation X: ", equation_forward_x )
    print("Equation Y: ", equation_forward_y )
    return
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
    #samples
    n_steps = 12
    #Angles J1
    min = -lib_numpy.pi/2
    max = lib_numpy.pi/2
    nn_angles_j1 = lib_numpy.linspace( min, max, n_steps )
    #Angles J2
    min = -lib_numpy.pi/2
    max = lib_numpy.pi/2
    nn_angles_j2 = lib_numpy.linspace( min, max, n_steps )
    #link length
    in_length_1_2 = 8
    in_length_2_e = 2
    #scan angles for J1
    for n_angle_j1 in nn_angles_j1:
        for n_angle_j2 in nn_angles_j2:
            #I replace the angle of the joints in the equation
            n_eval_x = equation_forward_x.evalf( subs={n_theta_1: n_angle_j1, n_theta_2 : n_angle_j2, n_length_1_2 : in_length_1_2, n_length_2_e : in_length_2_e } )
            sol_x = lib_sympy.solve( n_eval_x, dict=True )
            #print("solution X: ", sol_x )
            n_eval_y = equation_forward_y.evalf( subs={n_theta_1: n_angle_j1, n_theta_2 : n_angle_j2, n_length_1_2 : in_length_1_2, n_length_2_e : in_length_2_e } )
            sol_y = lib_sympy.solve( n_eval_y, dict=True )
            #print("solution Y: ", sol_y )
            sol = [ sol_x[0][n_x], sol_y[0][n_y] ]
            #solve the now simple equation and get a number
            #print("solution: ", sol )
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