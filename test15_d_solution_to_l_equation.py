#why doesn't solve make some effort? ASk stack overflow
#Q
#I designing DIY robot arms, and I want to make a python program that given the length of the links, shows me the area reached by the arm
#I'm using sympy to make a symbolic solution, and then derive the equations and solve them
#My problem is that solve doesn't make an effort to cancel out symbols

import numpy as numpy
# Import sympy library
import sympy as sympy
#from sympy import ordered
#Display
import matplotlib.pyplot as plt

#solve is returning me a dictionary with index name of variable, and content the symbolic solution
#I want to translate back that dictionary into a list of equations for later processing

#d_solution = {EX: L1*cos(T1) + L2*cos(T1 + T2), EYdT1: L1*cos(T1) + L2*cos(T1 + T2), ETdT1: 1, EY: L1*sin(T1) + L2*sin(T1 + T2), M2X: L1*cos(T1), EXdT1: -L1*sin(T1) - L2*sin(T1 + T2), M2Y: L1*sin(T1), ET: T1 + T2, M2T: T1}

def my_solve():

    return


def seek(eqs, do, sol=[], strict=True):
    from sympy.solvers.solvers import _invert as f
    #from sympy.core.compatibility import ordered
    from sympy import Eq
    while do and eqs:
        for x in do:
            for e in eqs:
                if not isinstance(e, Eq):
                    continue
                i, d = f(e.lhs - e.rhs, x)
                if d != x:
                    continue
                break
            else:
                if strict:
                    assert None  # no eq could be solved for x
                continue
            sol.append((d, i))
            eqs.remove(e)
            break
        do.remove(x)
        if not strict:
            do.extend(i.free_symbols)
            do = list(sympy.ordered(do))
        for _ in range(len(eqs)):
            if not isinstance(eqs[_], Eq):
                continue
            # avoid dividing by zero
            ln, ld = eqs[_].lhs.as_numer_denom()
            rn, rd = eqs[_].rhs.as_numer_denom()
            eqs[_] = Eq(ln*rd, rn*ld).xreplace({x: i})
            if eqs[_] == False:
                raise ValueError('inconsistency detected')
    return sol

def focus(eqs, *syms, **kwargs):
    """Given Equality instances in ``eqs``, solve for symbols in
    ``syms`` and resolve as many of the free symbols in the solutions
    as possible. When ``evaluate=True`` a dictionary with keys being
    ``syms`` is returned, otherwise a list of identified symbols
    leading to the desired symbols is given.

    Examples
    ========
    >>> focus((Eq(a, b), Eq(b + 2, c)), a)
    {a: c - 2}
    >>> focus((Eq(a, b), Eq(b + 2, c)), a, evaluate=False)
    [(b, c - 2), (a, b)]
    """
    from sympy.solvers.solvers import _invert as f
    #from sympy.core.compatibility import ordered
    from sympy import Eq, Tuple
    x_evaluate = kwargs.get('evaluate', True)
    assert all(isinstance(i, Eq) for i in eqs)
    l_solution = []
    free = Tuple(*eqs).free_symbols
    do = set(syms) & free
    if not do:
        return l_solution
    eqs = list(eqs)
    seek(eqs, do, l_solution)
    assert not do
    for x, i in l_solution:
        do |= i.free_symbols
    do = list(sympy.ordered(do))  # make it canonical
    seek(eqs, do, l_solution, strict=False)
    if x_evaluate:
        while len(l_solution) > len(syms):
            x, s = l_solution.pop()
            for i in range(len(l_solution)):
                l_solution[i] = (l_solution[i][0], l_solution[i][1].xreplace({x: s}))
        for i in reversed(range(1, len(syms))):
            x, s = l_solution[i]
            for j in range(i):
                y, t = l_solution[j]
                l_solution[j] = y, f(y - t.xreplace({x: s}), y)[0]
    x_simplify = kwargs.get("simplify", False)
    if x_simplify:
        for i in range(len(l_solution)):
            l_solution[i] = sympy.Eq(l_solution[i][0], l_solution[i][1].simplify())
    if x_evaluate:
        #sol = dict(sol)
        l_solution = l_solution
    else:
        l_solution = list(reversed(l_solution))
    return l_solution


def create_rotation_matrix_2d( theta : sympy.Symbol):
    return sympy.Matrix([[sympy.cos(theta), sympy.sin(theta)], [-sympy.sin(theta), sympy.cos(theta)]])

def create_vector_2d( x : sympy.Symbol, y : sympy.Symbol ):
    return sympy.Matrix([[x, y]])

def create_segment( in_phi : sympy.Symbol, in_theta : sympy.Symbol, in_length : sympy.Symbol ):
    #joints
    nnn_rotation_matrix = create_rotation_matrix_2d( in_phi +in_theta )
    #link from this joint to the next joint to come
    nn_link_vector = create_vector_2d( in_length, 0 )
    #equation of the link
    return nn_link_vector *nnn_rotation_matrix

def create_segment_offset( in_start_x : sympy.Symbol, in_start_y : sympy.Symbol, in_phi : sympy.Symbol, in_theta : sympy.Symbol, in_length : sympy.Symbol ):
    nn_offset = create_vector_2d( in_start_x, in_start_y )
    nn_segment = create_segment( in_phi, in_theta, in_length )
    return nn_offset +nn_segment

def create_segment_equations( in_length : sympy.Symbol, in_start_x : sympy.Symbol, in_start_y : sympy.Symbol, in_phi : sympy.Symbol, in_theta : sympy.Symbol, in_end_x : sympy.Symbol, in_end_y : sympy.Symbol, in_end_theta : sympy.Symbol ):
    l_equation = []
    #Segment X,Y equations function of angle
    equation_1 = sympy.Eq( create_vector_2d( in_end_x, in_end_y ), create_segment_offset( in_start_x, in_start_y, in_phi, in_theta, in_length) )
    solution_1 = sympy.solve(  [equation_1], [in_end_x])
    solution_2 = sympy.solve(  [equation_1], [in_end_y])
    #Segment T angle equation function of angle
    equation_theta = sympy.Eq( in_end_theta, in_phi+in_theta )
    #compose segment equations
    l_equation.append( sympy.Eq( in_end_x, solution_1[in_end_x] ) )
    l_equation.append( sympy.Eq( in_end_y, solution_2[in_end_y] ) )
    l_equation.append( equation_theta )
    return l_equation

def double_pendulum_system():
    #forward equations
    #T1,T2->EX,EY,ET
    l_equation = []
    #Motor 1 segment from World to its joint
    n_segment_1_length = sympy.Symbol('L1')
    n_motor_1_theta = sympy.Symbol('T1')
    n_segment_1_x = sympy.Symbol('M2X')
    n_segment_1_y = sympy.Symbol('M2Y')
    n_segment_1_theta = sympy.Symbol('M2T')
    l_equation = l_equation +create_segment_equations( n_segment_1_length, 0, 0, 0, n_motor_1_theta, n_segment_1_x, n_segment_1_y, n_segment_1_theta ) 
    #Motor 2 segment from Motor 1 Joint to End Effector
    n_segment_2_length = sympy.Symbol('L2')
    n_motor_2_theta = sympy.Symbol('T2')
    n_end_effector_x = sympy.Symbol('EX')
    n_end_effector_y = sympy.Symbol('EY')
    n_end_effector_theta = sympy.Symbol('ET')
    l_equation = l_equation +create_segment_equations( n_segment_2_length, n_segment_1_x, n_segment_1_y, n_segment_1_theta, n_motor_2_theta, n_end_effector_x, n_end_effector_y, n_end_effector_theta ) 

    print( "Forward Equations: ", l_equation )

    #Forward Equation
    l_forward_solution = sympy.solve( l_equation, [n_end_effector_x, n_end_effector_y, n_end_effector_theta, n_segment_1_x, n_segment_1_y, n_segment_1_theta], exclude=(), dict = True )
    print( "Forward Solution: ", l_forward_solution )

    #Forward Sensitivity
    #Sensitivity of End Effector X in respect to variations in T1 angle
    n_end_effector_sensitivity_x_t1 = sympy.Symbol('EXdT1')
    n_end_effector_sensitivity_y_t1 = sympy.Symbol('EYdT1')
    n_end_effector_sensitivity_theta_t1 = sympy.Symbol('ETdT1')
    #evaluate=True evaluate the current equation, and if not solved, it returns zero
    #evaluate=False doesn't solve the derivative
    l_equation.append( sympy.Eq( n_end_effector_sensitivity_x_t1, sympy.Derivative(n_end_effector_x, n_motor_1_theta) ) )
    l_equation.append( sympy.Eq( n_end_effector_sensitivity_y_t1, sympy.Derivative(n_end_effector_y, n_motor_1_theta) ) )
    l_equation.append( sympy.Eq( n_end_effector_sensitivity_theta_t1, sympy.Derivative(n_end_effector_theta, n_motor_1_theta) ) )
    print("Forward Sensitivity Equations:")
    print( l_equation )

    #IDEA1: make derivative from the forward solution
    #IDEA2: find a way to solve the derivative later
    l_sensitivity = focus(l_equation, n_end_effector_x, n_end_effector_y, n_end_effector_theta, n_segment_1_x, n_segment_1_y, n_segment_1_theta, n_end_effector_sensitivity_x_t1, n_end_effector_sensitivity_y_t1, n_end_effector_sensitivity_theta_t1, simplify=True)
    print("Forward Sensitivity Solution:")
    print( l_sensitivity )
    
    return

if __name__ == '__main__':
    print("TEST12")
    print("Forward density chart")

    #STEP1: compile forward equations
    double_pendulum_system()
    #STEP2: compile forward sensitivity, how sensitive is position to T1 and T2
    #STEP3: 

