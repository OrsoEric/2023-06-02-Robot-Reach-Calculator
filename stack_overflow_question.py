#Try to solve X^2=Y+ReplaceMe for X with ReplaceMe=0
import sympy as lib_sympy

#
def good( in_x : lib_sympy.Symbol, in_y : lib_sympy.Symbol, in_z : lib_sympy.Symbol ):
    equation = lib_sympy.Eq( in_x*in_x, in_y+ in_z )
    equation = equation.evalf( subs={in_z: -1} )
    solution = lib_sympy.solve( equation, in_x )
    return solution

#The solver doesn't realize that Z=0 and doesn't sobstitute
def bad( in_x : lib_sympy.Symbol, in_y : lib_sympy.Symbol, in_z : lib_sympy.Symbol ):
    l_equation = []
    l_equation.append( lib_sympy.Eq( in_z, -1 ) )
    l_equation.append( lib_sympy.Eq( in_x*in_x, in_y+ in_z ) )
    solution = lib_sympy.solve( l_equation, (in_x,), exclude = (in_z,) )
    return solution

#The solver doesn't realize that Z=0 and doesn't sobstitute
def bad_fixed( in_x : lib_sympy.Symbol, in_y : lib_sympy.Symbol, in_z : lib_sympy.Symbol ):
    l_equation = []
    l_equation.append( lib_sympy.Eq( in_z, -1 ) )
    l_equation.append( lib_sympy.Eq( in_x*in_x, in_y+ in_z ) )
    solution = lib_sympy.solve( l_equation, (in_x,in_z,), exclude = () )
    return solution

def bad_derivative_wrong( in_x : lib_sympy.Symbol, in_y : lib_sympy.Symbol, in_z : lib_sympy.Symbol ):
    l_equation = []
    l_equation.append( lib_sympy.Eq( in_y, in_z ) )
    l_equation.append( lib_sympy.Eq( in_x, lib_sympy.Derivative(in_y*in_y*in_y, in_z, evaluate = True) ) )
    solution = lib_sympy.solve( l_equation, (in_x,in_y,), exclude = () )
    return solution

def bad_derivative_unhelpful( in_x : lib_sympy.Symbol, in_y : lib_sympy.Symbol, in_z : lib_sympy.Symbol ):
    l_equation = []
    l_equation.append( lib_sympy.Eq( in_y, in_z ) )
    l_equation.append( lib_sympy.Eq( in_x, lib_sympy.Derivative(in_y*in_y*in_y, in_z, evaluate = True) ) )
    solution = lib_sympy.solve( l_equation, (in_x,in_y,), exclude = () )
    return solution

#
def good_derivative( in_x : lib_sympy.Symbol, in_y : lib_sympy.Symbol, in_z : lib_sympy.Symbol ):
    l_equation = []
    l_equation.append( lib_sympy.Eq( in_y, in_z ) )
    l_equation.append( lib_sympy.Eq( in_x, lib_sympy.Derivative(in_z*in_z*in_z, in_z, evaluate = True) ) )
    solution = lib_sympy.solve( l_equation, (in_x,in_y,), exclude = () )
    return solution

#
if __name__ == '__main__':
    n_x = lib_sympy.Symbol('X')
    n_y = lib_sympy.Symbol('Y')
    n_z = lib_sympy.Symbol('ReplaceMe')
    print("Manual Solution: ", good( n_x, n_y, n_z ) )
    print("Unhelpful Solution: ", bad( n_x, n_y, n_z ) )
    print("Fixed Solution: ", bad_fixed( n_x, n_y, n_z ) )
    print("Wrong Derivative: ", bad_derivative( n_x, n_y, n_z ) )
    print("Good Derivative: ", good_derivative( n_x, n_y, n_z ) )