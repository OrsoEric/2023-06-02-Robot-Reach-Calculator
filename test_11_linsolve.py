import sympy as lib_sympy

#try linsolve
def test_bench_linsolve_numeric():
    print("--------------------------------------------------------------")
    print("TEST: Numeric Matrix Linsolve")
    #parameter
    n_k = lib_sympy.symbols("k")
    #dependent variables
    n_x = lib_sympy.symbols("x")
    n_y = lib_sympy.symbols("y")
    n_z = lib_sympy.symbols("z")
    #linear system, three equations
    nnn_linear_coefficients = lib_sympy.Matrix([[n_k, 2, -1], [2, -2, 4], [2, -1, 2]])
    #constants after the equal
    nn_constants = lib_sympy.Matrix([[1], [-2], [0]])

    nn_solution=lib_sympy.linsolve( (nnn_linear_coefficients, nn_constants), [n_x,n_y,n_z] )
    print("Equation Parameters: ", nnn_linear_coefficients )
    print("Equation Constants: ", nn_constants )
    print("Solution: ", nn_solution )

    return

def test():
    
    return


def test_rotation_matrix():
    print("--------------------------------------------------------------")
    print("TEST: 2D rotation matrix")
    #polar coordinate
    n_distance = lib_sympy.symbols("d")
    n_theta = lib_sympy.symbols("t")
    #cartesian coordinates
    n_x = lib_sympy.symbols("x")
    n_y = lib_sympy.symbols("y")
    #build equations
    l_equations = [ n_distance*lib_sympy.cos( n_theta ) -n_x, n_distance*lib_sympy.sin( n_theta ) -n_y ]
    #solve
    l_solution = lib_sympy.linsolve( l_equations, [n_x,n_y] )
    print("Solution: ", l_solution )
    #inverse solution (FAIL non linear)
    #l_solution = lib_sympy.linsolve( l_equations, [n_distance,n_theta] )

    return

def test_rotation_matrix_inverse():
    print("--------------------------------------------------------------")
    print("TEST: cartesian->polar inverse 2D rotation")
    #polar coordinate
    n_distance = lib_sympy.symbols("d")
    n_theta = lib_sympy.symbols("t")
    #cartesian coordinates
    n_x = lib_sympy.symbols("x")
    n_y = lib_sympy.symbols("y")
    #build equations
    l_equations = [ n_distance*lib_sympy.cos( n_theta ) -n_x, n_distance*lib_sympy.sin( n_theta ) -n_y ]
    l_solution = lib_sympy.solve( l_equations, [n_distance,n_theta] )
    print("Solution: ", l_solution )


    return

#if execution detected
if __name__ == '__main__':
    test_bench_linsolve_numeric()
    test_rotation_matrix()
    test_rotation_matrix_inverse()