from typing import List, Sequence, Union, Optional, Tuple
import itertools 
from pdb import set_trace
import cirq

from quple.circuit.quantum_circuit import QuantumCircuit

class EntanglementCircuit(QuantumCircuit):
    def __init__(self, n_qubit:int, name:str=None) -> None:
        super().__init__(n_qubit, name=name)
    
    @staticmethod
    def _validate_entangler_map(n_qubit:int, n_ent:int) -> None:
        if n_ent > n_qubit:
            raise ValueError('The number of entangled qubits in a block'
            'cannot exceed the total number of qubits in the circuit.')

    @staticmethod
    def _get_entangler_map(n_qubit:int, n_ent:Optional[int]=2,
                          method:str='full') -> List[Sequence[int]]:
        '''
        args
            n_qubit: number of qubits in the circuit
            n_ent: number of qubits to be entangled in a block
        '''
        EntanglementCircuit._validate_entangler_map(n_qubit, n_ent)
        n, m = n_qubit, n_ent
        entangler_map = None
        if method == 'full':
            entangler_map =  list(itertools.combinations(list(range(n)), m))
        elif method == 'linear':
            entangler_map =  [tuple(range(i, i + m)) for i in range(n - m + 1)]
        elif method == 'circular':
            entangler_map = [tuple(range(n - m + 1, n)) + (0,)]
            entangler_map += [tuple(range(i, i + m)) for i in range(n - m + 1)] #linear part
            
        return entangler_map
    
    def get_entangler_map(self, method:str='full', n_ent:Optional[int]=2,
                         qubit_repr:Optional[bool]=False) -> List[Tuple]:
        entangler_map = EntanglementCircuit._get_entangler_map(self.n_qubit, n_ent, method)
        if qubit_repr:
            return self.qubits.get(entangler_map)
        return entangler_map
    
    def _entanglement_pairing(self, qubits: Sequence[int]):
        '''determines how qubits are paired in the entanglement operation
        can be overriden
        args
            qubits: qubits to be entangled
        return
            list of tuples of qubit pairs for entanglement
        '''
        pairing_indices = [(qubits[i], qubits[i+1]) for i in range(len(qubits)-1)]
        # pairing_indices = [qpair for qpair in itertools.combinations(qubits, 2)]
        qubit_pairs = self._qubits.get(pairing_indices)
        return qubit_pairs
    
    def entangle(self, qubits:Sequence[int],
                 inverse:bool=False,
                 operation:cirq.Gate=cirq.ops.CNOT):
        '''entangle qubits in a quantum cirquit
        A application of a CNOT gate maximally entangles two qubits into the a Bell state
        args
            qubits: qubits to be entangled
            inverse: reverse the order of operation
            operation: gate operation that entangles the qubits
        example
        >>> cq.entangle
        '''
        
        qubit_pairs = self._entanglement_pairing(qubits)
        if inverse:
            qubit_pairs = qubit_pairs[::-1]
        self.append([operation(*qpair) for qpair in qubit_pairs])  
        
    '''
    def get_entangled_qubits(self) -> Set[Int]:
        entangled_qubits = set()        
    '''