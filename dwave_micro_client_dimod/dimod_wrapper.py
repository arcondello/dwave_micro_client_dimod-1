import dimod
import dwave_micro_client as micro

try:
    import numpy as np
    _numpy = True
except ImportError:  # pragma: no cover
    _numpy = False


class DWaveMicroClient(dimod.TemplateSampler):

    def __init__(self, solver_name=None, url=None, token=None, proxies=None, permissive_ssl=False):
        self.connection = connection = micro.Connection(url, token, proxies, permissive_ssl)
        self.solver = solver = connection.get_solver(solver_name)

    @dimod.decorators.ising(1, 2)
    def sample_ising(self, linear, quadratic, **kwargs):

        future = self.solver.sample_ising(linear, quadratic, **kwargs)

        # for now we just wait until the future is done and immediatly load into dimod response
        if _numpy:
            response = dimod.NumpySpinResponse()

            # get the samples in an array
            samples = np.asarray(future.samples)
            energies = np.asarray(future.energies)

            # finally load into the response
            response.add_samples_from_array(samples, energies)
        else:
            response = dimod.SpinResponse()

            # convert samples to a dict
            samples = (dict(enumerate(sample)) for sample in future.samples)
            energies = future.energies

            response.add_samples_from(samples, energies)

        # we will want to add other data from Future into the response.

        return response