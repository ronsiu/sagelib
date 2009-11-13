###############################################################################
#   Sage: Open Source Mathematical Software
#       Copyright (C) 2009 Burcin Erocal <burcin@erocal.org>
#  Distributed under the terms of the GNU General Public License (GPL),
#  version 2 or any later version.  The full text of the GPL is available at:
#                  http://www.gnu.org/licenses/
###############################################################################


from sage.symbolic.function import SymbolicFunction, sfunctions_funcs, \
        unpickle_wrapper

def function_factory(name, nargs=0, latex_name=None, conversions=None,
            eval_func=None, evalf_func=None,
            conjugate_func=None, real_part_func=None, imag_part_func=None,
            derivative_func=None, power_func=None, series_func=None,
            print_func=None, print_latex_func=None):
    """
    Create a formal symbolic function. For an explanation of the arguments see
    the documentation for the method :method:`function`.

    EXAMPLES::

        sage: from sage.symbolic.function_factory import function_factory
        sage: f = function_factory('f', 2, '\\foo', {'mathematica':'Foo'})
        sage: f(2,4)
        f(2, 4)
        sage: latex(f(1,2))
        \foo\left(1, 2\right)
        sage: f._mathematica_init_()
        'Foo'

        sage: def evalf_f(self, x, parent=None): return x*.5r
        sage: g = function_factory('g',1,evalf_func=evalf_f)
        sage: g(2)
        g(2)
        sage: g(2).n()
        1.00000000000000
    """
    class NewSymbolicFunction(SymbolicFunction):
        def __init__(self):
            """
            EXAMPLES::

                sage: from sage.symbolic.function_factory import function_factory
                sage: f = function_factory('f', 2) # indirect doctest
                sage: f(2,4)
                f(2, 4)
            """
            SymbolicFunction.__init__(self, name, nargs, latex_name,
                    conversions)

        def _maxima_init_(self):
            """
            EXAMPLES::

                sage: from sage.symbolic.function_factory import function_factory
                sage: f = function_factory('f', 2) # indirect doctest
                sage: f._maxima_init_()
                "'f"
            """
            return "'%s"%self.name()

        def __reduce__(self):
            """
            EXAMPLES::

                sage: from sage.symbolic.function_factory import function_factory
                sage: f = function_factory('f', 2) # indirect doctest
                sage: nf = loads(dumps(f))
                sage: nf(1, 2)
                f(1, 2)
            """
            pickled_functions = self.__getstate__()[5]
            return (unpickle_function, (name, nargs, latex_name, conversions,
                pickled_functions))

    l = locals()
    for func_name in sfunctions_funcs:
        func = l.get(func_name+"_func", None)
        if func:
            if not callable(func):
                raise ValueError, func_name + "_func" + " parameter must be callable"
            setattr(NewSymbolicFunction, '_%s_'%func_name, func)

    return NewSymbolicFunction()

def unpickle_function(name, nargs, latex_name, conversions, pickled_funcs):
    """
    This is returned by the ``__reduce__`` method of symbolic functions to be
    called during unpickling to recreate the given function.

    It calls :method:`function_factory` with the supplied arguments.

    EXAMPLES::

        sage: from sage.symbolic.function_factory import unpickle_function
        sage: nf = unpickle_function('f', 2, '\\foo', {'mathematica':'Foo'}, [])
        sage: nf
        f
        sage: nf(1,2)
        f(1, 2)
        sage: latex(nf(x,x))
        \foo\left(x, x\right)
        sage: nf._mathematica_init_()
        'Foo'

        sage: from sage.symbolic.function import pickle_wrapper
        sage: def evalf_f(self, x, parent=None): return 2r*x + 5r
        sage: def conjugate_f(self, x): return x/2r
        sage: nf = unpickle_function('g', 1, None, None, [None, pickle_wrapper(evalf_f), pickle_wrapper(conjugate_f)] + [None]*7)
        sage: nf
        g
        sage: nf(2)
        g(2)
        sage: nf(2).n()
        9.00000000000000
        sage: nf(2).conjugate()
        1
    """
    funcs = map(unpickle_wrapper, pickled_funcs)
    args = [name, nargs, latex_name, conversions] + funcs
    return function_factory(*args)

def function(s, *args, **kwds):
    """
    Create a formal symbolic function with the name *s*.

    INPUT:

    - ``args`` - arguments to the function, if specified returns the new
      function evaluated at the given arguments
    - ``nargs=0`` - number of arguments the function accepts, defaults to
      variable number of arguments, or 0
    - ``latex_name`` - name used when printing in latex mode
    - ``conversions`` - a dictionary specifying names of this function in
      other systems, this is used by the interfaces internally during conversion
    - ``eval_func`` - method used for automatic evaluation
    - ``evalf_func`` - method used for numeric evaluation
    - ``conjugate_func`` - method used for complex conjugation
    - ``real_part_func`` - method used when taking real parts
    - ``imag_part_func`` - method used when taking imaginary parts
    - ``derivative_func`` - method to be used for derivation
      This method should take a keyword argument deriv_param specifying
      the index of the argument to differentiate w.r.t 
    - ``power_func`` - method used when taking powers
      This method should take a keyword argument power_param specifying
      the exponent
    - ``series_func`` - method used for series expansion 
      This method should expect keyword arguments
      - ``order`` - order for the expansion to be computed
      - ``var`` - variable to expand w.r.t.
      - ``at`` - expand at this value
    - ``print_func`` - method for custom printing
    - ``print_latex_func`` - method for custom printing in latex mode

    Note that custom methods must be instance methods, i.e., expect the instance
    of the symbolic function as the first argument.
    
    EXAMPLES::
    
        sage: var('a, b')
        (a, b)
        sage: f = function('cr', a)
        sage: g = f.diff(a).integral(b)
        sage: g
        b*D[0](cr)(a)
        sage: foo = function("foo", nargs=2)
        sage: x,y,z = var("x y z")
        sage: foo(x, y) + foo(y, z)^2
        foo(y, z)^2 + foo(x, y)

    In Sage 4.0, you need to use :meth:`substitute_function` to
    replace all occurrences of a function with another::

        sage: g.substitute_function(cr, cos)
        -b*sin(a)

        sage: g.substitute_function(cr, (sin(x) + cos(x)).function(x))
        -(sin(a) - cos(a))*b

    In Sage 4.0, basic arithmetic with unevaluated functions is no
    longer supported::
    
        sage: x = var('x')
        sage: f = function('f')
        sage: 2*f
        Traceback (most recent call last):
        ...
        TypeError: unsupported operand parent(s) for '*': 'Integer Ring' and '<class 'sage.symbolic.function_factory.NewSymbolicFunction'>'

    You now need to evaluate the function in order to do the arithmetic::

        sage: 2*f(x)
        2*f(x)


    We create a formal function of one variable, write down
    an expression that involves first and second derivatives,
    and extract off coefficients.

    ::

        sage: r, kappa = var('r,kappa')
        sage: psi = function('psi', nargs=1)(r); psi
        psi(r)
        sage: g = 1/r^2*(2*r*psi.derivative(r,1) + r^2*psi.derivative(r,2)); g
        (r^2*D[0, 0](psi)(r) + 2*r*D[0](psi)(r))/r^2
        sage: g.expand()
        2*D[0](psi)(r)/r + D[0, 0](psi)(r)
        sage: g.coeff(psi.derivative(r,2))
        1
        sage: g.coeff(psi.derivative(r,1))
        2/r

    Defining custom methods for automatic or numeric evaluation, derivation,
    conjugation, etc. is supported::


        sage: def ev(self, x): return 2*x
        sage: foo = function("foo", nargs=1, eval_func=ev)
        sage: foo(x)
        2*x
        sage: foo = function("foo", nargs=1, eval_func=lambda self, x: 5)
        sage: foo(x)
        5
        sage: def ef(self, x): pass
        sage: bar = function("bar", nargs=1, eval_func=ef)
        sage: bar(x)
        bar(x)

        sage: def evalf_f(self, x, parent=None): return 6
        sage: foo = function("foo", nargs=1, evalf_func=evalf_f)
        sage: foo(x)
        foo(x)
        sage: foo(x).n()
        6

        sage: foo = function("foo", nargs=1, conjugate_func=ev)
        sage: foo(x).conjugate()
        2*x

        sage: def deriv(self, *args,**kwds): print args, kwds; return args[kwds['diff_param']]^2
        sage: foo = function("foo", nargs=2, derivative_func=deriv)
        sage: foo(x,y).derivative(y)
        (x, y) {'diff_param': 1}
        y^2

        sage: def pow(self, x, power_param=None): print x, power_param; return x*power_param
        sage: foo = function("foo", nargs=1, power_func=pow)
        sage: foo(y)^(x+y)
        y x + y
        (x + y)*y

        sage: def expand(self, *args, **kwds): print args, kwds; return sum(args[0]^i for i in range(kwds['order']))
        sage: foo = function("foo", nargs=1, series_func=expand)
        sage: foo(y).series(y, 5)
        (y,) {'var': y, 'options': 0, 'at': 0, 'order': 5}
        y^4 + y^3 + y^2 + y + 1

        sage: def my_print(self, *args): return "my args are: " + ', '.join(map(repr, args))
        sage: foo = function('t', nargs=2, print_func=my_print)
        sage: foo(x,y^z)
        my args are: x, y^z

        sage: latex(foo(x,y^z))
        t\left(x, y^{z}\right)
        sage: foo = function('t', nargs=2, print_latex_func=my_print)
        sage: foo(x,y^z)
        t(x, y^z)
        sage: latex(foo(x,y^z))
        my args are: x, y^z
        sage: foo = function('t', nargs=2, latex_name='foo')
        sage: latex(foo(x,y^z))
        foo\left(x, y^{z}\right)
    """
    if not isinstance(s, (str, unicode)):
        raise TypeError, "expect string as first argument"

    # create the function
    if ',' in s:
        names = s.split(',')
    elif ' ' in s:
        names = s.split(' ')
    else:
        names = [s]

    funcs = [function_factory(name, **kwds) for name in names]

    if len(args) > 0:
        res = [f(*args) for f in funcs]
    else:
        res = funcs

    if len(res) == 1:
        return res[0]
    return tuple(res)

def deprecated_custom_evalf_wrapper(func):
    """
    This is used while pickling old symbolic functions that define a custom
    evalf method. 
    
    The protocol for numeric evaluation functions was changed to include a
    ``parent`` argument instead of ``prec``. This function creates a wrapper
    around the old custom method, which extracts the precision information
    from the given ``parent``, and passes it on to the old function.

    EXAMPLES::
        
        sage: from sage.symbolic.function_factory import deprecated_custom_evalf_wrapper as dcew
        sage: def old_func(x, prec=0): print "x: %s, prec: %s"%(x,prec)
        sage: new_func = dcew(old_func)
        sage: new_func(5, parent=RR)
        x: 5, prec: 53
        sage: new_func(0r, parent=ComplexField(100))
        x: 0, prec: 100
    """
    def new_evalf(*args, **kwds):
        parent = kwds['parent']
        if parent:
            prec = parent.prec()
        else:
            prec = 53
        return func(*args, prec=prec)
    return new_evalf
