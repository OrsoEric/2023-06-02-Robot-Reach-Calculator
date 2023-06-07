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
def create_rotation_matrix_2d( in_theta : lib_sympy.Symbol ):
    return lib_sympy.Matrix([[lib_sympy.cos(in_theta), -lib_sympy.sin(in_theta)], [lib_sympy.sin(in_theta), lib_sympy.cos(in_theta)]])

#create a symbolic 2D vector 2x1 vertical x, y
def create_vector_2d( in_x : lib_sympy.Symbol, in_y : lib_sympy.Symbol ):
    return lib_sympy.Matrix([[in_x, in_y]])

def create_vector_xyr( in_x : lib_sympy.Symbol, in_y : lib_sympy.Symbol, in_theta : lib_sympy.Symbol ):
    return lib_sympy.Matrix([[in_x, in_y, in_theta]])


#A segment is composed by a joint connected to a link
def create_segment( in_phi : lib_sympy.Symbol, in_theta : lib_sympy.Symbol, in_length : lib_sympy.Symbol ):
    #joints
    nnn_rotation_matrix = create_rotation_matrix_2d( in_phi +in_theta )
    #link from this joint to the next joint to come
    nn_link_vector = create_vector_2d( in_length, 0 )
    #equation of the link
    return nn_link_vector *nnn_rotation_matrix

#A segment is composed by a joint connected to a link
def create_segment_xyr( in_phi : lib_sympy.Symbol, in_theta : lib_sympy.Symbol, in_length : lib_sympy.Symbol ):
    #joints
    nnn_rotation_matrix = create_rotation_matrix_2d( in_phi +in_theta )
    #link from this joint to the next joint to come
    nn_link_vector = create_vector_xyr( in_length, 0, in_phi +in_theta )
    #equation of the link
    return nn_link_vector *nnn_rotation_matrix


#create the equation of an inverse pendulum
def system_inverse_pendulum():
    #---------------------------------------------------
    #spawn the link W - 1
    n_offset_x = lib_sympy.Symbol('WX')
    n_offset_y = lib_sympy.Symbol('WY')
    nn_link_w_1 = create_vector_2d( n_offset_x, n_offset_y )

    #---------------------------------------------------
    #spawn the link 1 - E
    n_length = lib_sympy.Symbol('L1E')
    nn_link_1_e = create_vector_2d( n_length, 0 )

    #---------------------------------------------------
    #angle offset of the rotation matrix
    n_phi = lib_sympy.Symbol('P1')
    #angle for the rotation matrix
    n_theta = lib_sympy.Symbol('T1')
    #spawn a rotation matrix
    nnn_rotation_matrix = create_rotation_matrix_2d( n_phi +n_theta )
    print("Rotation matrix: ", nnn_rotation_matrix )

    #---------------------------------------------------
    #spawn the output of the system (referred to world)
    n_end_effector_x = lib_sympy.Symbol('EX')
    n_end_effector_y = lib_sympy.Symbol('EY')
    n_end_effector_theta = lib_sympy.Symbol('ET')
    nn_end_effector = create_vector_2d( n_end_effector_x, n_end_effector_y, n_end_effector_theta )

    #---------------------------------------------------
    #build the equation
    eq = lib_sympy.Eq( nn_end_effector, nn_link_w_1 +nn_link_1_e *nnn_rotation_matrix)
    print("Equation: ", eq )

    #---------------------------------------------------
    #find the forward transformation, angle->position
    eq_forward = lib_sympy.solve( eq, [n_end_effector_x, n_end_effector_y, n_end_effector_theta] )
    print("Forward Solution theta->x,y: ", eq_forward )

    #---------------------------------------------------
    #find the inverse, find the angle theta that results in the given XY coordinates
    eq_inverse = lib_sympy.solve( eq, [n_theta] )
    print("Inverse Solution x,y->theta: ", eq_inverse )

    return

def system_v2():
    #parameters
    n_length = lib_sympy.Symbol('L1E')
    n_phi = lib_sympy.Symbol('P1')
    #inputs
    n_theta = lib_sympy.Symbol('T1')
    #outputs
    n_x = lib_sympy.Symbol('EX')
    n_y = lib_sympy.Symbol('EY')
    n_theta = lib_sympy.Symbol('ET')
    #
    eq = lib_sympy.Eq( n_x, )

    #introduce equations
    eq_1_e = create_segment( n_phi, n_theta, n_length )

    return

#if execution detected
if __name__ == '__main__':
    print("Iverse Pendulum Equations: 1DOF 2D-XY")
    system_inverse_pendulum()