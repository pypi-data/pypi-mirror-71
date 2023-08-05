import unittest

import numpy as np

import openmdao.api as om
from openmdao.utils.assert_utils import assert_near_equal


class TestMatrixVectorProductComp3x3(unittest.TestCase):

    def setUp(self):
        self.nn = 5

        self.p = om.Problem()

        ivc = om.IndepVarComp()
        ivc.add_output(name='A', shape=(self.nn, 3, 3))
        ivc.add_output(name='x', shape=(self.nn, 3))

        self.p.model.add_subsystem(name='ivc',
                                   subsys=ivc,
                                   promotes_outputs=['A', 'x'])

        self.p.model.add_subsystem(name='mat_vec_product_comp',
                                   subsys=om.MatrixVectorProductComp(vec_size=self.nn))

        self.p.model.connect('A', 'mat_vec_product_comp.A')
        self.p.model.connect('x', 'mat_vec_product_comp.x')

        self.p.setup(force_alloc_complex=True)

        self.p['A'] = np.random.rand(self.nn, 3, 3)
        self.p['x'] = np.random.rand(self.nn, 3)

        self.p.run_model()

    def test_results(self):

        for i in range(self.nn):
            A_i = self.p['A'][i, :, :]
            x_i = self.p['x'][i, :]
            b_i = self.p['mat_vec_product_comp.b'][i, :]

            expected_i = np.dot(A_i, x_i)
            np.testing.assert_almost_equal(b_i, expected_i)

    def test_partials(self):
        np.set_printoptions(linewidth=1024)
        cpd = self.p.check_partials(out_stream=None, method='cs')

        for comp in cpd:
            for (var, wrt) in cpd[comp]:
                np.testing.assert_almost_equal(actual=cpd[comp][var, wrt]['J_fwd'],
                                               desired=cpd[comp][var, wrt]['J_fd'],
                                               decimal=6)


class TestMatrixVectorProductComp6x4(unittest.TestCase):

    def setUp(self):
        self.nn = 5

        self.p = om.Problem()

        ivc = om.IndepVarComp()
        ivc.add_output(name='A', shape=(self.nn, 6, 4))
        ivc.add_output(name='x', shape=(self.nn, 4))

        self.p.model.add_subsystem(name='ivc',
                                   subsys=ivc,
                                   promotes_outputs=['A', 'x'])

        self.p.model.add_subsystem(name='mat_vec_product_comp',
                                   subsys=om.MatrixVectorProductComp(vec_size=self.nn,
                                                                     A_shape=(6, 4)))

        self.p.model.connect('A', 'mat_vec_product_comp.A')
        self.p.model.connect('x', 'mat_vec_product_comp.x')

        self.p.setup(force_alloc_complex=True)

        self.p['A'] = np.random.rand(self.nn, 6, 4)
        self.p['x'] = np.random.rand(self.nn, 4)

        self.p.run_model()

    def test_results(self):

        for i in range(self.nn):
            A_i = self.p['A'][i, :, :]
            x_i = self.p['x'][i, :]
            b_i = self.p['mat_vec_product_comp.b'][i, :]

            expected_i = np.dot(A_i, x_i)
            np.testing.assert_almost_equal(b_i, expected_i)

    def test_partials(self):
        cpd = self.p.check_partials(out_stream=None, method='cs')

        for comp in cpd:
            for (var, wrt) in cpd[comp]:
                np.testing.assert_almost_equal(actual=cpd[comp][var, wrt]['J_fwd'],
                                               desired=cpd[comp][var, wrt]['J_fd'],
                                               decimal=6)


class TestMatrixVectorProductCompNonVectorized(unittest.TestCase):

    def setUp(self):
        self.p = om.Problem()

        ivc = om.IndepVarComp()
        ivc.add_output(name='A', shape=(3, 3))
        ivc.add_output(name='x', shape=(3, 1))

        self.p.model.add_subsystem(name='ivc',
                                   subsys=ivc,
                                   promotes_outputs=['A', 'x'])

        self.p.model.add_subsystem(name='mat_vec_product_comp',
                                   subsys=om.MatrixVectorProductComp())

        self.p.model.connect('A', 'mat_vec_product_comp.A')
        self.p.model.connect('x', 'mat_vec_product_comp.x')

        self.p.setup(force_alloc_complex=True)

        self.p['A'] = np.random.rand(3, 3)
        self.p['x'] = np.random.rand(3, 1)

        self.p.run_model()

    def test_results(self):

        A_i = self.p['A']
        x_i = self.p['x']
        b_i = self.p['mat_vec_product_comp.b']

        expected = np.dot(np.reshape(A_i, (3, 3)), np.reshape(x_i, (3,)))
        assert_near_equal(b_i, expected)

    def test_partials(self):
        np.set_printoptions(linewidth=1024)
        cpd = self.p.check_partials(out_stream=None, method='cs')

        for comp in cpd:
            for (var, wrt) in cpd[comp]:
                assert_near_equal(
                                 actual=cpd[comp][var, wrt]['J_fwd'],
                                 desired=cpd[comp][var, wrt]['J_fd'])


class TestUnits(unittest.TestCase):

    def setUp(self):
        self.nn = 5

        self.p = om.Problem()

        ivc = om.IndepVarComp()
        ivc.add_output(name='A', shape=(self.nn, 3, 3), units='ft')
        ivc.add_output(name='x', shape=(self.nn, 3), units='lbf')

        self.p.model.add_subsystem(name='ivc',
                                   subsys=ivc,
                                   promotes_outputs=['A', 'x'])

        self.p.model.add_subsystem(name='mat_vec_product_comp',
                                   subsys=om.MatrixVectorProductComp(vec_size=self.nn,
                                                                     A_units='m', x_units='N',
                                                                     b_units='N*m'))

        self.p.model.connect('A', 'mat_vec_product_comp.A')
        self.p.model.connect('x', 'mat_vec_product_comp.x')

        self.p.setup(force_alloc_complex=True)

        self.p['A'] = np.random.rand(self.nn, 3, 3)
        self.p['x'] = np.random.rand(self.nn, 3)

        self.p.run_model()

    def test_results(self):

        for i in range(self.nn):
            A_i = self.p['A'][i, :, :]
            x_i = self.p['x'][i, :]
            b_i = self.p.get_val('mat_vec_product_comp.b', units='ft*lbf')[i, :]

            expected_i = np.dot(A_i, x_i)
            np.testing.assert_almost_equal(b_i, expected_i)

    def test_partials(self):
        np.set_printoptions(linewidth=1024)
        cpd = self.p.check_partials(out_stream=None, method='cs')

        for comp in cpd:
            for (var, wrt) in cpd[comp]:
                np.testing.assert_almost_equal(actual=cpd[comp][var, wrt]['J_fwd'],
                                               desired=cpd[comp][var, wrt]['J_fd'],
                                               decimal=6)


class TestFeature(unittest.TestCase):

    def test(self):
        import numpy as np
        import openmdao.api as om

        nn = 2

        p = om.Problem()

        ivc = om.IndepVarComp()
        ivc.add_output(name='Mat', shape=(nn, 3, 3))
        ivc.add_output(name='x', shape=(nn, 3), units='m')

        p.model.add_subsystem(name='ivc',
                              subsys=ivc,
                              promotes_outputs=['Mat', 'x'])

        p.model.add_subsystem(name='mat_vec_product_comp',
                              subsys=om.MatrixVectorProductComp(A_name='Mat', vec_size=nn,
                                                                b_name='y', b_units='m',
                                                                x_units='m'))

        p.model.connect('Mat', 'mat_vec_product_comp.Mat')
        p.model.connect('x', 'mat_vec_product_comp.x')

        p.setup()

        p['Mat'] = np.random.rand(nn, 3, 3)
        p['x'] = np.random.rand(nn, 3)

        p.run_model()

        Mat_i = p['Mat'][0, :, :]
        x_i = p['x'][0, :]

        expected_i = np.dot(Mat_i, x_i) * 3.2808399
        assert_near_equal(p.get_val('mat_vec_product_comp.y', units='ft')[0, :], expected_i, tolerance=1.0E-8)

        Mat_i = p['Mat'][1, :, :]
        x_i = p['x'][1, :]

        expected_i = np.dot(Mat_i, x_i) * 3.2808399
        assert_near_equal(p.get_val('mat_vec_product_comp.y', units='ft')[1, :], expected_i, tolerance=1.0E-8)


if __name__ == "__main__":
    unittest.main()
