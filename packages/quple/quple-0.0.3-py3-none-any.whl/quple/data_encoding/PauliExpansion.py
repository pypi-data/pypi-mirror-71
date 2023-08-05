from functools import reduce
import numpy as np

from quple import QuantumCircuit

from .feature_map import FeatureMap 


class PauliExpansion(EncodingCircuit):
	def __init__(self, feature_dimension: int,
                 depth: int=2, paulis:List[str] = ['Z', 'ZZ']):
		super().__init__(feature_dimension, depth)
        self._paulis = paulis
        

	def construct_circuit(self, inverse=False):
        self.clear()
        n_qubit = self._n_qibit
        # build the Hadamard layer
        Hadamard_layer = self.new_block('Hadamard_layer')
        Hadamard_layer.H(range(n_qubit))
        self.append_block(Hadamard_layer)
        
        # build the entanglement layer
		
        
def self_product(x: np.ndarray) -> float:
    """
    Define a function map from R^n to R.

    Args:
        x: data

    Returns:
        float: the mapped value
    """
    coeff = x[0] if len(x) == 1 else reduce(lambda m, n: m * n, np.pi - x)  
    return coeff


'''

#reverse order of Pauli operations:
    pauli = pauli[::-1]
    

for pauli in paulis:
    mapped_params = ...
    puli_block = pauli_evolution(pauli, mapped_params)
    
    
pauli_string = pauli_string[::-1]

# trim the pauli string if identities are included
trimmed = []
indices = []
for i, pauli in enumerate(pauli_string):
    if pauli != 'I':
        trimmed += [pauli]
        indices += [i]

evo = QuantumCircuit(len(pauli_string))

if len(trimmed) == 0:
    return evo

def basis_change(circuit, inverse=False):
    for i, pauli in enumerate(pauli_string):
        if pauli == 'X':
            circuit.h(i)
        elif pauli == 'Y':
            circuit.rx(-np.pi / 2 if inverse else np.pi / 2, i)

def cx_chain(circuit, inverse=False):
    num_cx = len(indices) - 1
    for i in reversed(range(num_cx)) if inverse else range(num_cx):
        circuit.cx(indices[i], indices[i + 1])

basis_change(evo)
cx_chain(evo)
evo.u1(2.0 * time, indices[-1])
cx_chain(evo, inverse=True)
basis_change(evo, inverse=True)


get_entangler_map = list(combinations(list(range(num_circuit_qubits)), num_block_qubits))

build_entanglement_layer = 

#i : repetition
#j : the j-th block ['Z','ZZ'] = 2 blocks
#indices: the entanglement indices
for j, block in enumerate(self.entanglement_blocks):
    # create a new layer and get the entangler map for this block
    layer = QuantumCircuit(*self.qregs)
    entangler_map = self.get_entangler_map(i, j, block.num_qubits)

    # apply the operations in the layer
    for indices in entangler_map:
        parametrized_block = self._parametrize_block(block, param_iter, i, j, indices)
        layer.compose(parametrized_block, indices, inplace=True)

    # add the layer to the circuit
    self += layer


def _parametrize_block(self, block, param_iter=None, rep_num=None, block_num=None, indices=None,
                       params=None):
    """Convert ``block`` to a circuit of correct width and parameterized using the iterator."""
    if self._overwrite_block_parameters:
        # check if special parameters should be used
        # pylint: disable=assignment-from-none
        if params is None:
            params = self._parameter_generator(rep_num, block_num, indices)
        if params is None:
            params = [next(param_iter) for _ in range(len(get_parameters(block)))]

        update = dict(zip(block.parameters, params))
        return block.assign_parameters(update)

    return block.copy()
    
def compose(self, other, qubits=None, clbits=None, front=False, inplace=False):
    """Compose circuit with ``other`` circuit or instruction, optionally permuting wires.

    ``other`` can be narrower or of equal width to ``self``.

    Args:
        other (qiskit.circuit.Instruction or QuantumCircuit or BaseOperator):
            (sub)circuit to compose onto self.
        qubits (list[Qubit|int]): qubits of self to compose onto.
        clbits (list[Clbit|int]): clbits of self to compose onto.
        front (bool): If True, front composition will be performed (not implemented yet).
        inplace (bool): If True, modify the object. Otherwise return composed circuit.

    Returns:
        QuantumCircuit: the composed circuit (returns None if inplace==True).

    Raises:
        CircuitError: if composing on the front.
        QiskitError: if ``other`` is wider or there are duplicate edge mappings.

    Examples:

        >>> lhs.compose(rhs, qubits=[3, 2], inplace=True)

        .. parsed-literal::

                        ┌───┐                   ┌─────┐                ┌───┐
            lqr_1_0: ───┤ H ├───    rqr_0: ──■──┤ Tdg ├    lqr_1_0: ───┤ H ├───────────────
                        ├───┤              ┌─┴─┐└─────┘                ├───┤
            lqr_1_1: ───┤ X ├───    rqr_1: ┤ X ├───────    lqr_1_1: ───┤ X ├───────────────
                     ┌──┴───┴──┐           └───┘                    ┌──┴───┴──┐┌───┐
            lqr_1_2: ┤ U1(0.1) ├  +                     =  lqr_1_2: ┤ U1(0.1) ├┤ X ├───────
                     └─────────┘                                    └─────────┘└─┬─┘┌─────┐
            lqr_2_0: ─────■─────                           lqr_2_0: ─────■───────■──┤ Tdg ├
                        ┌─┴─┐                                          ┌─┴─┐        └─────┘
            lqr_2_1: ───┤ X ├───                           lqr_2_1: ───┤ X ├───────────────
                        └───┘                                          └───┘
            lcr_0: 0 ═══════════                           lcr_0: 0 ═══════════════════════

            lcr_1: 0 ═══════════                           lcr_1: 0 ═══════════════════════

    """
    if front:
        raise CircuitError("Front composition of QuantumCircuit not supported yet.")

    if isinstance(other, QuantumCircuit):
        from qiskit.converters.circuit_to_dag import circuit_to_dag
        from qiskit.converters.dag_to_circuit import dag_to_circuit

        dag_self = circuit_to_dag(self)
        dag_other = circuit_to_dag(other)
        dag_self.compose(dag_other, qubits=qubits, clbits=clbits, front=front)
        composed_circuit = dag_to_circuit(dag_self)
        if inplace:  # FIXME: this is just a hack for inplace to work. Still copies.
            self.__dict__.update(composed_circuit.__dict__)
            return None
        else:
            return composed_circuit

    else:  # fall back to append which accepts Instruction and BaseOperator
        if inplace:
            self.append(other, qargs=qubits, cargs=clbits)
            return None
        else:
            new_circuit = self.copy()
            new_circuit.append(other, qargs=qubits, cargs=clbits)
            return new_circuit    

'''