class Trace:
    def __init__(self, composant: str, action: str, params: str, result: str):
        self.composant = composant
        self.action = action
        self.params = params
        self.result = result

    def __str__(self):
        return self.composant + " did " + self.action + " with " + self.params + " result " + self.result
