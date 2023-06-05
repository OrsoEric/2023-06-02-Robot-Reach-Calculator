#Double Inverse pendulum
#Joints (active)
#   J_1:    Motor
#   J_2:    Motor
#Joints (passive)
#   J_E:    Tip
#Links
#   L_W1:   connects world and J1
#   L_12:   End effector
#   L_2E:   End effector

#symbolic equation solver
import sympy as lib_sympy

#create a symbolic 2D rotation matrix (2x2)
def create_rotation_matrix_2d( theta : lib_sympy.Symbol):
    return lib_sympy.Matrix([[lib_sympy.cos(theta), -lib_sympy.sin(theta)], [lib_sympy.sin(theta), lib_sympy.cos(theta)]])

#create a symbolic 2D vector 2x1 vertical x, y
def create_vector_2d( x : lib_sympy.Symbol, y : lib_sympy.Symbol ):
    return lib_sympy.Matrix([[x, y]])

#create the equation of an inverse pendulum
def system_inverse_pendulum():

    #---------------------------------------------------
    #   LINKS
    #---------------------------------------------------
    #spawn the link W - 1
    n_offset_x = 0 #lib_sympy.Symbol('WX')
    n_offset_y = 0 #lib_sympy.Symbol('WY')
    nn_link_w_1 = create_vector_2d( n_offset_x, n_offset_y )
    #---------------------------------------------------
    #spawn the link 1 - 2
    n_length_1_2 = lib_sympy.Symbol('L12')
    nn_link_1_2 = create_vector_2d( n_length_1_2, 0 )
    #---------------------------------------------------
    #spawn the link 2 - E
    n_length_2_e = lib_sympy.Symbol('L2E')
    nn_link_2_e = create_vector_2d( n_length_2_e, 0 )

    #---------------------------------------------------
    #   JOINTS
    #---------------------------------------------------
        #JOINT 1
    #angle offset of the rotation matrix
    n_phi_1 = lib_sympy.Symbol('P1')
    #angle for the rotation matrix
    n_theta_1 = lib_sympy.Symbol('T1')
    #spawn a rotation matrix
    nnn_rotation_matrix_1 = create_rotation_matrix_2d( n_phi_1 +n_theta_1 )
    #---------------------------------------------------
        #JOINT 2
    #angle offset of the rotation matrix
    n_phi_2 = lib_sympy.Symbol('P2')
    #angle for the rotation matrix
    n_theta_2 = lib_sympy.Symbol('T2')
    #spawn a rotation matrix
    nnn_rotation_matrix_2 = create_rotation_matrix_2d( n_phi_1 +n_theta_1 +n_phi_2 +n_theta_2 )

    #---------------------------------------------------
    #   END EFFECTOR
    #---------------------------------------------------
    #spawn the output of the system (referred to world)
    n_x = lib_sympy.Symbol('x')
    n_y = lib_sympy.Symbol('y')
    nn_end_effector = create_vector_2d( n_x, n_y )

    #---------------------------------------------------
    #build the equation
    eq = lib_sympy.Eq( nn_end_effector, nn_link_w_1 +nn_link_1_2 *nnn_rotation_matrix_1 +nn_link_2_e *nnn_rotation_matrix_2 )
    print("Equation: ", eq )

    #---------------------------------------------------
    #find the forward transformation, angle->position
    eq_forward = lib_sympy.solve( eq, [n_x, n_y] )
    print("Forward Solution theta->x,y: ", eq_forward )

    #---------------------------------------------------
    #find the inverse, find the angle theta that results in the given XY coordinates
    #python just doesn't have the chops to find the inverse solution -.-
    solution = lib_sympy.solve( eq, [n_theta_1, n_theta_2], dict=True )
    print("Inverse Solution x,y->theta: ")
    print("num solutions: ", len(solution))
    for n_solution_index in solution:
        print(n_solution_index)
        #Construct equations from solutions
        #eq_inverse = lib_sympy.Eq(n_theta, n_solution_index[n_theta_1] ) 
        #evaluate inverse equation on a given point, it's stil an equation
        #n_eval = eq_inverse.evalf( subs={y:1, length:2} )
        #solve the now simple equation and get a number
        #n_theta = lib_sympy.solve(n_eval, dict=True)
        #print("eval", n_theta[0][theta] *360.0 /2 /3.14158)
    

    #---------------------------------------------------
    #What I want to do, is to find the geometry to fill an area
    #fix theta at zero, I want to find link length L and joing offset phi

    

#if execution detected
if __name__ == '__main__':
    print("Iverse Pendulum Equations: 1DOF 2D-XY")
    system_inverse_pendulum()