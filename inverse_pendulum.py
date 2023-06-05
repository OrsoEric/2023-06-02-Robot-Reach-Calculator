#Inverse pendulum
#Joints (active)
#   J_1:    Motor
#Joints (passive)
#   J_E:    Tip
#Links
#   L_W1:   connects world and J1
#   L_1E:   End effector

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
    #spawn the link W - 1
    n_offset_x = lib_sympy.Symbol('world_x')
    n_offset_y = lib_sympy.Symbol('world_y')
    nn_link_w_1 = create_vector_2d( n_offset_x, n_offset_y )

    #---------------------------------------------------
    #spawn the link 1 - E
    n_length = lib_sympy.Symbol('length')
    nn_link_1_e = create_vector_2d( n_length, 0 )

    #---------------------------------------------------
    #angle offset of the rotation matrix
    n_phi = lib_sympy.Symbol('phi')
    #angle for the rotation matrix
    n_theta = lib_sympy.Symbol('theta')
    #spawn a rotation matrix
    nnn_rotation_matrix = create_rotation_matrix_2d( n_phi +n_theta )
    print("Rotation matrix: ", nnn_rotation_matrix )

    #---------------------------------------------------
    #spawn the output of the system (referred to world)
    n_x = lib_sympy.Symbol('x')
    n_y = lib_sympy.Symbol('y')
    nn_end_effector = create_vector_2d( n_x, n_y )

    #---------------------------------------------------
    #build the equation
    eq = lib_sympy.Eq( nn_end_effector, nn_link_w_1 +nn_link_1_e *nnn_rotation_matrix)
    print("Equation: ", eq )

    #---------------------------------------------------
    #find the forward transformation, angle->position
    eq_forward = lib_sympy.solve( eq, [n_x, n_y] )
    print("Forward Solution theta->x,y: ", eq_forward )

    #---------------------------------------------------
    #find the inverse, find the angle theta that results in the given XY coordinates
    eq_inverse = lib_sympy.solve( eq, [n_theta] )
    print("Inverse Solution x,y->theta: ", eq_inverse )

#if execution detected
if __name__ == '__main__':
    print("Iverse Pendulum Equations: 1DOF 2D-XY")
    system_inverse_pendulum()