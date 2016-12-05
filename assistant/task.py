# coding: utf-8


class Task(object):

    def __init__(self, domain=None, intent=None, parameters=None):
        self.domain = domain
        self.intent = intent

        self.parameters = {}
        if isinstance(parameters, dict):
            for k, v in parameters.iteritems():
                self.parameters[k] = v

    @property
    def get_parameters(self):
        if len(self.parameters) == 0:
            return None

        for k, v in self.parameters.iteritems():
            if self.parameters[k]['value'] is not None:
                return self.parameters
        return None
