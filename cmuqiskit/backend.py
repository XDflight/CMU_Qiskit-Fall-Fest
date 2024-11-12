from typing import *

from qiskit.providers import BackendV2 as _BaseProvider
from qiskit_ibm_runtime.fake_provider import FakeQuebec as _FakeProvider

from qiskit_ibm_runtime.base_primitive import BasePrimitiveV2 as _BaseExecutor
from qiskit_ibm_runtime import SamplerV2 as _QuantumSampler

from qiskit.transpiler import StagedPassManager as _BaseTranspiler
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager as _generate_preset_pass_manager


class Backend:
    """Qiskit Quantum Backend"""

    def __init__(self, provider: Union[str, None] = None, executor: str = 'sampler',
                 executor_seed: Union[int, None] = None, transpiler_seed: Union[int, None] = None):
        """ Instantiate a Qiskit Quantum Backend

        :param provider: The name of the quantum computing service (e.g. 'qiskit-ibm').
                         Leave None to use the simulator.
                         Currently only supports the simulator.
        :type provider: str or None

        :param executor: The type of execution engine to use (e.g. 'sampler').
                         Currently only supports 'sampler'.
        :type executor: str

        :param executor_seed: The seed for the execution engine (e.g. 1234).
        :type executor_seed: int

        :param transpiler_seed: The seed for the transpiler engine (e.g. 1234).
        :type transpiler_seed: int
        """
        self.provider = provider
        self.executor = executor
        self.executor_seed = executor_seed
        self.transpiler_seed = transpiler_seed

        self._provider: _BaseProvider = Backend._new_provider(provider=provider)
        self._executor: _BaseExecutor = Backend._new_executor(provider=self._provider,
                                                              executor=executor,
                                                              seed=executor_seed)
        self._transpiler: _BaseTranspiler = Backend._new_transpiler(provider=self._provider,
                                                                    seed=transpiler_seed)

    def __repr__(self):
        return (f'<Backend: provider={self.provider}, '
                f'executor={self.executor}, '
                f'executor_seed={self.executor_seed}, '
                f'transpiler_seed={self.transpiler_seed}>')

    @staticmethod
    def _new_provider(provider: Union[str, None] = None) -> _BaseProvider:
        if provider is None:
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
