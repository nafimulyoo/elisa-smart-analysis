from api_model import InitialPromptHandlerResult
import re
from metagpt.actions import Action
import json

class AskDataAvailability(Action):
    PROMPT_TEMPLATE: str = """
    Anda adalah agen yang bertugas memvalidasi dan mengklasifikasikan prompt pengguna berdasarkan relevansinya dengan use case ELISA. Tugas Anda adalah memastikan bahwa prompt tersebut sesuai dengan kategori berikut:

    1. **Unrelevant**: Prompt tidak memiliki hubungan dengan use case ELISA.
    2. **No Data**: Prompt tidak dapat dijawab karena kurangnya informasi atau data.
    3. **Basic Knowledge**: Prompt berkaitan dengan informasi dasar mengenai ELISA, ITB, atau penggunaan energi listrik secara umum.
    4. **Basic Data Analysis**: Prompt meminta analisis data sederhana, seperti perhitungan dasar atau visualisasi data.
    5. **Advanced Data Analysis**: Prompt memerlukan analisis yang lebih kompleks, termasuk teknik statistik atau pemodelan data yang lebih mendalam.

    Setelah mengklasifikasikan prompt, berikan respons dalam format JSON dengan struktur berikut:

    - Untuk prompt yang tidak relevan:
        {{
            "type": "Unrelevant",
            "message": "[Buat pesan yang sesuai untuk memberi tahu pengguna bahwa prompt tidak relevan]"
        }}

    - Untuk prompt yang tidak dapat diproses karena kurangnya data:
        {{
            "type": "No Data",
            "message": "[Buat pesan yang sesuai untuk memberi tahu pengguna bahwa data tidak cukup]"
        }}

    - Untuk prompt yang berkaitan dengan pengetahuan umum:
        {{
            "type": "Basic Knowledge",
            "message": "[Buat pesan yang sesuai untuk memberikan informasi dasar]"
        }}

    - Untuk prompt yang meminta analisis data sederhana:
        {{
            "type": "Basic Analysis",
            "message": "[Buat pesan yang sesuai untuk memberi tahu pengguna bahwa analisis sederhana sedang diproses]"
        }}

    - Untuk prompt yang memerlukan analisis yang lebih kompleks:
        {{
            "type": "Advanced Analysis",
            "message": "[Buat pesan yang sesuai untuk memberi tahu pengguna bahwa analisis kompleks sedang diproses]"
        }}

    Kembalikan  ```json json_yang_anda_tulis ```, tanpa tambahan teks atau penjelasan lainnya.

    Prompt pengguna: {instruction}

    json anda:
    """

    name: str = "RespondInitialPrompt"

    async def run(self, instruction: str):
        prompt = self.PROMPT_TEMPLATE.format(instruction=instruction)

        response = await self._aask(prompt)

        result = self.parse_json(response)

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
    