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

def create_segment_equations( in_end_x : lib_sympy.Symbol, in_end_y : lib_sympy.Symbol, in_start_x : lib_sympy.Symbol, in_start_y : lib_sympy.Symbol, in_phi : lib_sympy.Symbol, in_theta : lib_sympy.Symbol, in_length : lib_sympy.Symbol ):
    l_equation = []
    equation_1 = lib_sympy.Eq( create_vector_2d( in_end_x, in_end_y ), create_segment_offset( in_start_x, in_start_y, in_phi, in_theta, in_length) )
    solution_1 = lib_sympy.solve(  [equation_1], [in_end_x])
    solution_2 = lib_sympy.solve(  [equation_1], [in_end_y])
    l_equation.append( lib_sympy.Eq( in_end_x, solution_1[in_end_x] ) )
    l_equation.append( lib_sympy.Eq( in_end_y, solution_2[in_end_y] ) )
    return l_equation

def system():
    #World
    #0,0
    #world is pointing with X up, motors are on the sides of the X axis
    #Spawn equations for Motor 1 and Motor 2 position referred to world
    n_interaxis_motor = lib_sympy.Symbol('D12')
    n_phase_1 = lib_sympy.pi/2
    n_phase_2 = -lib_sympy.pi/2
    
    l_equations = []
    #Motor 1 fixture
    n_motor_1_x = lib_sympy.Symbol('M1X')
    n_motor_1_y = lib_sympy.Symbol('M1Y')
    l_equations = l_equations +create_segment_equations( n_motor_1_x, n_motor_1_y, 0, 0, n_phase_1, 0, n_interaxis_motor/2 ) 
    #motor 2 fixture
    n_motor_2_x = lib_sympy.Symbol('M2X')
    n_motor_2_y = lib_sympy.Symbol('M2Y')
    l_equations = l_equations +create_segment_equations( n_motor_2_x, n_motor_2_y, 0, 0, n_phase_2, 0, n_interaxis_motor/2 )
    #Segment 3 moved by Motor 1
    n_joint_3_x = lib_sympy.Symbol('J3X')
    n_joint_3_y = lib_sympy.Symbol('J3Y')
    
    n_joint_1_theta = lib_sympy.Symbol('T1')
    n_link_1_3 = lib_sympy.Symbol('L13')
    l_equations = l_equations +create_segment_equations( n_joint_3_x, n_joint_3_y, n_motor_1_x, n_motor_1_y, 0, n_joint_1_theta, n_link_1_3 )

    print(l_equations)
    #lib_sympy.simplify( l_equations,n_joint_3_x )
    #solution = lib_sympy.solve( l_equations, [n_joint_3_x, n_joint_3_y],exclude=[n_motor_1_x], dict =True )
    solution = lib_sympy.linsolve( l_equations, [n_joint_3_x, n_joint_3_y] )
    print("Solution", solution)

    s_wolfram = lib_sympy.mathematica_code( l_equations )
    print("Wolfram", s_wolfram )

    return

#if execution detected
if __name__ == '__main__':
    system()