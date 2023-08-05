

class ModelMetrics():
    '''

    '''

    def __init__(self, client, modelId=None, modelVersion=None, metrics=None, metricNames=None):
        self.client = client
        self.id = None
        self.model_id = modelId
        self.model_version = modelVersion
        self.metrics = metrics
        self.metric_names = metricNames

    def __repr__(self):
        return f"ModelMetrics(model_id={repr(self.model_id)}, model_version={repr(self.model_version)}, metrics={repr(self.metrics)}, metric_names={repr(self.metric_names)})"

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.id == other.id

    def to_dict(self):
        return {'model_id': self.model_id, 'model_version': self.model_version, 'metrics': self.metrics, 'metric_names': self.metric_names}
