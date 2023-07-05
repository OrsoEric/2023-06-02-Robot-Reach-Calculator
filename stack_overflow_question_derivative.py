#Try to solve Y=Z X=dY(Z)^3/dZ
import sympy as lib_sympy

#I'm trying to build a generic symbolic mechanical link solver using sympy
#I have trouble making it solve partial differential equations
#How do I put partial derivatives operators like dY(Z)/dz that the solver is happy to solve

def bad_derivative_wrong( in_x : lib_sympy.Symbol, in_y : lib_sympy.Symbol, in_z : lib_sympy.Symbol ):
    l_equation = []
    l_equation.append( lib_sympy.Eq( in_y, in_z ) )
    l_equation.append( lib_sympy.Eq( in_x, lib_sympy.Derivative( in_y*in_y*in_y, in_z, evaluate = True ) ) )
    solution = lib_sympy.solve( l_equation, (in_x,in_y,), exclude = () )
    return solution

def bad_derivative_unhelpful( in_x : lib_sympy.Symbol, in_y : lib_sympy.Symbol, in_z : lib_sympy.Symbol ):
    l_equation = []
    l_equation.append( lib_sympy.Eq( in_y, in_z ) )
    l_equation.append( lib_sympy.Eq( in_x, lib_sympy.Derivative( in_y*in_y*in_y, in_z, evaluate = False ) ) )
    solution = lib_sympy.solve( l_equation, (in_x,in_y,), exclude = () )
    return solution

def good_derivative( in_x : lib_sympy.Symbol, in_y : lib_sympy.Symbol, in_z : lib_sympy.Symbol ):
    l_equation = []
    l_equation.append( lib_sympy.Eq( in_y, in_z ) )
    l_equation.append( lib_sympy.Eq( in_x, lib_sympy.Derivative( in_z*in_z*in_z, in_z, evaluate = True ) ) )
    #what happens here is that Derivative has already solved the derivative, it's not a symbol
    solution = lib_sympy.solve( l_equation, (in_x,in_y,), exclude = () )
    #lib_sympy.dsolve
    return solution

#Creates a system of two equations
# 1) Y=Z
# 2) X=dY(Z)^3/dZ
# solve the system of partial differential equation for X and Y
def derivative_function( in_x : lib_sympy.Symbol, in_y : lib_sympy.Symbol, in_z : lib_sympy.Symbol ):
    # Define the variables
    Y = lib_sympy.Function('Y')(in_z)
    Z = lib_sympy.Function('Z')(in_z)
    solution = []
    # Define the equations
    eq1 = lib_sympy.Eq(Y, in_z)
    eq2 = lib_sympy.Eq(in_x, lib_sympy.diff(Y**3, in_z))

    # Solve the system of equations
    #solution = lib_sympy.dsolve((eq1, eq2), funcs=[Y, Z])
    
    return solution

if __name__ == '__main__':
    #n_x = lib_sympy.symbols('X', cls=lib_sympy.Function)
    n_x = lib_sympy.symbols('X')
    n_y = lib_sympy.Symbol('Y')
    n_z = lib_sympy.Symbol('Z')
    print("Derivative Solution: ", derivative_function(n_x, n_y, n_z))

    #print("Wrong Derivative: ", bad_derivative_wrong( n_x, n_y, n_z ) )
    #print("Unhelpful Derivative: ", bad_derivative_unhelpful( n_x, n_y, n_z ) )
    #print("Good Derivative: ", good_derivative( n_x, n_y, n_z ) )

    
