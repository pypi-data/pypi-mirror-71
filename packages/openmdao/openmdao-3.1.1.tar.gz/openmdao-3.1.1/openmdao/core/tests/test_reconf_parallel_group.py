import numpy as np
import unittest

from openmdao.api import Problem, Group, IndepVarComp, ExplicitComponent, ExecComp
from openmdao.api import NewtonSolver, PETScKrylov, NonlinearBlockGS, LinearBlockGS
from openmdao.utils.assert_utils import assert_near_equal
from openmdao.utils.mpi import MPI

try:
    from openmdao.parallel_api import PETScVector
except ImportError:
    PETScVector = None


class ReconfGroup(Group):

    def __init__(self):
        super(ReconfGroup, self).__init__()

        self.parallel = True

    def setup(self):
        self._mpi_proc_allocator.parallel = self.parallel
        if self.parallel:
            self.nonlinear_solver = NewtonSolver(solve_subsystems=False)
            self.linear_solver = PETScKrylov()
        else:
            self.nonlinear_solver = NonlinearBlockGS()
            self.linear_solver = LinearBlockGS()

        self.add_subsystem('C1', ExecComp('z = 1 / 3. * y + x0'), promotes=['x0'])
        self.add_subsystem('C2', ExecComp('z = 1 / 4. * y + x1'), promotes=['x1'])

        self.connect('C1.z', 'C2.y')
        self.connect('C2.z', 'C1.y')

        self.parallel = not self.parallel


@unittest.skipUnless(MPI and PETScVector, "MPI and PETSc are required.")
class Test(unittest.TestCase):

    N_PROCS = 2

    def test(self):
        prob = Problem()
        prob.model.add_subsystem('Cx0', IndepVarComp('x0'), promotes=['x0'])
        prob.model.add_subsystem('Cx1', IndepVarComp('x1'), promotes=['x1'])
        prob.model.add_subsystem('g', ReconfGroup(), promotes=['*'])
        prob.setup()

        # First, run with full setup, so ReconfGroup should be a parallel group
        prob['x0'] = 6.
        prob['x1'] = 4.
        prob.run_model()
        assert_near_equal(prob.get_val('C1.z', get_remote=True), 8.0)
        assert_near_equal(prob.get_val('C2.z', get_remote=True), 6.0)

        # Now, reconfigure so ReconfGroup is not parallel, and x0, x1 should be preserved
        prob.model.g.resetup('reconf')
        prob.model.resetup('update')
        prob.run_model()
        assert_near_equal(prob.get_val('C1.z', get_remote=True), 8.0, 1e-8)
        assert_near_equal(prob.get_val('C2.z', get_remote=True), 6.0, 1e-8)


if __name__ == '__main__':
    unittest.main()
