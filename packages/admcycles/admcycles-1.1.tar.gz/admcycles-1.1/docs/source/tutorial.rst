.. linkall

.. _tutorial:

******************
admcycles Tutorial
******************

Below we show how to use ``admcycles`` for computations in the tautological ring of the moduli space :math:`\overline{\mathcal{M}}_{g,n}` of stable curves. More detailed explanations are available in the preprint [Delecroix-Schmitt-vanZelm]_.

To use ``admcycles``, the first thing you need to do is import it::

    sage: from admcycles import *

Then many functions become available. For example you can enter tautological
classes as combinations of divisors (here on
:math:`\overline{\mathcal{M}}_{3,4}`)::

    sage: t1 = 3*sepbdiv(1,(1,2),3,4)-psiclass(4,3,4)^2

Above, the function ``sepbdiv(g1,A1,g,n)`` returns the class of a boundary
divisor, the pushforward of the fundamental class under the gluing map
:math:`\overline{\mathcal{M}}_{g_1, A_1 \cup \{\bullet\}} \times
\overline{\mathcal{M}}_{g-g_1, A_1^c \cup \{\bullet\}} \to
\overline{\mathcal{M}}_{g, n}`, and ``psiclass(i,g,n)`` returns :math:`\psi_i`
on :math:`\overline{\mathcal{M}}_{g,n}`. To avoid having to type g,n  in long
formulas, we can use ``reset_g_n(g,n)`` to set them once::

    sage: reset_g_n(2,1)
    sage: t2 = -1/3*irrbdiv()*lambdaclass(1)

To get explanations about a function such as ``irrbdiv``, you can type the name
of the function followed by a question mark::

    sage: irrbdiv?  # not tested

Tautological classes
====================

Creating tautological classes
-----------------------------

One way to enter a tautological class is to first use the function
``list_tautgens(g,n,r)`` to print a list of generators of
:math:`\mathrm{RH}^{2r}(\overline{\mathcal{M}}_{g,n})`::

    sage: list_tautgens(2,0,2) #generators of R^2(\Mbar_{2,0})
    [0] : Graph :      [2] [[]] []
    Polynomial : 1*(kappa_2^1 )_0
    [1] : Graph :      [2] [[]] []
    Polynomial : 1*(kappa_1^2 )_0
    [2] : Graph :      [1, 1] [[2], [3]] [(2, 3)]
    Polynomial : 1*(kappa_1^1 )_0
    [3] : Graph :      [1, 1] [[2], [3]] [(2, 3)]
    Polynomial : 1*psi_2^1
    [4] : Graph :      [1] [[2, 3]] [(2, 3)]
    Polynomial : 1*(kappa_1^1 )_0
    [5] : Graph :      [1] [[2, 3]] [(2, 3)]
    Polynomial : 1*psi_2^1
    [6] : Graph :      [0, 1] [[3, 4, 5], [6]] [(3, 4), (5, 6)]
    Polynomial : 1*
    [7] : Graph :      [0] [[3, 4, 5, 6]] [(3, 4), (5, 6)]
    Polynomial : 1*

Generators are given by a stable graph, decorated with a monomial in
:math:`\kappa` and :math:`\psi`-classes (see below for an explanation of the
representation of stable graphs). One can create a list ``L`` of the generators
we printed above using ``tautgens(g,n,r)`` and compute linear combinations of
the elements ``L[i]`` of this list::

    sage: L = tautgens(2,0,2)
    sage: t3=2*L[3]+L[4]
    sage: t3
    Graph :      [1, 1] [[2], [3]] [(2, 3)]
    Polynomial : 2*psi_2^1
    <BLANKLINE>
    Graph :      [1] [[2, 3]] [(2, 3)]
    Polynomial : 1*(kappa_1^1 )_0

Stable graphs are represented by three lists:

* a list ``genera`` of the genera :math:`g_i` of the vertices,
* a list ``legs`` of lists of legs and half-edges at these vertices,
* a list ``edges`` of pairs ``(h1,h2)`` of half-edges forming an edge.

A stable graph can be created manually using ``StableGraph(genera,legs,edges)``
by specifying these three lists. Below we create a stable graph with two
vertices of genus 1, carrying half-edges 2,3 which form an edge::

    sage: G = StableGraph([1,1],[[2],[3]],[(2,3)]); G
    [1, 1] [[2], [3]] [(2, 3)]

Basic operations
----------------

Tautological classes can be manipulated using standard arithmetic operations::

    sage: s1 = psiclass(3,1,3)^2 # square of psi_3 on \Mbar_{1,3}

They can also be pushed forward under forgetful morphisms, by specifying the
list of markings that are forgotten. As an example, we push forward ``s_1``,
the class :math:`\psi_3^2` on :math:`\overline{\mathcal{M}}_{1,3}`, under the
map forgetting marking :math:`3`, obtaining the class :math:`\kappa_1` on
:math:`\overline{\mathcal{M}}_{1,2}` as expected::

    sage: s1.forgetful_pushforward([3])
    Graph :      [1] [[1, 2]] []
    Polynomial : 1*(kappa_1^1 )_0

Similarly, we can pull back the class :math:`\psi_2` on :math:`\overline{\mathcal{M}}_{1,2}`::

    sage: s2 = psiclass(2,1,2)
    sage: s2.forgetful_pullback([3])
    Graph :      [1] [[1, 2, 3]] []
    Polynomial : 1*psi_2^1
    <BLANKLINE>
    Graph :      [1, 0] [[1, 4], [2, 3, 5]] [(4, 5)]
    Polynomial : (-1)*

Given a tautological class ``t``, the function ``t.evaluate()`` computes the
integral of ``t`` against the fundamental class of
:math:`\overline{\mathcal{M}}_{g,n}`, i.e. the degree of the zero-cycle part of
``t``. Below we compute the intersection number
:math:`\int_{\overline{\mathcal{M}}_{1,3}} \psi_2 \psi_3^2` We check the
equality

.. math::

    \int_{\overline{\mathcal{M}}_{1,3}} \psi_2 \psi_3^2 = \int_{\overline{\mathcal{M}}_{1,2}} \psi_2^2 + \psi_1 \psi_2

predicted by the String equation::

    sage: s3 = psiclass(2,1,3)*psiclass(3,1,3)^2
    sage: s3.evaluate()
    1/12

    sage: s4 = psiclass(2,1,2)^2+psiclass(1,1,2)*psiclass(2,1,2)
    sage: s4.evaluate()
    1/12

Using ``simplify()`` to reduce number of terms in tautclass::

    sage: psisum = psiclass(1,2,1) + 3 * psiclass(1,2,1); psisum
    Graph :      [2] [[1]] []
    Polynomial : 1*psi_1^1
    <BLANKLINE>
    Graph :      [2] [[1]] []
    Polynomial : 3*psi_1^1
    sage: psisimple = psisum.simplify(); psisimple
    Graph :      [2] [[1]] []
    Polynomial : 4*psi_1^1

A basis of the tautological ring and tautological relations
-----------------------------------------------------------

The package can compute the generalized Faber-Zagier relations between the
generators above. The function ``generating_indices(g,n,r)`` computes a list of
indices of ``tautgens(g,n,r)`` forming a basis of
:math:`\mathrm{RH}^{2r}(\overline{\mathcal{M}}_{g,n})`::

    sage: generating_indices(2,0,2)
    [0, 1]

Then, the function ``toTautbasis(g,n,r)`` can be used to express a tautological class in this basis::

    sage: t3.toTautbasis(2,0,2)
    (-48, 22)

This means that the class ``t3`` we defined above as the linear combination
``t3=2*L[3]+L[4]`` can be expressed as ``t3=-48*L[0]+22*L[1]`` in terms of the
basis ``L[0],L[1]`` of :math:`\mathrm{RH}^{4}(\overline{\mathcal{M}}_{2,0})`.

We can also use the function ``is_zero`` to check a tautological relation.
Below, we verify the divisor relation :math:`\kappa - \psi + \delta_0 = 0` on
:math:`\overline{\mathcal{M}}_{1,4}`::

    sage: g=1; n=4
    sage: reset_g_n(g,n)
    sage: bgraphs = [bd for bd in list_strata(g,n,1) if bd.numvert()>1]
    sage: del0 = sum([bd.to_tautclass() for bd in bgraphs]) # sum of boundary classes with separating node
    sage: psisum = sum([psiclass(i) for i in range(1,n+1)]) # sum of psi-classes
    sage: rel = kappaclass(1)-psisum+del0
    sage: rel.is_zero()
    True

Comparing classes on open subsets of :math:`\overline{\mathcal{M}}_{1,4}` using
parameter ``moduli`` to be one of ``'st'``, ``'tl'``, ``'ct'``, ``'rt'`` or
``'sm'``::

    sage: kappaclass(1,3,0).toTautbasis(moduli='sm')
    (1)
    sage: lambdaclass(1,3,0).toTautbasis(moduli='sm')
    (1/12)
    sage: diff = lambdaclass(1,3,0) - (1/12)*kappaclass(1,3,0)
    sage: diff.is_zero(moduli='sm')
    True

Pulling back tautological classes to a boundary divisor
-------------------------------------------------------

Below we create a stable graph ``bdry`` and compute a pullback of a
tautological class under the corresponding boundary gluing map. The result is
expressed in terms of a basis of the tautological ring on
:math:`\overline{\mathcal{M}}_{2,1} \times \overline{\mathcal{M}}_{2,1}`::

    sage: bdry = StableGraph([2,2],[[1],[2]],[(1,2)])
    sage: generator = tautgens(4,0,2)[3]
    sage: generator
    Graph :      [1, 3] [[2], [3]] [(2, 3)]
    Polynomial : 1*psi_3^1
    sage: pullback = bdry.boundary_pullback(generator)
    sage: pullback.totensorTautbasis(2)
    [
                               [-3]
                               [ 1]
                      [0 0 0]  [-3]
                      [0 0 0]  [ 7]
    [-3  1 -3  7  1], [0 0 0], [ 1]
    ]
    sage: pullback.totensorTautbasis(2,vecout=true)
    (-3, 1, -3, 7, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, -3, 1, -3, 7, 1)

We can see that in the Kunneth decomposition of
:math:`\mathrm{H}^4(\overline{\mathcal{M}}_{2,1} \times
\overline{\mathcal{M}}_{2,1})` the pullback has no component along
:math:`\mathrm{H}^2(\overline{\mathcal{M}}_{2,1}) \otimes
\mathrm{H}^2(\overline{\mathcal{M}}_{2,1})` and the contributions to
:math:`\mathrm{H}^0(\overline{\mathcal{M}}_{2,1}) \otimes
\mathrm{H}^4(\overline{\mathcal{M}}_{2,1})` and
:math:`\mathrm{H}^4(\overline{\mathcal{M}}_{2,1}) \otimes
\mathrm{H}^0(\overline{\mathcal{M}}_{2,1})` are symmetric, as expected.

Pushing forward classes from the boundary
-----------------------------------------

We can also compute the pushforward of the product of classes under a boundary
gluing map::

    sage: B = StableGraph([2,1],[[4,1,2],[3,5]],[(4,5)])
    sage: Bclass = B.boundary_pushforward() # class of undecorated boundary divisor
    sage: si1 = B.boundary_pushforward([fundclass(2,3),-psiclass(2,1,2)]); si1
    Graph :      [2, 1] [[4, 1, 2], [3, 5]] [(4, 5)]
    Polynomial : (-1)*psi_5^1
    sage: si2 = B.boundary_pushforward([-psiclass(1,2,3),fundclass(1,2)]); si2
    Graph :      [2, 1] [[4, 1, 2], [3, 5]] [(4, 5)]
    Polynomial : (-1)*psi_4^1

si1 is obtained by pushing forward the fundamental class on the genus 2 vertex
times :math:`-\psi_h` on the second vertex (where :math:`h` is the half-edge).
We can then check the self-intersection formula for the boundary divisor
above::

    sage: (Bclass*Bclass-si1-si2).is_zero()
    True

Special cycle classes
=====================

Double ramification cycles
--------------------------

Double ramification cycles are computed by the function ``DR_cycle(g,A)``. Below we verify a multiplicativity relation between DR-cycles from the paper [Holmes-Pixton-Schmitt]_::

    sage: A = vector((2,4,-6)); B = vector((-3,-1,4))
    sage: diff = DR_cycle(1,A)*DR_cycle(1,B)-DR_cycle(1,A)*DR_cycle(1,A+B)
    sage: diff.is_zero(moduli='tl') # vanishing on treelike locus
    True
    sage: diff.is_zero(moduli='st') # does not vanish on locus of all stable curves
    False

Calculating DR-cycles as classes with polynomial coefficients in the input::

    sage: R.<a1,a2,a3,b1,b2,b3> = PolynomialRing(QQ,6)
    sage: A = vector((a1,a2,a3)); B = vector((b1,b2,b3))
    sage: diff = DR_cycle(1,A)*DR_cycle(1,B)-DR_cycle(1,A)*DR_cycle(1,A+B)
    sage: diff.is_zero(moduli='tl')
    True

Checking intersection numbers of DR-cycles with lambdaclass from [Buryak-Rossi]_::

    sage: intersect = DR_cycle(1,A)*DR_cycle(1,B)*lambdaclass(1,1,3)
    sage: f = intersect.evaluate(); factor(f)
    (1/216) * (a2*b1 - a3*b1 - a1*b2 + a3*b2 + a1*b3 - a2*b3)^2
    sage: g = f.subs({a3:-a1-a2,b3:-b1-b2}); factor(g)
    (1/24) * (a2*b1 - a1*b2)^2

Strata of k-differentials
-------------------------

Strata of k-differentials using ``Strataclass(g,k,mu)`` with ``mu`` vector of
zero and pole multiplicities::

    sage: L = Strataclass(2,1,(3,-1)); L.is_zero()
    True
    sage: L = Strataclass(2,1,(2,)); (L-Hyperell(2,1)).is_zero()
    True

Generalized lambda classes
--------------------------

Computing Chern classes of :math:`R \pi_* \mathcal{O}(D)` for the universal
curve :math:`\mathcal{C}_{g,n} \to \overline{\mathcal{M}}_{g,n}` using
``generalized_lambda``::

    sage: g=3; n=1
    sage: l=1; d=[0]; a=[]
    sage: s = lambdaclass(2,g,n)
    sage: t = generalized_lambda(2,l,d,a,g,n)
    sage: (s-t).is_zero()
    True

Admissible cover cycles
-----------------------
Hyperelliptic and bielliptic cycles
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Computing the cycle of the hyperelliptic locus in genus 3::

    sage: H = Hyperell(3,0,0)

The cycle of hyperelliptic curves of genus 3 with 0 marked fixed points of
the involution and 0 marked pairs of conjugate points::

    sage: H.toTautbasis()
    (3/4, -9/4, -1/8)

We compare with the known expression :math:`H=9 \cdot \lambda_1-\delta_0-3\cdot \delta_1`::

    sage: reset_g_n(3, 0)
    sage: H2 = 9*lambdaclass(1)-(1/2)*irrbdiv()-3*sepbdiv(1,())
    sage: H2.toTautbasis()
    (3/4, -9/4, -1/8)

Creating and identifying general admissible cover cycles
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Below we define the group :math:`G=\mathbb{Z}/2\mathbb{Z}` and ramification
data ``H``, specifying that we look at double covers with two points of
stabilizer ``G[1]``, which is the generator of the group :math:`G`::

    sage: G = PermutationGroup([(1,2)]) # G=Z/2Z
    sage: H = HurData(G,[G[1],G[1]])

An example with this ramification behaviour is the locus of bielliptic curves
:math:`(C,p,q)` in :math:`\overline{\mathcal{M}}_{2,2}` of genus 2 curves
:math:`C`  admitting a double cover of an elliptic curve with marked
ramification points :math:`p,q` . The following identifies the class of this
locus in terms of the generating set ``tautgens(2,2,3)`` of
:math:`\mathrm{RH}^6(\overline{\mathcal{M}}_{2,2})`::

    sage: vbeta = Hidentify(2,H,vecout=true) # not tested (too long)
    sage: vector(vbeta) # not tested (too long)

If instead we wanted to specify a locus with two points of generator ``G[1]``
and one pair of points with generator ``G[0]``, we would consider::

    sage: H2 = HurData(G,[G[1],G[1],G[0]])

We can also identify the pushforward of the locus of bielliptic curves
:math:`(C,p,q)` under the map forgetting both markings, obtaining (a multiple
of) the locus of bielliptic curves :math:`C` inside
:math:`\overline{\mathcal{M}}_{2,0}`. For this we use the optional parameter
``markings`` to specify that no marking should be remembered::

    sage: G = PermutationGroup([(1,2)])
    sage: H = HurData(G,[G[1],G[1]])
    sage: Biell = Hidentify(2,H,markings=[])
    sage: Biell.toTautbasis(2,0,1)
    (30, -9)

We can compare this to a known formula :math:`[\overline{B}_2] = 3/2
\delta_{\text{irr}} + 3 \delta_1`. When entering this, note that ``irrbdiv``
returns two times the class :math:`\delta_{\text{irr}}` since in general the
convention is not to divide by automorphisms of stable graphs::

    sage: reset_g_n(2, 0)
    sage: Biell2 = 3/4*irrbdiv()+ 3*sepbdiv(1,())
    sage: Biell2.toTautbasis(2,0,1)
    (15/2, -9/4)

Example: Hurwitz-Hodge integrals
--------------------------------

Computing the Hurwitz-Hodge integral :math:`\int_{\overline{B}_{2,2,0}} \lambda_2`::

    sage: (Biell*lambdaclass(2,2,0)).evaluate()
    1/48

Computing Hurwitz-Hodge integral of cyclic triple covers of genus 0 curves
against :math:`\lambda_1`, see [Owens-Somerstep]_::

    sage: G = PermutationGroup([(1,2,3)])
    sage: g1 = G('(1,2,3)')
    sage: g2 = G('(1,3,2)')
    sage: H = HurData(G,[g1, g1, g2, g2]) #n=2, m=2
    sage: t = Hidentify(2,H,markings=[])
    sage: (t*lambdaclass(1,2,0)).evaluate()
    2/9

Citing ``admcycles``
====================

If you use ``admcycles`` in your research, consider citing the preprint [Delecroix-Schmitt-vanZelm]_.

References
==========

.. [Buryak-Rossi] Alexandr Buryak, Paolo Rossi
   "Quadratic double ramification integrals and the noncommutative KdV hierarchy"
   `arXiv:1909.11617 [math.AG] <https://arxiv.org/abs/1909.11617>`_

.. [Delecroix-Schmitt-vanZelm] Vincent Delecroix, Johannes Schmitt, Jason van Zelm
   "admcycles - a {S}age package for calculations in the tautological ring of the moduli space of stable curves"
   forthcoming

.. [Holmes-Pixton-Schmitt] David Holmes, Aaron Pixton, Johannes Schmitt
   "Multiplicativity of the double ramification cycle"
   `Documenta Mathematica, 24. (2019) <https://www.elibm.org/article/10011958>`_

.. [Owens-Somerstep] Bryson Owens, Seamus Somerstep
   "Boundary Expression for Chern Classes of the Hodge Bundle on Spaces of Cyclic Covers"
   `arXiv:1912.07720 [math.AG] <https://arxiv.org/abs/1912.07720>`_
