from ..linear_quadratic import LinearQuadratic
from ...primitives import DoseArray, DoseType, Dose
import numpy as np


class TcpDensity():
    def __init__(self, density: float, alpha: float) -> None:
        self._validate_positive_or_throw_exception(density, "density must be positive number")
        self._validate_positive_or_throw_exception(alpha, "alpha must be positive number")
        self.density = density
        self.alpha = alpha


    def _validate_positive_or_throw_exception(self, value, message):
        if value < 0:
            raise ValueError(message)

    def response_from_pysical_dose(self, dose_array_in_physical_dose: DoseArray,
                                   volume_array,
                                   ab_ratio: Dose,
                                   nfx: int):
        lqmodel = LinearQuadratic(ab_ratio=ab_ratio, nfx=nfx)
        eqd0_dose_array = lqmodel.eqd0(dose_array_in_physical_dose)
        tcp_voxels = np.exp(- self.density * np.array(volume_array) * np.exp(-self.alpha * eqd0_dose_array.data))
        return np.prod(tcp_voxels)
