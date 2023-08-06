from __future__ import absolute_import, division, print_function

from vivarium.processes.derive_globals import AVOGADRO
from vivarium.core.process import Deriver
from vivarium.library.units import units


def get_default_state():
    mass = 1339 * units.fg  # wet mass in fg
    density = 1100 * units.g / units.L
    volume = mass / density
    mmol_to_counts = (AVOGADRO * volume).to('L/mmol')

    return {
        'global': {
            'volume': volume.to('fL'),
            'mmol_to_counts': mmol_to_counts}}


class DeriveCounts(Deriver):
    """
    Process for deriving counts from concentrations
    """
    defaults = {
        'concentration_keys': []}

    def __init__(self, initial_parameters=None):
        if initial_parameters is None:
            initial_parameters = {}

        self.initial_state = initial_parameters.get('initial_state', get_default_state())

        self.concentration_keys = self.or_default(
            initial_parameters, 'concentration_keys')

        ports = {
            'global': ['volume', 'mmol_to_counts'],
            'concentrations': self.concentration_keys,
            'counts': self.concentration_keys}

        parameters = {}
        parameters.update(initial_parameters)

        super(DeriveCounts, self).__init__(ports, parameters)

    def ports_schema(self):
        return {
            'global': {
                'volume': {
                    '_default': 0.0 * units.fL},
                'mmol_to_counts': {
                    '_default': 0.0 * units.L / units.mmol}},
            'counts': {
                molecule: {
                    '_divider': 'split',
                    '_updater': 'set'}
                for molecule in self.concentration_keys},
            'concentrations': {
                molecule: {
                    '_default': 0.0}
                for molecule in self.concentration_keys}}

    def next_update(self, timestep, states):
        mmol_to_counts = states['global']['mmol_to_counts'].to('L/mmol').magnitude
        concentrations = states['concentrations']

        counts = {}
        for molecule, concentration in concentrations.items():
            counts[molecule] = int(concentration * mmol_to_counts)

        return {
            'counts': counts}
