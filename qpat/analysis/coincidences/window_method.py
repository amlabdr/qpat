from qpat.analysis.coincidences.base import CoincidenceModel

class WindowCoincidenceModel(CoincidenceModel):
    def __init__(self, window: float):
        self.window = window

    def compute(self, detection_events):
        # your existing logic
        coincidences = 0
        return coincidences

    def rate(self, coincidences, duration):
        return 1