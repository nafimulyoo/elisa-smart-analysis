from api_model import InitialPromptHandlerResult
import re
from metagpt.actions import Action
import json

class RespondInitialPrompt(Action):
    PROMPT_TEMPLATE: str = """
    Anda adalah agen yang sangat ahli dalam menjawab pertanyaan seputar use case ELISA ITB (Sistem Informasi Energi Listrik dan Air), nama lain ELISA adalah SiElis.
    Saat ini, anda bertugas memvalidasi dan mengklasifikasikan prompt pengguna berdasarkan relevansinya dengan use case ELISA. Tugas Anda adalah memastikan bahwa prompt tersebut sesuai dengan kategori berikut:

    1. **Unrelevant**: Prompt tidak memiliki hubungan dengan use case ELISA.
    2. **Basic Knowledge**: Prompt berkaitan dengan informasi dasar mengenai ELISA dan ITB tanpa memerlukan data analisis, walauun sederhana seperti perhitungan dan perbandingan dasar.
    3. **Basic Analysis**: Prompt meminta analisis data sederhana, seperti pemakaian total, perhitungan maksimum, minimum, TANPA diperlukan prediksi, forcasting dan rekomendasi. ini harus bisa dikode dalan satu cell python notebook. jika anda tidak yakin, lebih baik klasifikasikan sebagai Advanced Data Analysis.
    4. **Advanced Analysis**: Prompt memerlukan analisis data kompleks, termasuk perkiraan pemakaian periode berikutnya, prediksi, forecasting, dan rekomendasi, yang memerlukan beberapa cell python notebook.

    Setelah mengklasifikasikan prompt, berikan respons dalam format JSON dengan struktur berikut:

    - Untuk prompt yang tidak relevan:
        {{
            "type": "Unrelevant",
            "message": "[Buat pesan yang sesuai untuk memberi tahu pengguna bahwa prompt tidak relevan]"
        }}

    - Untuk prompt yang berkaitan dengan informasi dasar mengenai ELISA, ITB, atau penggunaan energi listrik secara umum:
        {{
            "type": "Basic Knowledge",
            "message": "[kosongkan]"
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
    