class CapabilityRegistry:
    def __init__(self):
        self._caps = {}

    def register(self, cap):
        self._caps[cap.name] = cap

    def get(self, name: str):
        if name not in self._caps:
            raise KeyError(f"Capability '{name}' not registered")
        return self._caps[name]
