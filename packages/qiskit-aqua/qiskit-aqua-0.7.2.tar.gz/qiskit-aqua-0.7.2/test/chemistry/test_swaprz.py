# -*- coding: utf-8 -*-

# This code is part of Qiskit.
#
# (C) Copyright IBM 2019, 2020
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""Test of SWAPRZ from the circuit library."""

import warnings
from test.chemistry import QiskitChemistryTestCase
from ddt import ddt, data
from qiskit import BasicAer
from qiskit.circuit.library import ExcitationPreserving
from qiskit.aqua import QuantumInstance, aqua_globals
from qiskit.aqua.algorithms import VQE
from qiskit.aqua.components.optimizers import SLSQP
from qiskit.aqua.components.variational_forms import SwapRZ
from qiskit.chemistry.components.initial_states import HartreeFock
from qiskit.chemistry.drivers import HDF5Driver
from qiskit.chemistry.core import Hamiltonian, QubitMappingType


@ddt
class TestSwapRZ(QiskitChemistryTestCase):
    """
       SwapRZ was designed to preserve particles. We test it here from
       chemistry with JORDAN_WIGNER mapping and HartreeFock initial
       state to set it up. THis facilitates testing SwapRZ using these
       chemistry components/problem to ensure its correct operation
    """

    def setUp(self):
        super().setUp()
        self.seed = 50
        aqua_globals.random_seed = self.seed
        self.reference_energy = -1.137305593252385

    @data('wrapped', 'library')
    def test_swaprz(self, mode):
        """ SwapRZ variational form test """

        driver = HDF5Driver(self.get_resource_path('test_driver_hdf5.hdf5'))
        qmolecule = driver.run()
        operator = Hamiltonian(qubit_mapping=QubitMappingType.JORDAN_WIGNER,
                               two_qubit_reduction=False)
        qubit_op, _ = operator.run(qmolecule)

        optimizer = SLSQP(maxiter=100)
        initial_state = HartreeFock(operator.molecule_info['num_orbitals'],
                                    operator.molecule_info['num_particles'],
                                    qubit_mapping=operator._qubit_mapping,
                                    two_qubit_reduction=operator._two_qubit_reduction)

        if mode == 'wrapped':
            warnings.filterwarnings('ignore', category=DeprecationWarning)
            wavefunction = SwapRZ(qubit_op.num_qubits, initial_state=initial_state)
        else:
            wavefunction = ExcitationPreserving(qubit_op.num_qubits, initial_state=initial_state)

        algo = VQE(qubit_op, wavefunction, optimizer)

        if mode == 'wrapped':
            warnings.filterwarnings('always', category=DeprecationWarning)

        result = algo.run(QuantumInstance(BasicAer.get_backend('statevector_simulator'),
                                          seed_simulator=aqua_globals.random_seed,
                                          seed_transpiler=aqua_globals.random_seed))
        result = operator.process_algorithm_result(result)
        self.assertAlmostEqual(result.energy, self.reference_energy, places=6)
