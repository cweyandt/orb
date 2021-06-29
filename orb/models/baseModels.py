import abc

from pydantic import BaseModel


class _OrbModel(BaseModel, abc.ABC):
    model_name: str = None
    model_desc: str = None
    _data: None

    def describe(self):
        '''Return model configuration'''
        return self

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        self._data = data

    @abc.abstractmethod
    def plot(self, *data):
        '''Custom plot function'''
        pass


class OfflineOrbModel(_OrbModel):

    @abc.abstractmethod
    def analyze(self, *data):
        '''Analyze past data'''
        pass


class OnlineOrbModel(_OrbModel):

    @abc.abstractmethod
    def analyze(self):
        '''Analyze streaming input'''
        pass


class PredictOrbModel(_OrbModel):

    @abc.abstractmethod
    def predict(self):
        '''Generate prediction'''
        pass
