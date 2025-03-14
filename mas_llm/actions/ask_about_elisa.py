from metagpt.actions import Action
from metagpt.rag.engines import SimpleEngine
from metagpt.rag.schema import FAISSRetrieverConfig, BM25RetrieverConfig, LLMRankerConfig

DOC_PATH = "mas_llm/data/elisa.txt"

class AskAboutElisa(Action):
    PROMPT_TEMPLATE: str = """
    Anda adalah agen yang sangat ahli dalam menjawab pertanyaan seputar use case ELISA. Tugas Anda adalah memberikan informasi yang relevan dan akurat mengenai use case ELISA.
    Jawablah pertanyaan pengguna berikut ini dengan memberikan informasi yang sesuai.
    Pertanyaan pengguna: {instruction}
    Jawaban anda:
    """

    name: str = "AskAboutElisa"

    async def run(self, instruction: str):
        engine = SimpleEngine.from_docs(
            input_files=[DOC_PATH],
            retriever_configs=[FAISSRetrieverConfig(), BM25RetrieverConfig()],
            ranker_configs=[LLMRankerConfig()]
        )

        prompt = self.PROMPT_TEMPLATE.format(instruction=instruction)

        result = await engine.aquery(prompt)

        return result


    