import sympy as lib_sympy

def test_dsolve():
    t = lib_sympy.symbols('t')
    x, y = lib_sympy.symbols('x, y', cls=lib_sympy.Function)
    l_equation = []
    l_equation.append( lib_sympy.Eq(lib_sympy.Derivative(x(t),t), 12*t*x(t) + 8*y(t)) )
    l_equation.append( lib_sympy.Eq(lib_sympy.Derivative(y(t),t), 21*x(t) + 7*t*y(t)) )
    solution = lib_sympy.dsolve(l_equation)
    print( "Solution: ", solution )

def test_geometry_dsolve():
    n_time = lib_sympy.symbols('t')
    #symbols are my inputs, the angles
    n_theta_1 = lib_sympy.symbols('T1', cls=lib_sympy.Function )
    #n_theta_2 = lib_sympy.symbols('T2', cls=lib_sympy.Function )
    #output is a function, in this case velocity of X positionof end effector
    n_position = lib_sympy.symbols('EX_VEL', cls=lib_sympy.Function )
    n_speed = lib_sympy.symbols('EX_VEL', cls=lib_sympy.Function )
    #System of Equations
    l_equation = []
    l_equation.append( lib_sympy.Eq( n_position(n_time), lib_sympy.cos(n_theta_1(n_time)) ) )
    l_equation.append( lib_sympy.Eq( n_speed(n_time), lib_sympy.Derivative( n_position(n_time), n_time ) ) )
    print( "equations", l_equation )
    solution = lib_sympy.dsolve( l_equation )
    print("Solution", solution )

if __name__ == '__main__':
    #test_dsolve()
    test_geometry_dsolve()

    
