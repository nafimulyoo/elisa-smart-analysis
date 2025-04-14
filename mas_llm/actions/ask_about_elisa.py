from metagpt.actions import Action
from metagpt.rag.engines import SimpleEngine
from metagpt.rag.schema import BM25RetrieverConfig
import os
from metagpt.logs import logger
from mas_llm.prompts.initial_prompt import ASK_ELISA_PROMPT

ELISA_DOC_PATH = "mas_llm/rag/data/elisa"

class AskAboutElisa(Action):

    name: str = "AskAboutElisa"

    async def run(self, instruction: str):
        files = os.listdir(ELISA_DOC_PATH)
        doc_paths = [os.path.join(ELISA_DOC_PATH, file) for file in files]

        engine = SimpleEngine.from_docs(
            input_files=doc_paths,
            retriever_configs=[BM25RetrieverConfig()]
        )

        prompt = ASK_ELISA_PROMPT.format(instruction=instruction)

        result = await engine.aquery(prompt)

        return result.response


    