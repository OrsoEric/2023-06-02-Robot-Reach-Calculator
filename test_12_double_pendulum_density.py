#why doesn't solve make some effort? ASk stack overflow
#Q
#I designing DIY robot arms, and I want to make a python program that given the length of the links, shows me the area reached by the arm
#I'm using sympy to make a symbolic solution, and then derive the equations and solve them
#My problem is that solve doesn't make an effort to cancel out symbols

import numpy as lib_numpy
# Import sympy library
import sympy as lib_sympy
#Display
import matplotlib.pyplot as plt

def create_rotation_matrix_2d( theta : lib_sympy.Symbol):
    return lib_sympy.Matrix([[lib_sympy.cos(theta), lib_sympy.sin(theta)], [-lib_sympy.sin(theta), lib_sympy.cos(theta)]])

def create_vector_2d( x : lib_sympy.Symbol, y : lib_sympy.Symbol ):
    return lib_sympy.Matrix([[x, y]])

def create_segment( in_phi : lib_sympy.Symbol, in_theta : lib_sympy.Symbol, in_length : lib_sympy.Symbol ):
    #joints
    nnn_rotation_matrix = create_rotation_matrix_2d( in_phi +in_theta )
    #link from this joint to the next joint to come
    nn_link_vector = create_vector_2d( in_length, 0 )
    #equation of the link
    return nn_link_vector *nnn_rotation_matrix

def create_segment_offset( in_start_x : lib_sympy.Symbol, in_start_y : lib_sympy.Symbol, in_phi : lib_sympy.Symbol, in_theta : lib_sympy.Symbol, in_length : lib_sympy.Symbol ):
    nn_offset = create_vector_2d( in_start_x, in_start_y )
    nn_segment = create_segment( in_phi, in_theta, in_length )
    return nn_offset +nn_segment

def create_segment_equations( in_length : lib_sympy.Symbol, in_start_x : lib_sympy.Symbol, in_start_y : lib_sympy.Symbol, in_phi : lib_sympy.Symbol, in_theta : lib_sympy.Symbol, in_end_x : lib_sympy.Symbol, in_end_y : lib_sympy.Symbol, in_end_theta : lib_sympy.Symbol ):
    l_equation = []
    #Segment X,Y equations function of angle
    equation_1 = lib_sympy.Eq( create_vector_2d( in_end_x, in_end_y ), create_segment_offset( in_start_x, in_start_y, in_phi, in_theta, in_length) )
    solution_1 = lib_sympy.solve(  [equation_1], [in_end_x])
    solution_2 = lib_sympy.solve(  [equation_1], [in_end_y])
    #Segment T angle equation function of angle
    equation_theta = lib_sympy.Eq( in_end_theta, in_phi+in_theta )
    #compose segment equations
    l_equation.append( lib_sympy.Eq( in_end_x, solution_1[in_end_x] ) )
    l_equation.append( lib_sympy.Eq( in_end_y, solution_2[in_end_y] ) )
    l_equation.append( equation_theta )
    return l_equation

def double_pendulum_system():
    #forward equations
    #T1,T2->EX,EY,ET
    l_equation = []
    #Motor 1 segment from World to its joint
    n_segment_1_length = lib_sympy.Symbol('L1')
    n_motor_1_theta = lib_sympy.Symbol('T1')
    n_segment_1_x = lib_sympy.Symbol('M2X')
    n_segment_1_y = lib_sympy.Symbol('M2Y')
    n_segment_1_theta = lib_sympy.Symbol('M2T')
    l_equation = l_equation +create_segment_equations( n_segment_1_length, 0, 0, 0, n_motor_1_theta, n_segment_1_x, n_segment_1_y, n_segment_1_theta ) 
    #Motor 2 segment from Motor 1 Joint to End Effector
    n_segment_2_length = lib_sympy.Symbol('L2')
    n_motor_2_theta = lib_sympy.Symbol('T2')
    n_end_effector_x = lib_sympy.Symbol('EX')
    n_end_effector_y = lib_sympy.Symbol('EY')
    n_end_effector_theta = lib_sympy.Symbol('ET')
    l_equation = l_equation +create_segment_equations( n_segment_2_length, n_segment_1_x, n_segment_1_y, n_segment_1_theta, n_motor_2_theta, n_end_effector_x, n_end_effector_y, n_end_effector_theta ) 

    print( "Forward Equations: ", l_equation )

    #Forward Equation
    l_forward_solution = lib_sympy.solve( l_equation, [n_end_effector_x, n_end_effector_y, n_end_effector_theta, n_segment_1_x, n_segment_1_y, n_segment_1_theta], exclude=(), dict = True )
    print( "Forward Solution: ", l_forward_solution )

    #Forward Sensitivity
    #Sensitivity of End Effector X in respect to variations in T1 angle
    n_end_effector_sensitivity_x_t1 = lib_sympy.Symbol('EXdT1')
    n_end_effector_sensitivity_y_t1 = lib_sympy.Symbol('EYdT1')
    n_end_effector_sensitivity_theta_t1 = lib_sympy.Symbol('ETdT1')
    #evaluate=True evaluate the current equation, and if not solved, it returns zero
    #evaluate=False doesn't solve the derivative
    l_equation.append( lib_sympy.Eq( n_end_effector_sensitivity_x_t1, lib_sympy.Derivative(n_end_effector_x, n_motor_1_theta, evaluate = False) ) )
    #l_equation.append( lib_sympy.Eq( n_end_effector_sensitivity_y_t1, lib_sympy.Derivative(n_end_effector_y, n_motor_1_theta, evaluate = True) ) )
    #l_equation.append( lib_sympy.Eq( n_end_effector_sensitivity_theta_t1, lib_sympy.Derivative(n_end_effector_theta, n_motor_1_theta, evaluate = True) ) )
    print("Forward Sensitivity Equations:")
    print( l_equation )

    #IDEA1: make derivative from the forward solution
    #IDEA2: find a way to solve the derivative later
    #l_sensitivity = lib_sympy.solve( l_equation, [n_end_effector_sensitivity_x_t1, n_end_effector_sensitivity_y_t1, n_end_effector_sensitivity_theta_t1, n_end_effector_x, n_end_effector_y, n_end_effector_theta, n_segment_1_x, n_segment_1_y, n_segment_1_theta], exclude=(), dict = True )
    l_sensitivity = lib_sympy.solve( l_equation, [n_end_effector_sensitivity_x_t1, n_end_effector_x, n_end_effector_y, n_end_effector_theta, n_segment_1_x, n_segment_1_y, n_segment_1_theta], exclude=(), dict = True )
    print("Forward Sensitivity Solution:", l_sensitivity )
    
    return

if __name__ == '__main__':
    print("TEST12")
    print("Forward density chart")

    #STEP1: compile forward equations
    double_pendulum_system()
    #STEP2: compile forward sensitivity, how sensitive is position to T1 and T2
    #STEP3: 

