from typing import *

from qiskit.providers import BackendV2 as _BaseProvider
from qiskit_ibm_runtime.fake_provider import FakeQuebec as _FakeProvider

from qiskit_ibm_runtime.base_primitive import BasePrimitiveV2 as _BaseExecutor
from qiskit_ibm_runtime import SamplerV2 as _QuantumSampler

from qiskit.transpiler import StagedPassManager as _BaseTranspiler
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager as _generate_preset_pass_manager


class Backend:
    """ Qiskit Quantum Backend

    Attributes:
        provider (str): The name of the quantum computing service.
        executor (str): The type of execution engine to use.
        transpiler_seed (int, None): The seed for the transpiler. None if not given by the user.
        simulator_seed (int, None): The seed for the simulator. None if not given by the user.
    """

    def __init__(self, provider: str = 'simulator', executor: str = 'sampler',
                 transpiler_seed: Union[int, None] = None, simulator_seed: Union[int, None] = None):
        """ Instantiate a Qiskit Quantum Backend

        :param provider: The name of the quantum computing service (e.g. 'simulator' or 'ibm_xxx').
                         Currently only supports 'simulator'.
        :type provider: str

        :param executor: The type of execution engine to use (e.g. 'sampler').
                         Currently only supports 'sampler'.
        :type executor: str

        :param transpiler_seed: The seed for the transpiler (e.g. 1234).
                                Must be non-negative.
                                Leave None to use a random seed (cannot be retrieved).
        :type transpiler_seed: int, None

        :param simulator_seed: The seed for the simulator (e.g. 1234).
                               Leave None to use a random seed (cannot be retrieved).
        :type simulator_seed: int, None
        """
        self.provider = provider
        self.executor = executor
        self.transpiler_seed = transpiler_seed
        self.simulator_seed = simulator_seed

        self._provider: _BaseProvider = Backend._new_provider(provider=provider)
        self._executor: _BaseExecutor = Backend._new_executor(provider=self._provider,
                                                              executor=executor,
                                                              seed=simulator_seed)
        self._transpiler: _BaseTranspiler = Backend._new_transpiler(provider=self._provider,
                                                                    seed=transpiler_seed)

    def __repr__(self):
        return (f'<Backend: provider={self.provider}, '
                f'executor={self.executor}, '
                f'transpiler_seed={self.transpiler_seed}, '
                f'simulator_seed={self.simulator_seed}>')

    @staticmethod
    def _new_provider(provider: str = 'simulator') -> _BaseProvider:
        if provider == 'simulator':
            # Instantiate a fake provider
            return _FakeProvider()
        raise ValueError(f'Provider {provider} is not supported')

    @staticmethod
    def _new_executor(provider: _BaseProvider,
                      executor: str = 'sampler',
                      seed: Union[int, None] = None) -> _BaseExecutor:
        # Construct the options
        options = {
            "simulator": {}
        }
        if seed is not None:
            options['simulator']['seed_simulator'] = seed
        if executor == 'sampler':
            # Instantiate a sampler
            return _QuantumSampler(mode=provider, options=options)
        raise ValueError(f'Method "{executor}" is not implemented')

    @staticmethod
    def _new_transpiler(provider: _BaseProvider,
                        seed: Union[int, None] = None) -> _BaseTranspiler:
        assert seed is None or seed >= 0, 'Transpiler seed must be non-negative'
        # Instantiate a transpiler
        return _generate_preset_pass_manager(
            seed_transpiler=seed,
            optimization_level=3,
            backend=provider,
            layout_method='sabre',
            routing_method='sabre',
            translation_method='translator',
            scheduling_method='asap',
            approximation_degree=1.0,
            unitary_synthesis_method='default'
        )
