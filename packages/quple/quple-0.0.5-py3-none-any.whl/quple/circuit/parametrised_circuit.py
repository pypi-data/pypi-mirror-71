from typing import List, Union

from quple.circuit.quantum_circuit import QuantumCircuit
from quple.components.parametrisation import UnresolvedParameters
from sympy import Symbol

class ParametrisedCircuit(QuantumCircuit):
    def __init__(self, n_qubit:int, 
                 parameters: Union[str, List[str], Symbol, List[Symbol]]=None) -> None:
        super().__init__(n_qubit)
        self._params = UnresolvedParameters(parameters)
        
    @property
    def params(self):
        return self._params
    
    def get_array_parameters(self, indices:List[int]):
        '''
        generate parameter symbols corresponding to the qubit indices
        >>>  cq.get_parameters((1,2))
        (x[1], x[2])
        '''
        return self.params.get_array(self._param_symbol, indices)        
    
    
        
        