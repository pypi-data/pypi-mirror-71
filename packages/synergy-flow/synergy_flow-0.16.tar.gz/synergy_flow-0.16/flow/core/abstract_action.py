__author__ = 'Bohdan Mushkevych'

from flow.core.abstract_cluster import AbstractCluster
from flow.core.execution_context import ContextDriven, get_action_logger, valid_context


class AbstractAction(ContextDriven):
    """ abstraction for action
        API sequence:
        1. *set_context*
        2. *do*
        3. *cleanup* """
    def __init__(self, action_name, log_tag=None, skip=False, **kwargs):
        super(AbstractAction, self).__init__()
        self.action_name = action_name
        self.log_tag = log_tag
        self.skip = skip
        self.step_name = None
        self.kwargs = {} if not kwargs else kwargs

    def __del__(self):
        self.cleanup()
        if self.logger:
            self.logger.info('Action {0} finished.'.format(self.action_name))

    def set_context(self, context, step_name=None, **kwargs):
        assert step_name is not None, 'step name must be passed to the action.set_context'
        self.step_name = step_name
        super(AbstractAction, self).set_context(context, **kwargs)

    def get_logger(self):
        fqlt = self.action_name if self.log_tag is None else '{0}.{1}'.format(self.action_name, self.log_tag)
        return get_action_logger(self.flow_name, self.step_name, fqlt, self.settings)

    def run(self, execution_cluster):
        """ abstract method implementing Action functionality
            :param execution_cluster: of type `AbstractCluster`
        """
        raise NotImplementedError('method *run* must be implemented by {0}'.format(self.__class__.__name__))

    @valid_context
    def do(self, execution_cluster):
        """ this method calls *run* in a skip-aware manner
            :return None or raise and exception
        """
        assert isinstance(execution_cluster, AbstractCluster)
        if self.skip:
            return
        self.run(execution_cluster)

    def cleanup(self):
        pass
