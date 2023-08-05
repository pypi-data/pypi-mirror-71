from abc import ABC, abstractmethod
from typing import Optional, List, Union

from quple.circuit.quantum_circuit import QuantumCircuit
from quple.components.parametrisation import UnresolvedParameters

class EncodingCircuit(QuantumCircuit, ABC):
    '''The data encoding circuit
    A parametrised quantum circuit for encoding classical data into quantum states
    Examples:
    >>> cq = EncodingCircuit(5, depth=1, param_symbol='x')
    '''
    def __init__(self, feature_dimension:int, depth:int=1,
                param_symbol:Optional[str]=None, name:str=None):
        '''Create a new Pauli expansion circuit.
        Args:
            feature_dimension: dimension of data to be encoded (=number of qubits in the circuit)
            depth: the number of repeatition of the encoding circuit
            param_symbol: the symbol for the unresolved parameter array
        '''
        super().__init__(n_qubit=feature_dimension, name=name)
        self._feature_dimension = feature_dimension
        self._depth = depth
        self._param_symbol = param_symbol or 'x'
        self._params = UnresolvedParameters()
        self._params.append_array(self._param_symbol, feature_dimension)
        
    def get_parameters(self, indices:List[int]):
        '''
        obtain parameter symbols corresponding to the array indices
        >>>  cq.get_parameters((1,2))
        (x[1], x[2])
        '''
        return self._params.get_array(self._param_symbol, indices)        

    @abstractmethod
    def construct_circuit(self, inverse=False):
        raise NotImplementedError()
        
    @property
    def params(self):
        return self._params

    @property
    def param_symbol(self):
        return self._param_symbol
    
    @property
    def feature_dimension(self):
        return self._feature_dimension
    
    @property
    def depth(self):
        return self._depth