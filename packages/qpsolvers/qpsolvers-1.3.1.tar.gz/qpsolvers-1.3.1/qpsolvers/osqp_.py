#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2016-2020 Stephane Caron <stephane.caron@normalesup.org>
#
# This file is part of qpsolvers.
#
# qpsolvers is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# qpsolvers is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with qpsolvers. If not, see <http://www.gnu.org/licenses/>.

import osqp

from numpy import hstack, inf, ndarray, ones
from osqp import OSQP
from scipy.sparse import csc_matrix, vstack
from warnings import warn


__verbose__ = False


def conversion_warning(M):
    return "Converted %s to scipy.sparse.csc.csc_matrix\n" \
        "For best performance, build %s as a csc_matrix " \
        "rather than as a numpy.ndarray" % (M, M)


def osqp_set_verbosity(verbose):
    global __verbose__
    __verbose__ = verbose


def osqp_solve_qp(P, q, G=None, h=None, A=None, b=None, initvals=None):
    """
    Solve a Quadratic Program defined as:

        minimize
            (1/2) * x.T * P * x + q.T * x

        subject to
            G * x <= h
            A * x == b

    using OSQP <https://github.com/oxfordcontrol/osqp>.

    Parameters
    ----------
    P : scipy.sparse.csc_matrix
        Symmetric quadratic-cost matrix.
    q : numpy.array
        Quadratic cost vector.
    G : scipy.sparse.csc_matrix
        Linear inequality constraint matrix.
    h : numpy.array
        Linear inequality constraint vector.
    A : scipy.sparse.csc_matrix, optional
        Linear equality constraint matrix.
    b : numpy.array, optional
        Linear equality constraint vector.
    initvals : numpy.array, optional
        Warm-start guess vector.

    Returns
    -------
    x : array, shape=(n,)
        Solution to the QP, if found, otherwise ``None``.

    Note
    ----
    OSQP requires `P` to be symmetric, and won't check for errors otherwise.
    Check out for this point if you e.g. `get nan values
    <https://github.com/oxfordcontrol/osqp/issues/10>`_ in your solutions.
    """
    global __verbose__
    if type(P) is ndarray:
        warn(conversion_warning("P"))
        P = csc_matrix(P)
    solver = OSQP()
    if A is None and G is None:
        solver.setup(P=P, q=q, verbose=__verbose__)
    elif A is not None:
        if type(A) is ndarray:
            warn(conversion_warning("A"))
            A = csc_matrix(A)
        if G is None:
            solver.setup(P=P, q=q, A=A, l=b, u=b, verbose=__verbose__)
        else:  # G is not None
            l = -inf * ones(len(h))
            qp_A = vstack([G, A]).tocsc()
            qp_l = hstack([l, b])
            qp_u = hstack([h, b])
            solver.setup(P=P, q=q, A=qp_A, l=qp_l, u=qp_u, verbose=__verbose__)
    else:  # A is None
        if type(G) is ndarray:
            warn(conversion_warning("G"))
            G = csc_matrix(G)
        l = -inf * ones(len(h))
        solver.setup(P=P, q=q, A=G, l=l, u=h, verbose=__verbose__)
    if initvals is not None:
        solver.warm_start(x=initvals)
    res = solver.solve()
    if hasattr(solver, 'constant'):
        success_status = solver.constant('OSQP_SOLVED')
    else:  # more recent versions of OSQP
        success_status = osqp.constant('OSQP_SOLVED')
    if res.info.status_val != success_status:
        print("OSQP exited with status '%s'" % res.info.status)
    return res.x
