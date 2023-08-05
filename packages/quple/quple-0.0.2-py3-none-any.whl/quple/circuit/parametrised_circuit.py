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
    
        
        