from api_model import InitialPromptHandlerResult
import re
from metagpt.actions import Action
import json

from metagpt.rag.engines import SimpleEngine
from metagpt.rag.schema import FAISSRetrieverConfig, BM25RetrieverConfig, LLMRankerConfig

DOC_PATH = "mas_llm/rag/data/elisa/data_availability.txt"

class AskDataAvailability(Action):
    PROMPT_TEMPLATE: str = """
    Anda adalah agen yang berguna untuk mengecek ketersediaan data yang diperlukan untuk analisis. Tugas Anda adalah memvalidasi apakah data yang diperlukan untuk menjawab prompt pengguna sudah tersedia atau tidak.
    format JSON yang diharapkan:
    - Jika data sudah tersedia:
        {{
            "type": "Data Available",
            "message": "[Buat pesan yang sesuai untuk memberi tahu pengguna bahwa data sudah tersedia]"
        }}
    - Jika data belum tersedia:
        {{
            "type": "Data Not Available",
            "message": "[Buat pesan yang sesuai untuk memberi tahu pengguna bahwa data belum tersedia]"
        }}
    Kembalikan ```json json_yang_anda_tulis```, tanpa tambahan teks atau penjelasan lainnya.
    Prompt pengguna: {instruction}
    json anda:
    """

    name: str = "AskDataAvailability"

    async def run(self, instruction: str):
        prompt = self.PROMPT_TEMPLATE.format(instruction=instruction)

        engine = SimpleEngine.from_docs(
            input_files=[DOC_PATH],
            retriever_configs=[BM25RetrieverConfig()]
        )

        response = await engine.aquery(prompt)
        
        result = self.parse_json(response.response)

        return result

    @staticmethod
    def parse_json(response):
        pattern = r"```json(.*)```"
        match = re.search(pattern, response, re.DOTALL)
        
        json_string = match.group(1) if match else response

        json_object = json.loads(json_string)

        result = InitialPromptHandlerResult(
            type=json_object.get("type"),
            message=json_object.get("message")
        )

        return result
    