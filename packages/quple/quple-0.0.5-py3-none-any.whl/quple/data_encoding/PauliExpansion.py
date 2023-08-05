from functools import reduce
from typing import List, Union, Optional, Callable
import numpy as np
from pdb import set_trace

import cirq

from quple.circuit.quantum_circuit import QuantumCircuit

from .encoding_circuit import EncodingCircuit


class PauliExpansion(EncodingCircuit):
    '''PauliExpansion feature map

    '''    
    def __init__(self, feature_dimension: int,
                 depth: int=2, paulis:List[str] = ['Z', 'ZZ'],
                 data_morphism:Optional[Callable[[np.ndarray], float]] = None,
                 rz_based:bool=True, name:str=None):
        '''Create PauliExpansion feature map
        
        '''
        super().__init__(feature_dimension, depth, name=name)
        self.paulis = paulis
        self._data_morphism = data_morphism or self_product
        self._rz_based = rz_based # make rotation always along Z axis (more of hardware reason)
        
    @staticmethod
    def _validate_paulis(paulis:List[str]):
        for pauli_str in paulis:
            for pauli in pauli_str:
                if not pauli.upper() in ['Z','X','Y','I']:
                    raise ValueError('Invalid Pauli operation: {}'.format(pauli))
        
    @property
    def data_morphism(self):
        return self._data_morphism
    
    @property
    def paulis(self):
        return self._paulis
    
    @paulis.setter
    def paulis(self, value):
        PauliExpansion._validate_paulis(value)
        self._paulis = value
    
    
    def construct_circuit(self, inverse=False):
        self.clear()
        n_qubit = self._n_qubit
        # build the Hadamard layer
        # this maps the |0>*n state into a superposition of 2^n states of equal weight
        # i.e. to the computational basis
        Hadamard_layer = self.new_block('Hadamard_layer')
        Hadamard_layer.H(range(n_qubit))
        self += Hadamard_layer
                                  
        def basis_change(circuit, var, string, inverse=False):
            for i, s in enumerate(string):
                if s == 'X':
                    circuit.H(var[i])
                elif s == 'Y':
                    circuit.Rx(-np.pi / 2 if inverse else np.pi / 2, var[i])
            
        # build the entanglement layer
        for pauli_string in self.paulis:
            entangle_layer = self.new_block('Entangle_layer_{}'.format(pauli_string))
            pauli_string = pauli_string[::-1]
            trimmed, indices = [], []     
            for i, pauli in enumerate(pauli_string):
                if pauli != 'I':
                    trimmed += [pauli]
                    indices += [i]
            if len(trimmed) == 0:
                continue          
            entangler_map = self.get_entangler_map('full', n_ent = len(pauli_string))
            
            for variables in entangler_map:
                basis_change(entangle_layer, variables, pauli_string)
                qubits_to_entangle = tuple(variables[i] for i in indices)
                entangle_layer.entangle(qubits_to_entangle)
                parameters = self.get_parameters(variables)
                mapped_value = self.data_morphism(parameters)            
                entangle_layer.Rz(2.0*mapped_value, variables[-1])
                entangle_layer.entangle(qubits_to_entangle, inverse=True)
                basis_change(entangle_layer, variables, pauli_string, inverse=True)
            self += entangle_layer
        
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
