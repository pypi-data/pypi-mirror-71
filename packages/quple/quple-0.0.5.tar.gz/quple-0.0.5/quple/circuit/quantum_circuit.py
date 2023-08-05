from abc import ABC, abstractmethod
import itertools
from typing import (Any, Callable, cast, Dict, FrozenSet, Iterable, Iterator,
                    List, Optional, overload, Sequence, Set, Tuple, Type,
                    TYPE_CHECKING, TypeVar, Union)
import re
import numpy as np 
from pdb import set_trace
import sympy

import cirq   
from cirq import  devices, GridQubit 
from cirq.circuits import InsertStrategy

from quple.circuit.quantum_register import QuantumRegister


# InsertStrategy.EARLIEST, InsertStrategy.NEW, InsertStrategy.INLINE and InsertStrategy.NEW_THEN_INLINE

class QuantumCircuit(cirq.Circuit):
    def __init__(self, n_qubit:int, name:str=None) -> None:
        super().__init__()
        self._name = 'qc' or name
        self._n_qubit = n_qubit
        self._qubits = QuantumRegister(n_qubit)
        self._blocks = {} # circuit blocks

    @staticmethod
    def _parse_qubit_operation(qubit_ops:Dict, target_qubits):
        resolved_operation = None
        for op in qubit_ops:
            pass

    @property
    def name(self) -> str:
        return self._name
    
    @property
    def n_qubit(self) -> int:
        return self._n_qubit

    @property
    def circuit(self):
        return self

    
    @property
    def qubits(self):
        return self._qubits

    @property
    def diagram(self):
        print(self)

    def apply_gate_operation(self, operation:cirq.Gate, qubit_expr):
        qubit_sequence = self._qubits.get(qubit_expr)
        strategy = InsertStrategy.INLINE
        if all(isinstance(qubits, GridQubit) for qubits in qubit_sequence):
            self.append([operation(qubit) for qubit in qubit_sequence], strategy=strategy)
        elif all(isinstance(qubits, tuple) for qubits in qubit_sequence):
            self.append([operation(*qubits) for qubits in qubit_sequence], strategy=strategy)
        else:
            raise ValueError('Inconsistent qubit representation: {}'.format(operation, qubit_sequence))
            
    def get_param_resolver(self, param_values: Dict):
        return cirq.ParamResolver(param_values)
    
    def _test01(self, repetitions=500):
        simulator.run(self, param_resolver, repetitions=repetitions)

    def S(self, qubit_expr):
        '''
        Clifford-S gate
        '''
        self.apply_gate_operation(cirq.ops.S, qubit_expr)

    def T(self, qubit_expr):
        '''
        Non-Clifford-T gate
        '''
        self.apply_gate_operation(cirq.ops.T, qubit_expr)


    def H(self, qubit_expr):
        '''
        Hadamard gate
        '''
        self.apply_gate_operation(cirq.ops.H, qubit_expr)

    def R(self, axis:str, theta:Union[int, float], qubit_expr):
        if axis.lower() == 'x':
            self.Rx(theta, qubit_expr)
        elif axis.lower() == 'y':
            self.Ry(theta, qubit_expr)
        elif axis.lower() == 'z':
            self.Rz(theta, qubit_expr)
        else:
            raise ValueError('Invalid rotation axis: {}'.format(axis))
    
    def Rx(self, theta:Union[int, float], qubit_expr):
        self.apply_gate_operation(cirq.ops.rx(theta), qubit_expr)

    def Ry(self, theta:Union[int, float], qubit_expr):
        self.apply_gate_operation(cirq.ops.ry(theta), qubit_expr)

    def Rz(self, theta:Union[int, float], qubit_expr):
        self.apply_gate_operation(cirq.ops.rz(theta), qubit_expr)                
    
    def SWAP(self, qubit_expr):
        '''
        SWAP gate
        '''
        self.apply_gate_operation(cirq.ops.SWAP, qubit_expr)
    

    def PauliX(self, qubit_expr):
        self.apply_gate_operation(cirq.X, qubit_expr)
        
    def PauliY(self, qubit_expr):
        self.apply_gate_operation(cirq.Y, qubit_expr)

    def PauliZ(self, qubit_expr):
        self.apply_gate_operation(cirq.Z, qubit_expr)
        

    def CNOT(self, qubit_expr):
        '''
        Controlled NOT gate
        '''
        self.apply_gate_operation(cirq.ops.CNOT, qubit_expr)
    
    def Toffoli(self, qubit_expr):
        self.apply_gate_operation(cirq.ops.TOFFOLI, qubit_expr)

    def PhaseShift(self, phi, qubit_expr):
        self.apply_gate_operation(cirq.ZPowGate(exponent=phi / np.pi), qubit_expr)
    
    def u1(self, theta:Union[int, float], qubit_expr):
        '''
        qiskit implementation: u1 = RZ gate
        named u1 for hardware reason
        '''
        return self.Rz(theta, qubit_expr)
            
    def CX(self, qubit_expr):
        '''
        Same as CNOT gate
        '''
        self.apply_gate_operation(cirq.ops.CX, qubit_expr)
  
    def CZ(self, qubit_expr):
        '''
        Controlled Z gate
        '''
        self.apply_gate_operation(cirq.ops.CZ, qubit_expr)
        
    def clear(self) -> None:
        '''
        clear all moments
        '''
        self._moments = []
        
    @property
    def blocks(self):
        return self._blocks
    
    def new_block(self, label:str, ignore_redef:bool=True) -> None:
        if (not ignore_redef) and (label in self._blocks):
            raise RuntimeError('circuit block with label {} already exist'.format(label))
        self._blocks[label] = QuantumCircuit(self._n_qubit, name=label)
        return self._blocks[label]
            
    def append_block(self, label:Union[str, 'QuantumCircuit']) -> None:
        if isinstance(label, str):
            self += self.blocks[label]
        elif isinstance(label, QuantumCircuit):
            self += label
        else:
            raise ValueError('unknown circuit block of type {}'.format(label))


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
        QuantumCircuit._validate_entangler_map(n_qubit, n_ent)
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
        entangler_map = QuantumCircuit._get_entangler_map(self.n_qubit, n_ent, method)
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