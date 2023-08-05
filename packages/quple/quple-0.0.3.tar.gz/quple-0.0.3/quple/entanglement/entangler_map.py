from typing import List, Sequence, Union
from itertools import combinations

from quple.circuit.quantum_register import QuantumRegister

'''
if n_block_qubit > n_qubit:
    raise ValueError('The number of block qubits cannot exceed the number of '
                     'qubits in the circuit.')
'''


class EntanglerMap():
    def __init__(self, qr:Union[int, QuantumRegister], n_ent:int=2) -> None:
        '''
        qr: quantum register
        n_ent: number of entangled qubits in each block
        '''
        if isinstance(qr, int):
            self._qr = QuantumRegister(qr)
        elif isinstance(qr, QuantumRegister):
            self._qr = qr
        
        self._n_ent = n_ent
        
        if self.n_ent > self.n_qubit:
            raise ValueError('The number of entangled qubits in a block'
            'cannot exceed the total number of qubits in the circuit.')
            
            
    @property
    def n_qubit(self):
        '''
        number of circuit qubits
        '''
        return self._qr.n_qubit
    
    @property
    def n_ent(self):
        '''
        degree of entanglement
        '''
        return self._n_ent
    
    
    @property
    def qr(self):
        '''
        quantum registers involved in entangler map
        '''
        return self._qr
    
    @property
    def n_block_qubit(self):
        return self._n_block_qubit

    def full_entanglement(self) -> List[Sequence[int]]:
        n, m = self.n_qubit, self.n_ent
        return list(combinations(list(range(n)), m))

    def linear_entanglement(self) -> List[Sequence[int]]:
        n, m = self.n_qubit, self.n_ent
        return [tuple(range(i, i + m)) for i in range(n - m + 1)]

    def circular_entanglement(self) -> List[Sequence[int]]:
        n, m = self.n_qubit, self.n_ent
        return [tuple(range(n - m + 1, n)) + (0,)] + self.linear_entanglement()

    def get_entangler_map(self, method:str='full', qubit_repr:bool=False) -> List[Sequence[int]]:
        entangle_method = {
            'full': self.full_entanglement,
            'linear': self.linear_entanglement,
            'circular': self.circular_entanglement
        }
        entangler_map = entangle_method[method]()
        if qubit_repr:
            entangler_map = self._qr._parse_qubit_expression(entangler_map, self.qr.qubits)
        return entangler_map
