r"""
Finite semilattices and lattices
"""
#*****************************************************************************
#       Copyright (C) 2008 Peter Jipsen <jipsen@chapman.edu>,
#                          Franco Saliola <saliola@gmail.com>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#
#    This code is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#    General Public License for more details.
#
#  The full text of the GPL is available at:
#
#                  http://www.gnu.org/licenses/
#*****************************************************************************
from sage.categories.finite_lattice_posets import FiniteLatticePosets
from sage.combinat.posets.posets import Poset, FinitePoset
from sage.combinat.posets.elements import (LatticePosetElement,
                                           MeetSemilatticeElement,
                                           JoinSemilatticeElement)

####################################################################################

def MeetSemilattice(data, *args, **options):
    r"""
    Construct a meet semi-lattice from various forms of input data.

    INPUT:

    - ``data``, ``*args``, ``**options`` -- data and options that will
      be passed down to :func:`Poset` to construct a poset that is
      also a meet semilattice.

    .. seealso:: :func:`Poset`, :func:`JoinSemilattice`, :func:`LatticePoset`

    EXAMPLES:

    Using data that defines a poset::

          sage: MeetSemilattice([[1,2],[3],[3]])
          Finite meet-semilattice containing 4 elements

          sage: MeetSemilattice([[1,2],[3],[3]], cover_relations = True)
          Finite meet-semilattice containing 4 elements

    Using a previously constructed poset::

          sage: P = Poset([[1,2],[3],[3]])
          sage: L = MeetSemilattice(P); L
          Finite meet-semilattice containing 4 elements
          sage: type(L)
          <class 'sage.combinat.posets.lattices.FiniteMeetSemilattice_with_category'>

    If the data is not a lattice, then an error is raised::

          sage: elms = [1,2,3,4,5,6,7]
          sage: rels = [[1,2],[3,4],[4,5],[2,5]]
          sage: MeetSemilattice((elms, rels))
          Traceback (most recent call last):
          ...
          ValueError: Not a meet semilattice.
    """
    if isinstance(data,FiniteMeetSemilattice) and len(args) == 0 and len(options) == 0:
        return data
    P = Poset(data, *args, **options)
    if not P.is_meet_semilattice():
        raise ValueError, "Not a meet semilattice."
    return FiniteMeetSemilattice(P)

class FiniteMeetSemilattice(FinitePoset):
    """
    .. note::
        We assume that the argument passed to MeetSemilattice is the poset
        of a meet-semilattice (i.e. a poset with greatest lower bound for
        each pair of elements).

    TESTS::

        sage: M = MeetSemilattice([[1,2],[3],[3]])
        sage: TestSuite(M).run()

    ::

        sage: P = Poset([[1,2],[3],[3]])
        sage: M = MeetSemilattice(P)
        sage: TestSuite(M).run()

    """
    Element = MeetSemilatticeElement

    def _repr_(self):
        r"""
        TESTS::
        
            sage: M = MeetSemilattice([[1,2],[3],[3]])
            sage: M._repr_()
            'Finite meet-semilattice containing 4 elements'

        ::

            sage: P = Poset([[1,2],[3],[3]])
            sage: M = MeetSemilattice(P)
            sage: M._repr_()
            'Finite meet-semilattice containing 4 elements'
        """
        return "Finite meet-semilattice containing %s elements"\
                %self._hasse_diagram.order()

    def meet(self,x,y):
        r"""
        Return the meet of two elements in the lattice.

        EXAMPLES::

            sage: D = Posets.DiamondPoset(5)
            sage: D.meet(1, 2)
            0
            sage: D.meet(1, 1)
            1
            sage: D.meet(1, 0)
            0
            sage: D.meet(1, 4)
            1

        If this method is used directly, it is not necessary to coerce
        elements into the poset. (Trac #11292)  ::

            sage: D = Posets.DiamondPoset(5)
            sage: D.meet(1, 0)
            0
            sage: D.meet(1, 4)
            1

        Test that this method also works for facade lattices::

            sage: L = LatticePoset([[1,2],[3],[3]], facade = True)
            sage: L.meet(2, 3)
            2
            sage: L.meet(1, 2)
            0

        """
        i, j = map(self._element_to_vertex,(x,y))
        return self._vertex_to_element(self._hasse_diagram._meet[i,j])

####################################################################################

def JoinSemilattice(data, *args, **options):
    r"""
    Construct a join semi-lattice from various forms of input data.

    INPUT:

    - ``data``, ``*args``, ``**options`` -- data and options that will
      be passed down to :func:`Poset` to construct a poset that is
      also a join semilattice.

    .. seealso:: :func:`Poset`, :func:`MeetSemilattice`, :func:`LatticePoset`

    EXAMPLES:

    Using data that defines a poset::

          sage: JoinSemilattice([[1,2],[3],[3]])
          Finite join-semilattice containing 4 elements

          sage: JoinSemilattice([[1,2],[3],[3]], cover_relations = True)
          Finite join-semilattice containing 4 elements

    Using a previously constructed poset::

          sage: P = Poset([[1,2],[3],[3]])
          sage: J = JoinSemilattice(P); J
          Finite join-semilattice containing 4 elements
          sage: type(J)
          <class 'sage.combinat.posets.lattices.FiniteJoinSemilattice_with_category'>

    If the data is not a lattice, then an error is raised::

          sage: elms = [1,2,3,4,5,6,7]
          sage: rels = [[1,2],[3,4],[4,5],[2,5]]
          sage: JoinSemilattice((elms, rels))
          Traceback (most recent call last):
          ...
          ValueError: Not a join semilattice.
    """
    if isinstance(data,FiniteJoinSemilattice) and len(args) == 0 and len(options) == 0:
        return data
    P = Poset(data, *args, **options)
    if not P.is_join_semilattice():
        raise ValueError, "Not a join semilattice."
    return FiniteJoinSemilattice(P)

class FiniteJoinSemilattice(FinitePoset):
    """
    We assume that the argument passed to FiniteJoinSemilattice is the
    poset of a join-semilattice (i.e. a poset with least upper bound
    for each pair of elements).

    TESTS::

        sage: J = JoinSemilattice([[1,2],[3],[3]])
        sage: TestSuite(J).run()

    ::

        sage: P = Poset([[1,2],[3],[3]])
        sage: J = JoinSemilattice(P)
        sage: TestSuite(J).run()

    """
    Element = JoinSemilatticeElement

    def _repr_(self):
        r"""
        TESTS::
        
            sage: J = JoinSemilattice([[1,2],[3],[3]])
            sage: J._repr_()
            'Finite join-semilattice containing 4 elements'

        ::

            sage: P = Poset([[1,2],[3],[3]])
            sage: J = JoinSemilattice(P)
            sage: J._repr_()
            'Finite join-semilattice containing 4 elements'
        """
        return "Finite join-semilattice containing %s elements"\
                %self._hasse_diagram.order()

    def join(self,x,y):
        r"""
        Return the join of two elements in the lattice.

        EXAMPLES::

            sage: D = Posets.DiamondPoset(5)
            sage: D.join(1, 2)
            4
            sage: D.join(1, 1)
            1
            sage: D.join(1, 4)
            4
            sage: D.join(1, 0)
            1

        If this method is used directly, it is not necessary to coerce
        elements into the poset. (Trac #11292)  ::

            sage: D = Posets.DiamondPoset(5)
            sage: D.join(1, 0)
            1
            sage: D.join(1, 4)
            4

        Test that this method also works for facade lattices::

            sage: L = LatticePoset([[1,2],[3],[3]], facade = True)
            sage: L.join(1, 0)
            1
            sage: L.join(1, 2)
            3

        """
        i, j = map(self._element_to_vertex,(x,y))
        return self._vertex_to_element(self._hasse_diagram._join[i,j])

####################################################################################

def LatticePoset(data, *args, **options):
    r"""
    Construct a lattice from various forms of input data.

    INPUT:

    - ``data``, ``*args``, ``**options`` -- data and options that will
      be passed down to :func:`Poset` to construct a poset that is
      also a lattice.

    OUTPUT:

        FiniteLatticePoset -- an instance of :class:`FiniteLatticePoset`

    .. seealso:: :class:`Posets`, :class:`FiniteLatticePosets`, :func:`JoinSemiLattice`, :func:`MeetSemiLattice`

    EXAMPLES:

    Using data that defines a poset::

        sage: LatticePoset([[1,2],[3],[3]])
        Finite lattice containing 4 elements

        sage: LatticePoset([[1,2],[3],[3]], cover_relations = True)
        Finite lattice containing 4 elements

    Using a previously constructed poset::

        sage: P = Poset([[1,2],[3],[3]])
        sage: L = LatticePoset(P); L
        Finite lattice containing 4 elements
        sage: type(L)
        <class 'sage.combinat.posets.lattices.FiniteLatticePoset_with_category'>

    If the data is not a lattice, then an error is raised::

        sage: elms = [1,2,3,4,5,6,7]
        sage: rels = [[1,2],[3,4],[4,5],[2,5]]
        sage: LatticePoset((elms, rels))
        Traceback (most recent call last):
        ...
        ValueError: Not a lattice.

    Creating a facade lattice::

        sage: L = LatticePoset([[1,2],[3],[3]], facade = True)
        sage: L.category()
        Category of facade finite lattice posets
        sage: parent(L[0])
        Integer Ring
        sage: TestSuite(L).run(skip = ['_test_an_element']) # is_parent_of is not yet implemented

    """
    if isinstance(data,FiniteLatticePoset) and len(args) == 0 and len(options) == 0:
        return data
    P = Poset(data, *args, **options)
    if not P.is_lattice():
        raise ValueError, "Not a lattice."
    return FiniteLatticePoset(P, category = FiniteLatticePosets())

class FiniteLatticePoset(FiniteMeetSemilattice, FiniteJoinSemilattice):
    """
    We assume that the argument passed to FiniteLatticePoset is the
    poset of a lattice (i.e. a poset with greatest lower bound and
    least upper bound for each pair of elements).

    TESTS::

        sage: L = LatticePoset([[1,2],[3],[3]])
        sage: TestSuite(L).run()

    ::

        sage: P = Poset([[1,2],[3],[3]])
        sage: L = LatticePoset(P)
        sage: TestSuite(L).run()

    """
    Element = LatticePosetElement

    def _repr_(self):
        r"""
        TESTS::

            sage: L = LatticePoset([[1,2],[3],[3]])
            sage: L._repr_()
            'Finite lattice containing 4 elements'

        ::

            sage: P = Poset([[1,2],[3],[3]])
            sage: L = LatticePoset(P)
            sage: L._repr_()
            'Finite lattice containing 4 elements'
        """
        return "Finite lattice containing %s elements"%self._hasse_diagram.order()

    def is_distributive(self):
        r"""
        Returns ``True`` if the lattice is distributive, and ``False``
        otherwise.

        EXAMPLES::

            sage: L = LatticePoset({0:[1,2],1:[3],2:[3]})
            sage: L.is_distributive()
            True
            sage: L = LatticePoset({0:[1,2,3],1:[4],2:[4],3:[4]})
            sage: L.is_distributive()
            False
        """
        return self._hasse_diagram.is_distributive_lattice()

    def is_complemented(self):
        r"""
        Returns ``True`` if ``self`` is a complemented lattice, and
        ``False`` otherwise.

        EXAMPLES::

            sage: L = LatticePoset({0:[1,2,3],1:[4],2:[4],3:[4]})
            sage: L.is_complemented()
            True

            sage: L = LatticePoset({0:[1,2],1:[3],2:[3],3:[4]})
            sage: L.is_complemented()
            False
        """
        return self._hasse_diagram.is_complemented_lattice()

    def complements(self):
        r"""
        Returns all elements in ``self`` that have a complement.

        A complement of ``x`` is an element ``y`` such that the meet
        of ``x`` and ``y`` is the bottom element of ``self`` and the
        join of ``x`` and ``y`` is the top element of ``self``.

        EXAMPLES::

            sage: L = LatticePoset({0:[1,2,3],1:[4],2:[4],3:[4]})
            sage: L.complements()
            [4, 3, 3, 2, 0]

            sage: L = LatticePoset({0:[1,2],1:[3],2:[3],3:[4]})
            sage: L.complements()
            [4, None, None, None, 0]
        """
        return self._hasse_diagram.complements()

####################################################################################

FiniteMeetSemilattice._dual_class = FiniteJoinSemilattice
FiniteJoinSemilattice._dual_class = FiniteMeetSemilattice
FiniteLatticePoset   ._dual_class = FiniteLatticePoset
