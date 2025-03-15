from metagpt.actions import Action
from metagpt.rag.engines import SimpleEngine
from metagpt.rag.schema import FAISSRetrieverConfig, BM25RetrieverConfig, LLMRankerConfig
import os
from metagpt.logs import logger

ELISA_DOC_PATH = "mas_llm/rag/data/elisa"

class AskAboutElisa(Action):
    PROMPT_TEMPLATE: str = """
    Anda adalah agen yang sangat ahli dalam menjawab pertanyaan seputar use case ELISA ITB (Sistem Informasi Energi Listrik dan Air), nama lain ELISA adalah SiElis. Tugas Anda adalah memberikan informasi yang relevan dan akurat mengenai use case ELISA berdasarkan dokumen yang disediakan untuk anda.
    Jawablah pertanyaan pengguna berikut ini dengan memberikan informasi yang sesuai, tanpa menjelaskan sumber informasi atau memberikan informasi yang tidak relevan. Anggap juga bahwa anda adalah ELISA itu sendiri.
    Pertanyaan pengguna: {instruction}
    Jawaban anda:
    """

    name: str = "AskAboutElisa"

    async def run(self, instruction: str):
        files = os.listdir(ELISA_DOC_PATH)
        doc_paths = [os.path.join(ELISA_DOC_PATH, file) for file in files]

        engine = SimpleEngine.from_docs(
            input_files=doc_paths,
            retriever_configs=[BM25RetrieverConfig()]
        )

        prompt = self.PROMPT_TEMPLATE.format(instruction=instruction)

        result = await engine.aquery(prompt)

        return result.response


    