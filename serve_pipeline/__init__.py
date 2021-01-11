import random

from ray import serve

class GenerateEmbedding:
    def __init__(self):
        # Here you would load your actual model.
        self.model = random.random

    def __call__(self, request):
        return self.model()

class Classify:
    def __init__(self):
        # Here you would load your actual model.
        self.model = random.random

    @serve.accept_batch
    def __call__(self, request):
        return self.model()

class ModelPipeline:
    def __init__(self, models):
        client = serve.connect()
        self.model_handles = [client.get_handle(model, sync=False) for model in models]

    async def __call__(self, request):
        prev_result = request
        for handle in self.model_handles:
            prev_result = await handle.remote(prev_result)

        return await prev_result
