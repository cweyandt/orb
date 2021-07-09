import numpy as np
import ruptures as rpt

from .baseModels import OfflineOrbModel

MODEL_NAMES = ["pelt-rbf"]

class PeltRBF(OfflineOrbModel):
    model_name = "pelt-rbf"
    model_desc = "Pelt Search Method, RBF Segment Model"
    model = "rbf"
    penalty = 10
    results = None

    def analyze(self):
        if self.data is None:
            return "Error: No data"
        else:
            # TODO: retain timestamp data post-analysis
            points = np.array(self.data)

            algo = rpt.Pelt(model=self.model).fit(points)
            self.results = algo.predict(pen=self.penalty)
            return self.results

    def plot(self):
        if self.results is None:
            return "Error"
        else:
            rpt.display(self.data, self.results, figsize=(20, 8))
