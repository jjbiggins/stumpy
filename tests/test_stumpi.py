import numpy as np
import numpy.testing as npt
import pandas as pd
from stumpy import stumpi, core, config
import pytest
import naive

substitution_locations = [(slice(0, 0), 0, -1, slice(1, 3), [0, 3])]
substitution_values = [np.nan, np.inf]


def test_stumpi_int_input():
    with pytest.raises(TypeError):
        stumpi(np.arange(10), 5)


def test_stumpi_self_join():
    m = 3
    zone = int(np.ceil(m / 4))

    seed = np.random.randint(100000)
    np.random.seed(seed)

    T = np.random.rand(30)
    stream = stumpi(T, m, egress=False)
    for i in range(34):
        t = np.random.rand()
        stream.update(t)

    comp_P = stream.P_
    comp_I = stream.I_
    comp_left_P = stream.left_P_
    comp_left_I = stream.left_I_

    ref_mp = naive.stamp(stream.T_, m, exclusion_zone=zone)
    ref_P = ref_mp[:, 0]
    ref_I = ref_mp[:, 1]
    ref_left_P = np.empty(ref_P.shape)
    ref_left_P[:] = np.inf
    ref_left_I = ref_mp[:, 2]
    for i, j in enumerate(ref_left_I):
        if j >= 0:
            D = core.mass(stream.T_[i : i + m], stream.T_[j : j + m])
            ref_left_P[i] = D[0]

    naive.replace_inf(ref_P)
    naive.replace_inf(ref_left_P)
    naive.replace_inf(comp_P)
    naive.replace_inf(comp_left_P)

    npt.assert_almost_equal(ref_P, comp_P)
    npt.assert_almost_equal(ref_I, comp_I)
    npt.assert_almost_equal(ref_left_P, comp_left_P)
    npt.assert_almost_equal(ref_left_I, comp_left_I)

    np.random.seed(seed)
    T = np.random.rand(30)
    T = pd.Series(T)
    stream = stumpi(T, m, egress=False)
    for i in range(34):
        t = np.random.rand()
        stream.update(t)

    comp_P = stream.P_
    comp_I = stream.I_
    comp_left_P = stream.left_P_
    comp_left_I = stream.left_I_

    naive.replace_inf(comp_P)
    naive.replace_inf(comp_left_P)

    npt.assert_almost_equal(ref_P, comp_P)
    npt.assert_almost_equal(ref_I, comp_I)
    npt.assert_almost_equal(ref_left_P, comp_left_P)
    npt.assert_almost_equal(ref_left_I, comp_left_I)


def test_stumpi_self_join_egress():
    m = 3

    seed = np.random.randint(100000)
    np.random.seed(seed)
    n = 30
    T = np.random.rand(n)

    ref_mp = naive.stumpi_egress(T, m)
    ref_P = ref_mp.P_.copy()
    ref_I = ref_mp.I_
    ref_left_P = ref_mp.left_P_.copy()
    ref_left_I = ref_mp.left_I_

    stream = stumpi(T, m, egress=True)

    comp_P = stream.P_.copy()
    comp_I = stream.I_
    comp_left_P = stream.left_P_.copy()
    comp_left_I = stream.left_I_

    naive.replace_inf(ref_P)
    naive.replace_inf(ref_left_P)
    naive.replace_inf(comp_P)
    naive.replace_inf(comp_left_P)

    npt.assert_almost_equal(ref_P, comp_P)
    npt.assert_almost_equal(ref_I, comp_I)
    npt.assert_almost_equal(ref_left_P, comp_left_P)
    npt.assert_almost_equal(ref_left_I, comp_left_I)

    for i in range(34):
        t = np.random.rand()
        ref_mp.update(t)
        stream.update(t)

        comp_P = stream.P_.copy()
        comp_I = stream.I_
        comp_left_P = stream.left_P_.copy()
        comp_left_I = stream.left_I_

        ref_P = ref_mp.P_.copy()
        ref_I = ref_mp.I_
        ref_left_P = ref_mp.left_P_.copy()
        ref_left_I = ref_mp.left_I_

        naive.replace_inf(ref_P)
        naive.replace_inf(ref_left_P)
        naive.replace_inf(comp_P)
        naive.replace_inf(comp_left_P)

        npt.assert_almost_equal(ref_P, comp_P)
        npt.assert_almost_equal(ref_I, comp_I)
        npt.assert_almost_equal(ref_left_P, comp_left_P)
        npt.assert_almost_equal(ref_left_I, comp_left_I)

    np.random.seed(seed)
    T = np.random.rand(n)
    T = pd.Series(T)

    ref_mp = naive.stumpi_egress(T, m)
    ref_P = ref_mp.P_.copy()
    ref_I = ref_mp.I_
    ref_left_P = ref_mp.left_P_.copy()
    ref_left_I = ref_mp.left_I_

    stream = stumpi(T, m, egress=True)

    comp_P = stream.P_.copy()
    comp_I = stream.I_
    comp_left_P = stream.left_P_.copy()
    comp_left_I = stream.left_I_

    naive.replace_inf(ref_P)
    naive.replace_inf(ref_left_P)
    naive.replace_inf(comp_P)
    naive.replace_inf(comp_left_P)

    npt.assert_almost_equal(ref_P, comp_P)
    npt.assert_almost_equal(ref_I, comp_I)
    npt.assert_almost_equal(ref_left_P, comp_left_P)
    npt.assert_almost_equal(ref_left_I, comp_left_I)

    for i in range(34):
        t = np.random.rand()
        t = np.random.rand()
        ref_mp.update(t)
        stream.update(t)

        comp_P = stream.P_.copy()
        comp_I = stream.I_
        comp_left_P = stream.left_P_.copy()
        comp_left_I = stream.left_I_

        ref_P = ref_mp.P_.copy()
        ref_I = ref_mp.I_
        ref_left_P = ref_mp.left_P_.copy()
        ref_left_I = ref_mp.left_I_

        naive.replace_inf(ref_P)
        naive.replace_inf(ref_left_P)
        naive.replace_inf(comp_P)
        naive.replace_inf(comp_left_P)

        npt.assert_almost_equal(ref_P, comp_P)
        npt.assert_almost_equal(ref_I, comp_I)
        npt.assert_almost_equal(ref_left_P, comp_left_P)
        npt.assert_almost_equal(ref_left_I, comp_left_I)


@pytest.mark.parametrize("substitute", substitution_values)
@pytest.mark.parametrize("substitution_locations", substitution_locations)
def test_stumpi_init_nan_inf_self_join(substitute, substitution_locations):
    m = 3
    zone = int(np.ceil(m / 4))

    seed = np.random.randint(100000)
    # seed = 58638

    for substitution_location in substitution_locations:
        np.random.seed(seed)
        T = np.random.rand(30)

        if substitution_location == -1:
            substitution_location = T.shape[0] - 1
        T[substitution_location] = substitute
        stream = stumpi(T, m, egress=False)
        for i in range(34):
            t = np.random.rand()
            stream.update(t)

        comp_P = stream.P_
        comp_I = stream.I_

        stream.T_[substitution_location] = substitute
        ref_mp = naive.stamp(stream.T_, m, exclusion_zone=zone)
        ref_P = ref_mp[:, 0]
        ref_I = ref_mp[:, 1]

        naive.replace_inf(ref_P)
        naive.replace_inf(comp_P)
        npt.assert_almost_equal(ref_P, comp_P)
        npt.assert_almost_equal(ref_I, comp_I)

        np.random.seed(seed)
        T = np.random.rand(30)

        if substitution_location == -1:  # pragma: no cover
            substitution_location = T.shape[0] - 1
        T[substitution_location] = substitute
        T = pd.Series(T)
        stream = stumpi(T, m, egress=False)
        for i in range(34):
            t = np.random.rand()
            stream.update(t)

        comp_P = stream.P_
        comp_I = stream.I_

        naive.replace_inf(comp_P)

        npt.assert_almost_equal(ref_P, comp_P)
        npt.assert_almost_equal(ref_I, comp_I)


@pytest.mark.parametrize("substitute", substitution_values)
@pytest.mark.parametrize("substitution_locations", substitution_locations)
def test_stumpi_init_nan_inf_self_join_egress(substitute, substitution_locations):
    m = 3

    seed = np.random.randint(100000)
    # seed = 58638

    for substitution_location in substitution_locations:
        np.random.seed(seed)
        n = 30
        T = np.random.rand(n)

        if substitution_location == -1:
            substitution_location = T.shape[0] - 1
        T[substitution_location] = substitute

        ref_mp = naive.stumpi_egress(T, m)
        ref_P = ref_mp.P_.copy()
        ref_I = ref_mp.I_
        ref_left_P = ref_mp.left_P_.copy()
        ref_left_I = ref_mp.left_I_

        stream = stumpi(T, m, egress=True)

        comp_P = stream.P_.copy()
        comp_I = stream.I_
        comp_left_P = stream.left_P_.copy()
        comp_left_I = stream.left_I_

        naive.replace_inf(ref_P)
        naive.replace_inf(ref_left_P)
        naive.replace_inf(comp_P)
        naive.replace_inf(comp_left_P)

        npt.assert_almost_equal(ref_P, comp_P)
        npt.assert_almost_equal(ref_I, comp_I)
        npt.assert_almost_equal(ref_left_P, comp_left_P)
        npt.assert_almost_equal(ref_left_I, comp_left_I)

        for i in range(34):
            t = np.random.rand()
            ref_mp.update(t)
            stream.update(t)

            comp_P = stream.P_.copy()
            comp_I = stream.I_
            comp_left_P = stream.left_P_.copy()
            comp_left_I = stream.left_I_

            ref_P = ref_mp.P_.copy()
            ref_I = ref_mp.I_
            ref_left_P = ref_mp.left_P_.copy()
            ref_left_I = ref_mp.left_I_

            naive.replace_inf(ref_P)
            naive.replace_inf(ref_left_P)
            naive.replace_inf(comp_P)
            naive.replace_inf(comp_left_P)

            npt.assert_almost_equal(ref_P, comp_P)
            npt.assert_almost_equal(ref_I, comp_I)
            npt.assert_almost_equal(ref_left_P, comp_left_P)
            npt.assert_almost_equal(ref_left_I, comp_left_I)

        np.random.seed(seed)
        T = np.random.rand(n)

        if substitution_location == -1:  # pragma: no cover
            substitution_location = T.shape[0] - 1
        T[substitution_location] = substitute
        T = pd.Series(T)

        ref_mp = naive.stumpi_egress(T, m)
        ref_P = ref_mp.P_.copy()
        ref_I = ref_mp.I_
        ref_left_P = ref_mp.left_P_.copy()
        ref_left_I = ref_mp.left_I_

        stream = stumpi(T, m, egress=True)

        comp_P = stream.P_.copy()
        comp_I = stream.I_
        comp_left_P = stream.left_P_.copy()
        comp_left_I = stream.left_I_

        naive.replace_inf(ref_P)
        naive.replace_inf(ref_left_P)
        naive.replace_inf(comp_P)
        naive.replace_inf(comp_left_P)

        npt.assert_almost_equal(ref_P, comp_P)
        npt.assert_almost_equal(ref_I, comp_I)
        npt.assert_almost_equal(ref_left_P, comp_left_P)
        npt.assert_almost_equal(ref_left_I, comp_left_I)

        for i in range(34):
            t = np.random.rand()
            ref_mp.update(t)
            stream.update(t)

            comp_P = stream.P_.copy()
            comp_I = stream.I_
            comp_left_P = stream.left_P_.copy()
            comp_left_I = stream.left_I_

            ref_P = ref_mp.P_.copy()
            ref_I = ref_mp.I_
            ref_left_P = ref_mp.left_P_.copy()
            ref_left_I = ref_mp.left_I_

            naive.replace_inf(ref_P)
            naive.replace_inf(ref_left_P)
            naive.replace_inf(comp_P)
            naive.replace_inf(comp_left_P)

            npt.assert_almost_equal(ref_P, comp_P)
            npt.assert_almost_equal(ref_I, comp_I)
            npt.assert_almost_equal(ref_left_P, comp_left_P)
            npt.assert_almost_equal(ref_left_I, comp_left_I)


@pytest.mark.parametrize("substitute", substitution_values)
@pytest.mark.parametrize("substitution_locations", substitution_locations)
def test_stumpi_stream_nan_inf_self_join(substitute, substitution_locations):
    m = 3
    zone = int(np.ceil(m / 4))

    seed = np.random.randint(100000)

    for substitution_location in substitution_locations:
        np.random.seed(seed)
        T = np.random.rand(64)

        stream = stumpi(T[:30], m, egress=False)
        if substitution_location == -1:
            substitution_location = T[30:].shape[0] - 1
        T[30:][substitution_location] = substitute
        for t in T[30:]:
            stream.update(t)

        comp_P = stream.P_
        comp_I = stream.I_

        stream.T_[30:][substitution_location] = substitute
        ref_mp = naive.stamp(stream.T_, m, exclusion_zone=zone)
        ref_P = ref_mp[:, 0]
        ref_I = ref_mp[:, 1]

        naive.replace_inf(ref_P)
        naive.replace_inf(comp_P)

        npt.assert_almost_equal(ref_P, comp_P)
        npt.assert_almost_equal(ref_I, comp_I)

        np.random.seed(seed)
        T = np.random.rand(64)

        stream = stumpi(pd.Series(T[:30]), m, egress=False)
        if substitution_location == -1:  # pragma: no cover
            substitution_location = T[30:].shape[0] - 1
        T[30:][substitution_location] = substitute
        for t in T[30:]:
            stream.update(t)

        comp_P = stream.P_
        comp_I = stream.I_

        naive.replace_inf(comp_P)

        npt.assert_almost_equal(ref_P, comp_P)
        npt.assert_almost_equal(ref_I, comp_I)


@pytest.mark.parametrize("substitute", substitution_values)
@pytest.mark.parametrize("substitution_locations", substitution_locations)
def test_stumpi_stream_nan_inf_self_join_egress(substitute, substitution_locations):
    m = 3

    seed = np.random.randint(100000)

    for substitution_location in substitution_locations:
        np.random.seed(seed)
        T = np.random.rand(64)
        n = 30

        ref_mp = naive.stumpi_egress(T[:n], m)
        ref_P = ref_mp.P_.copy()
        ref_I = ref_mp.I_
        ref_left_P = ref_mp.left_P_.copy()
        ref_left_I = ref_mp.left_I_

        stream = stumpi(T[:n], m, egress=True)

        comp_P = stream.P_.copy()
        comp_I = stream.I_
        comp_left_P = stream.left_P_.copy()
        comp_left_I = stream.left_I_

        naive.replace_inf(ref_P)
        naive.replace_inf(ref_left_P)
        naive.replace_inf(comp_P)
        naive.replace_inf(comp_left_P)

        npt.assert_almost_equal(ref_P, comp_P)
        npt.assert_almost_equal(ref_I, comp_I)
        npt.assert_almost_equal(ref_left_P, comp_left_P)
        npt.assert_almost_equal(ref_left_I, comp_left_I)

        if substitution_location == -1:
            substitution_location = T[30:].shape[0] - 1
        T[n:][substitution_location] = substitute
        for t in T[n:]:
            ref_mp.update(t)
            stream.update(t)

            comp_P = stream.P_.copy()
            comp_I = stream.I_
            comp_left_P = stream.left_P_.copy()
            comp_left_I = stream.left_I_

            ref_P = ref_mp.P_.copy()
            ref_I = ref_mp.I_
            ref_left_P = ref_mp.left_P_.copy()
            ref_left_I = ref_mp.left_I_

            naive.replace_inf(ref_P)
            naive.replace_inf(ref_left_P)
            naive.replace_inf(comp_P)
            naive.replace_inf(comp_left_P)

            npt.assert_almost_equal(ref_P, comp_P)
            npt.assert_almost_equal(ref_I, comp_I)
            npt.assert_almost_equal(ref_left_P, comp_left_P)
            npt.assert_almost_equal(ref_left_I, comp_left_I)

        np.random.seed(seed)
        T = np.random.rand(64)

        ref_mp = naive.stumpi_egress(T[:n], m)
        ref_P = ref_mp.P_.copy()
        ref_I = ref_mp.I_
        ref_left_P = ref_mp.left_P_.copy()
        ref_left_I = ref_mp.left_I_

        stream = stumpi(T[:n], m, egress=True)

        comp_P = stream.P_.copy()
        comp_I = stream.I_
        comp_left_P = stream.left_P_.copy()
        comp_left_I = stream.left_I_

        naive.replace_inf(ref_P)
        naive.replace_inf(ref_left_P)
        naive.replace_inf(comp_P)
        naive.replace_inf(comp_left_P)

        npt.assert_almost_equal(ref_P, comp_P)
        npt.assert_almost_equal(ref_I, comp_I)
        npt.assert_almost_equal(ref_left_P, comp_left_P)
        npt.assert_almost_equal(ref_left_I, comp_left_I)

        if substitution_location == -1:  # pragma: no cover
            substitution_location = T[n:].shape[0] - 1
        T[n:][substitution_location] = substitute
        for t in T[n:]:
            ref_mp.update(t)
            stream.update(t)

            comp_P = stream.P_.copy()
            comp_I = stream.I_
            comp_left_P = stream.left_P_.copy()
            comp_left_I = stream.left_I_

            ref_P = ref_mp.P_.copy()
            ref_I = ref_mp.I_
            ref_left_P = ref_mp.left_P_.copy()
            ref_left_I = ref_mp.left_I_

            naive.replace_inf(ref_P)
            naive.replace_inf(ref_left_P)
            naive.replace_inf(comp_P)
            naive.replace_inf(comp_left_P)

            npt.assert_almost_equal(ref_P, comp_P)
            npt.assert_almost_equal(ref_I, comp_I)
            npt.assert_almost_equal(ref_left_P, comp_left_P)
            npt.assert_almost_equal(ref_left_I, comp_left_I)


def test_stumpi_constant_subsequence_self_join():
    m = 3
    zone = int(np.ceil(m / 4))

    seed = np.random.randint(100000)
    np.random.seed(seed)

    T = np.concatenate((np.zeros(20, dtype=np.float64), np.ones(10, dtype=np.float64)))
    stream = stumpi(T, m, egress=False)
    for i in range(34):
        t = np.random.rand()
        stream.update(t)

    comp_P = stream.P_
    # comp_I = stream.I_

    ref_mp = naive.stamp(stream.T_, m, exclusion_zone=zone)
    ref_P = ref_mp[:, 0]
    # ref_I = ref_mp[:, 1]

    naive.replace_inf(ref_P)
    naive.replace_inf(comp_P)

    npt.assert_almost_equal(ref_P, comp_P)
    # npt.assert_almost_equal(ref_I, comp_I)

    np.random.seed(seed)
    T = np.concatenate((np.zeros(20, dtype=np.float64), np.ones(10, dtype=np.float64)))
    T = pd.Series(T)
    stream = stumpi(T, m, egress=False)
    for i in range(34):
        t = np.random.rand()
        stream.update(t)

    comp_P = stream.P_
    # comp_I = stream.I_

    naive.replace_inf(comp_P)

    npt.assert_almost_equal(ref_P, comp_P)
    # npt.assert_almost_equal(ref_I, comp_I)


def test_stumpi_constant_subsequence_self_join_egress():
    m = 3

    seed = np.random.randint(100000)
    np.random.seed(seed)

    T = np.concatenate((np.zeros(20, dtype=np.float64), np.ones(10, dtype=np.float64)))

    ref_mp = naive.stumpi_egress(T, m)
    ref_P = ref_mp.P_.copy()
    # ref_I = ref_mp.I_
    ref_left_P = ref_mp.left_P_.copy()
    # ref_left_I = ref_mp.left_I_

    stream = stumpi(T, m, egress=True)

    comp_P = stream.P_.copy()
    # comp_I = stream.I_
    comp_left_P = stream.left_P_.copy()
    # comp_left_I = stream.left_I_

    naive.replace_inf(ref_P)
    naive.replace_inf(ref_left_P)
    naive.replace_inf(comp_P)
    naive.replace_inf(comp_left_P)

    npt.assert_almost_equal(ref_P, comp_P)
    # npt.assert_almost_equal(ref_I, comp_I)
    npt.assert_almost_equal(ref_left_P, comp_left_P)
    # npt.assert_almost_equal(ref_left_I, comp_left_I)

    for i in range(34):
        t = np.random.rand()
        ref_mp.update(t)
        stream.update(t)

        comp_P = stream.P_.copy()
        # comp_I = stream.I_
        comp_left_P = stream.left_P_.copy()
        # comp_left_I = stream.left_I_

        ref_P = ref_mp.P_.copy()
        # ref_I = ref_mp.I_
        ref_left_P = ref_mp.left_P_.copy()
        # ref_left_I = ref_mp.left_I_

        naive.replace_inf(ref_P)
        naive.replace_inf(ref_left_P)
        naive.replace_inf(comp_P)
        naive.replace_inf(comp_left_P)

        npt.assert_almost_equal(ref_P, comp_P)
        # npt.assert_almost_equal(ref_I, comp_I)
        npt.assert_almost_equal(ref_left_P, comp_left_P)
        # npt.assert_almost_equal(ref_left_I, comp_left_I)

    np.random.seed(seed)
    T = np.concatenate((np.zeros(20, dtype=np.float64), np.ones(10, dtype=np.float64)))
    T = pd.Series(T)

    ref_mp = naive.stumpi_egress(T, m)
    ref_P = ref_mp.P_.copy()
    # ref_I = ref_mp.I_
    ref_left_P = ref_mp.left_P_.copy()
    # ref_left_I = ref_mp.left_I_

    stream = stumpi(T, m, egress=True)

    comp_P = stream.P_.copy()
    # comp_I = stream.I_
    comp_left_P = stream.left_P_.copy()
    # comp_left_I = stream.left_I_

    naive.replace_inf(ref_P)
    naive.replace_inf(ref_left_P)
    naive.replace_inf(comp_P)
    naive.replace_inf(comp_left_P)

    npt.assert_almost_equal(ref_P, comp_P)
    # npt.assert_almost_equal(ref_I, comp_I)
    npt.assert_almost_equal(ref_left_P, comp_left_P)
    # npt.assert_almost_equal(ref_left_I, comp_left_I)

    for i in range(34):
        t = np.random.rand()
        ref_mp.update(t)
        stream.update(t)

        comp_P = stream.P_.copy()
        # comp_I = stream.I_
        comp_left_P = stream.left_P_.copy()
        # comp_left_I = stream.left_I_

        ref_P = ref_mp.P_.copy()
        # ref_I = ref_mp.I_
        ref_left_P = ref_mp.left_P_.copy()
        # ref_left_I = ref_mp.left_I_

        naive.replace_inf(ref_P)
        naive.replace_inf(ref_left_P)
        naive.replace_inf(comp_P)
        naive.replace_inf(comp_left_P)

        npt.assert_almost_equal(ref_P, comp_P)
        # npt.assert_almost_equal(ref_I, comp_I)
        npt.assert_almost_equal(ref_left_P, comp_left_P)
        # npt.assert_almost_equal(ref_left_I, comp_left_I)


def test_stumpi_identical_subsequence_self_join():
    m = 3
    zone = int(np.ceil(m / 4))

    seed = np.random.randint(100000)
    np.random.seed(seed)

    identical = np.random.rand(8)
    T = np.random.rand(20)
    T[1 : 1 + identical.shape[0]] = identical
    T[11 : 11 + identical.shape[0]] = identical
    stream = stumpi(T, m, egress=False)
    for i in range(34):
        t = np.random.rand()
        stream.update(t)

    comp_P = stream.P_
    # comp_I = stream.I_

    ref_mp = naive.stamp(stream.T_, m, exclusion_zone=zone)
    ref_P = ref_mp[:, 0]
    # ref_I = ref_mp[:, 1]

    naive.replace_inf(ref_P)
    naive.replace_inf(comp_P)

    npt.assert_almost_equal(ref_P, comp_P, decimal=config.STUMPY_TEST_PRECISION)
    # npt.assert_almost_equal(ref_I, comp_I)

    np.random.seed(seed)
    identical = np.random.rand(8)
    T = np.random.rand(20)
    T[1 : 1 + identical.shape[0]] = identical
    T[11 : 11 + identical.shape[0]] = identical
    T = pd.Series(T)
    stream = stumpi(T, m, egress=False)
    for i in range(34):
        t = np.random.rand()
        stream.update(t)

    comp_P = stream.P_
    # comp_I = stream.I_

    naive.replace_inf(comp_P)

    npt.assert_almost_equal(ref_P, comp_P, decimal=config.STUMPY_TEST_PRECISION)
    # npt.assert_almost_equal(ref_I, comp_I)


def test_stumpi_identical_subsequence_self_join_egress():
    m = 3

    seed = np.random.randint(100000)
    np.random.seed(seed)

    identical = np.random.rand(8)
    T = np.random.rand(20)
    T[1 : 1 + identical.shape[0]] = identical
    T[11 : 11 + identical.shape[0]] = identical

    ref_mp = naive.stumpi_egress(T, m)
    ref_P = ref_mp.P_.copy()
    # ref_I = ref_mp.I_
    ref_left_P = ref_mp.left_P_.copy()
    # ref_left_I = ref_mp.left_I_

    stream = stumpi(T, m, egress=True)

    comp_P = stream.P_.copy()
    # comp_I = stream.I_
    comp_left_P = stream.left_P_.copy()
    # comp_left_I = stream.left_I_

    naive.replace_inf(ref_P)
    naive.replace_inf(ref_left_P)
    naive.replace_inf(comp_P)
    naive.replace_inf(comp_left_P)

    npt.assert_almost_equal(ref_P, comp_P, decimal=config.STUMPY_TEST_PRECISION)
    # npt.assert_almost_equal(ref_I, comp_I)
    npt.assert_almost_equal(
        ref_left_P, comp_left_P, decimal=config.STUMPY_TEST_PRECISION
    )
    # npt.assert_almost_equal(ref_left_I, comp_left_I)

    for i in range(34):
        t = np.random.rand()
        ref_mp.update(t)
        stream.update(t)

        comp_P = stream.P_.copy()
        # comp_I = stream.I_
        comp_left_P = stream.left_P_.copy()
        # comp_left_I = stream.left_I_

        ref_P = ref_mp.P_.copy()
        # ref_I = ref_mp.I_
        ref_left_P = ref_mp.left_P_.copy()
        # ref_left_I = ref_mp.left_I_

        naive.replace_inf(ref_P)
        naive.replace_inf(ref_left_P)
        naive.replace_inf(comp_P)
        naive.replace_inf(comp_left_P)

        npt.assert_almost_equal(ref_P, comp_P, decimal=config.STUMPY_TEST_PRECISION)
        # npt.assert_almost_equal(ref_I, comp_I)
        npt.assert_almost_equal(
            ref_left_P, comp_left_P, decimal=config.STUMPY_TEST_PRECISION
        )
        # npt.assert_almost_equal(ref_left_I, comp_left_I)

    np.random.seed(seed)
    identical = np.random.rand(8)
    T = np.random.rand(20)
    T[1 : 1 + identical.shape[0]] = identical
    T[11 : 11 + identical.shape[0]] = identical
    T = pd.Series(T)
    ref_mp = naive.stumpi_egress(T, m)
    ref_P = ref_mp.P_.copy()
    # ref_I = ref_mp.I_
    ref_left_P = ref_mp.left_P_.copy()
    # ref_left_I = ref_mp.left_I_

    stream = stumpi(T, m, egress=True)

    comp_P = stream.P_.copy()
    # comp_I = stream.I_
    comp_left_P = stream.left_P_.copy()
    # comp_left_I = stream.left_I_

    naive.replace_inf(ref_P)
    naive.replace_inf(ref_left_P)
    naive.replace_inf(comp_P)
    naive.replace_inf(comp_left_P)

    npt.assert_almost_equal(ref_P, comp_P, decimal=config.STUMPY_TEST_PRECISION)
    # npt.assert_almost_equal(ref_I, comp_I)
    npt.assert_almost_equal(
        ref_left_P, comp_left_P, decimal=config.STUMPY_TEST_PRECISION
    )
    # npt.assert_almost_equal(ref_left_I, comp_left_I)

    for i in range(34):
        t = np.random.rand()
        ref_mp.update(t)
        stream.update(t)

        comp_P = stream.P_.copy()
        # comp_I = stream.I_
        comp_left_P = stream.left_P_.copy()
        # comp_left_I = stream.left_I_

        ref_P = ref_mp.P_.copy()
        # ref_I = ref_mp.I_
        ref_left_P = ref_mp.left_P_.copy()
        # ref_left_I = ref_mp.left_I_

        naive.replace_inf(ref_P)
        naive.replace_inf(ref_left_P)
        naive.replace_inf(comp_P)
        naive.replace_inf(comp_left_P)

        npt.assert_almost_equal(ref_P, comp_P, decimal=config.STUMPY_TEST_PRECISION)
        # npt.assert_almost_equal(ref_I, comp_I)
        npt.assert_almost_equal(
            ref_left_P, comp_left_P, decimal=config.STUMPY_TEST_PRECISION
        )
        # npt.assert_almost_equal(ref_left_I, comp_left_I)


def test_stumpi_profile_index_match():
    T_full = np.random.rand(64)
    m = 3
    T_full_subseq = core.rolling_window(T_full, m)
    warm_start = 8

    T_stream = T_full[:warm_start].copy()
    stream = stumpi(T_stream, m, egress=True)
    P = np.full(stream.P_.shape, np.inf)
    left_P = np.full(stream.left_P_.shape, np.inf)

    n = 0
    for i in range(len(T_stream), len(T_full)):
        t = T_full[i]
        stream.update(t)

        P[:] = np.inf
        idx = np.argwhere(stream.I_ >= 0).flatten()
        P[idx] = naive.distance(
            naive.z_norm(T_full_subseq[idx + n + 1], axis=1),
            naive.z_norm(T_full_subseq[stream.I_[idx]], axis=1),
            axis=1,
        )

        left_P[:] = np.inf
        idx = np.argwhere(stream.left_I_ >= 0).flatten()
        left_P[idx] = naive.distance(
            naive.z_norm(T_full_subseq[idx + n + 1], axis=1),
            naive.z_norm(T_full_subseq[stream.left_I_[idx]], axis=1),
            axis=1,
        )

        npt.assert_almost_equal(stream.P_, P)
        npt.assert_almost_equal(stream.left_P_, left_P)

        n += 1
