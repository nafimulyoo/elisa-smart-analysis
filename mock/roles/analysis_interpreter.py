class AnalysisInterpreter:
    def __init__(self, context, model):
        self.model = model
        self.context = context

    def run(self, prompt):
        return "Prompt valid dan relevan dengan use case ELISA."