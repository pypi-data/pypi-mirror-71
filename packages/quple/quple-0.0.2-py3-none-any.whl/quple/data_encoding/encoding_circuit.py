from abc import ABC, abstractmethod

from quple.circuit.parametrised_circuit import ParametrisedCircuit


class EncodingCircuit(ParametrisedCircuit, ABC):

	def __init__(self, feature_dimenion:int, depth:int=1):
        super().__init__(feature_dimension)
		self._feature_dimension = feature_dimension
		self._depth = depth
        self.params.append_list('x', feature_dimension)

	@abstractmethod
	def construct_circuit(self, inverse=False):
		raise NotImplementedError()


	@property
	def feature_dimension(self):
		return self._feature_dimension
    
	@property
	def depth(self):
		return self._depth