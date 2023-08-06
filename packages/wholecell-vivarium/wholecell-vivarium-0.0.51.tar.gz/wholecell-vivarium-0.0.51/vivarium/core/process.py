from __future__ import absolute_import, division, print_function


class Process(object):
    def __init__(self, ports, parameters=None):
        ''' Declare what ports this process expects. '''

        self.ports = ports
        self.parameters = parameters or {}
        self.time_step = parameters.get('time_step', 1.0)

    def local_timestep(self):
        '''
        Returns the favored timestep for this process.
        Meant to be overridden in subclasses, unless 1.0 is a happy value.
        '''
        return self.time_step

    def default_state(self):
        '''
        ports_schema returns a dictionary that declares which states are expected by the processes,
        and how each state will behave.

        state keys can be assigned properties through schema_keys declared in Store:
            '_default'
            '_updater'
            '_divider'
            '_value'
            '_properties'
            '_emit'
            '_serializer'
        '''

        schema = self.ports_schema()
        state = {}
        for port, states in schema.items():
            for key, value in states.items():
                if '_default' in value:
                    if port not in state:
                        state[port] = {}
                    state[port][key] = value['_default']
        return state

    def is_deriver(self):
        return False

    def derivers(self):
        return {}

    def pull_data(self):
        return {}

    def ports_schema(self):
        return {}

    def or_default(self, parameters, key):
        return parameters.get(key, self.defaults[key])

    def parameters_for(self, parameters, key):
        ''' Return key in parameters or from self.default_parameters if not present. '''

        return parameters.get(key, self.default_parameters[key])

    def derive_defaults(self, parameters, original_key, derived_key, f):
        present = self.parameters_for(parameters, original_key)
        self.default_parameters[derived_key] = f(present)
        return self.default_parameters[derived_key]

    def next_update(self, timestep, states):
        '''
        Find the next update given the current states this process cares about.

        This is the main function a new process would override.'''

        return {
            port: {}
            for port, values in self.ports.items()}


class Deriver(Process):
    def is_deriver(self):
        return True
