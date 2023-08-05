from __future__ import annotations
from abc import ABC, abstractmethod

from typing import (Any, Callable, cast, Dict, FrozenSet, Iterable, Iterator,
                    List, Optional, overload, Sequence, Set, Tuple, Type,
                    TYPE_CHECKING, TypeVar, Union)
import re
import numpy as np 

import sympy

import cirq   
from cirq import  devices, GridQubit 

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
        strategy = cirq.circuits.InsertStrategy.NEW_THEN_INLINE
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

    def apply_sequential_gate_operations(self, qubit_ops:list):
        for qop in qubit_ops:
            operation = QuantumCircuit._parse_qubit_operation(qop, self._qubits)
            self.append(operation)
            
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
            
    
    def append_block(self, label:Union[str, QuantumCircuit]) -> None:
        if isinstance(label, str):
            self += self.blocks[label]
        elif isinstance(label, QuantumCircuit):
            self += label
        else:
            raise ValueError('unknown circuit block of type {}'.format(label))

    def google_device_layouts(self, name):
        if name == 'Syncamore':
            return cirq.google.Syncamore
        elif name == 'Sycamore23':
            return cirq.google.Sycamore23
        elif name == 'Bristlecone':
            return cirq.google.Bristlecone
        elif name == 'Foxtail':
            return cirq.google.Foxtail
    '''
    def get_entangled_qubits(self) -> Set[Int]:
        entangled_qubits = set()
    '''

