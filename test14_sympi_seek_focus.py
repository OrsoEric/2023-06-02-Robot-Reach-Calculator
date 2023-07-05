import sympy as sp
from sympy import ordered
x, y, z = sp.symbols("x y z")

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
            do = list(ordered(do))
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
    evaluate = kwargs.get('evaluate', True)
    assert all(isinstance(i, Eq) for i in eqs)
    sol = []
    free = Tuple(*eqs).free_symbols
    do = set(syms) & free
    if not do:
        return sol
    eqs = list(eqs)
    seek(eqs, do, sol)
    assert not do
    for x, i in sol:
        do |= i.free_symbols
    do = list(ordered(do))  # make it canonical
    seek(eqs, do, sol, strict=False)
    if evaluate:
        while len(sol) > len(syms):
            x, s = sol.pop()
            for i in range(len(sol)):
                sol[i] = (sol[i][0], sol[i][1].xreplace({x: s}))
        for i in reversed(range(1, len(syms))):
            x, s = sol[i]
            for j in range(i):
                y, t = sol[j]
                sol[j] = y, f(y - t.xreplace({x: s}), y)[0]
    simplify = kwargs.get("simplify", False)
    if simplify:
        for i in range(len(sol)):
            sol[i] = (sol[i][0], sol[i][1].simplify())
    if evaluate:
        sol = dict(sol)
    else:
        sol = list(reversed(sol))
    return sol

l_equation = []
l_equation.append(sp.Eq(y, z))
l_equation.append(sp.Eq(x, sp.Derivative(y**3, z)))

solution = focus(l_equation, x, y, simplify=True)
print(solution)    # {y: z, x: 3*z**2}