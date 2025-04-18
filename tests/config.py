TEST_URL = "http://localhost:8000"

# TEST ANALYSIS CONFIG
TEST_FACULTY = "FTI"  
TEST_BUILDING = "LABTEK VI"  
TEST_FLOOR = ""  
TEST_PAST_DATE = "2025-03-01" 
TEST_PAST_DATE_END_HEATMAP = "2025-03-07"  
TEST_PAST_MONTH = "2025-02"

ASK_TEST_CASES_WEB = [
    # ["What is ELISA", "Basic Knowledge"],
    # ["What is the purpose of ELISA", "Basic Knowledge"],
    # ["Bagaimana cara ELISA mengidentifikasi pemborosan energi di ITB?", "Basic Knowledge"],
    # ["Fitur apa saja yang tersedia di dashboard ELISA untuk memantau konsumsi energi?", "Basic Knowledge"],
    # ["Bagaimana ELISA membantu ITB dalam membandingkan penggunaan energi antar fakultas?", "Basic Knowledge"],
    # ["Teknologi apa yang digunakan ELISA untuk mengumpulkan data konsumsi listrik secara real-time?", "Basic Knowledge"],
    # ["Apa tujuan utama dari sistem ELISA dalam memantau konsumsi energi dan air di ITB?", "Basic Knowledge"],
    # ["Bagaimana arsitektur SGAM (Smart Grid Architectural Model) digunakan dalam pengembangan ELISA?", "Basic Knowledge"],
    # ["Fitur apa saja yang tersedia di dashboard ELISA untuk membandingkan penggunaan energi antar fakultas?", "Basic Knowledge"],
    # ["Bagaimana data dari smart meter dikumpulkan dan diproses dalam platform Big Data ELISA?", "Basic Knowledge"],
    # ["Apa saja indikator kinerja (seperti IKE dan EnPI) yang digunakan ELISA untuk mengevaluasi efisiensi energi?", "Basic Knowledge"],
    # ["What is the weather like today", "Unrelevant"],
    # ["Tell me a joke", "Unrelevant"],
    # ["How are you doing today", "Unrelevant"],
    # ["Plot ITB Jakarta usage last month", "Data Not Available"],
    # ["Impact of weather on energy use (correlation data)", "Data Not Available"],
    # ["Plot Masjid Salman usage last month", "Data Not Available"],
    # ["Total ITB Jakarta usage over the past year", "Data Not Available"],
    # ["Plot last hour usage of Fakultas Kedokteran", "Basic Analysis"],
    # ["What is the usage trend of FSRD in the last 3 months", "Basic Analysis"],
    # ["Compare SF and FMIPA usage trends", "Basic Analysis"],
    # ["Total ITB usage over the past month", "Basic Analysis"],
    # ["Total ITB usage over the past year", "Basic Analysis"],
    # ["Top 3 buildings with highest usage last year", "Basic Analysis"],


    ["Lowest 3 faculty usage in the last 3 months", "Basic Analysis"],
    ["Top 3 faculty usage in the last 3 months", "Basic Analysis"],
    ["FTI usage in the last 3 months", "Basic Analysis"],
    ["Plot last hour usage of FSRD", "Basic Analysis"],
    ["What is the usage trend of FSRD in the last 3 months", "Basic Analysis"],
    ["Compare SF and FMIPA usage trends", "Basic Analysis"],
    ["Total ITB usage over the past month", "Basic Analysis"],
    ["Total ITB usage over the past year", "Basic Analysis"],
    ["FTI usage in the last 3 months", "Basic Analysis"],
    ["Plot last hour usage of FSRD", "Basic Analysis"],
    ["Lowest 3 faculty usage in the last 3 months", "Basic Analysis"],
    ["Top 3 buildings (not faculty) with highest usage last year", "Basic Analysis"],
    ["Plot FKK usage last 3 months", "Basic Analysis"],
        ["Lowest 3 faculty usage in the last 3 months", "Basic Analysis"],
    ["Top 3 faculty usage in the last 3 months", "Basic Analysis"],
    ["FTI usage in the last 3 months", "Basic Analysis"],
    ["Plot last hour usage of FSRD", "Basic Analysis"],
    ["What is the usage trend of FSRD in the last 3 months", "Basic Analysis"],
    ["Compare SF and FMIPA usage trends", "Basic Analysis"],
    ["Total ITB usage over the past month", "Basic Analysis"],
    ["Total ITB usage over the past year", "Basic Analysis"],
    ["FTI usage in the last 3 months", "Basic Analysis"],
    ["Plot last hour usage of FSRD", "Basic Analysis"],
    ["Lowest 3 faculty usage in the last 3 months", "Basic Analysis"],
    ["Top 3 buildings (not faculty) with highest usage last year", "Basic Analysis"],
    ["Plot FKK usage last 3 months", "Basic Analysis"],
        ["Lowest 3 faculty usage in the last 3 months", "Basic Analysis"],
    ["Top 3 faculty usage in the last 3 months", "Basic Analysis"],
    ["FTI usage in the last 3 months", "Basic Analysis"],
    ["Plot last hour usage of FSRD", "Basic Analysis"],
    ["What is the usage trend of FSRD in the last 3 months", "Basic Analysis"],
    ["Compare SF and FMIPA usage trends", "Basic Analysis"],
    ["Total ITB usage over the past month", "Basic Analysis"],
    ["Total ITB usage over the past year", "Basic Analysis"],
    ["FTI usage in the last 3 months", "Basic Analysis"],
    ["Plot last hour usage of FSRD", "Basic Analysis"],
    ["Lowest 3 faculty usage in the last 3 months", "Basic Analysis"],
    ["Top 3 buildings (not faculty) with highest usage last year", "Basic Analysis"],
    ["Plot FKK usage last 3 months", "Basic Analysis"],




    # ["Forecast CC Barat usage during holidays", "Advanced Analysis"],
    # ["Predict Labtek VI peak hours next week", "Advanced Analysis"],
    # ["Average Engineering Physics Building usage during summer", "Basic Analysis"],
    # ["Compare STEI usage: weekdays vs weekends", "Basic Analysis"],
    # ["Forecast ITB usage for next academic year", "Advanced Analysis"],
    # ["Labtek III usage trends last 3 semesters", "Advanced Analysis"],
    # ["Predict FTI usage during next major event", "Advanced Analysis"],
    # ["Forecast Labtek VII usage during winter break", "Advanced Analysis"],
    # ["Cluster ITB buildings based on usage patterns", "Advanced Analysis"],
    # ["Identify usage clusters among faculties", "Advanced Analysis"],
    # ["Find anomaly clusters in weekend usage", "Advanced Analysis"],
    # ["Cluster departments based on energy efficiency", "Advanced Analysis"],


    # TESTING
        ["Lowest 3 faculty usage in the last 3 months", "Basic Analysis"],
    ["Top 3 faculty usage in the last 3 months", "Basic Analysis"],
    ["FTI usage in the last 3 months", "Basic Analysis"],
    ["Plot last hour usage of FSRD", "Basic Analysis"],
    ["What is the usage trend of FSRD in the last 3 months", "Basic Analysis"],
    ["Compare SF and FMIPA usage trends", "Basic Analysis"],
    ["Total ITB usage over the past month", "Basic Analysis"],
    ["Total ITB usage over the past year", "Basic Analysis"],
    ["FTI usage in the last 3 months", "Basic Analysis"],
    ["Plot last hour usage of FSRD", "Basic Analysis"],
    ["Lowest 3 faculty usage in the last 3 months", "Basic Analysis"],
    ["Top 3 buildings (not faculty) with highest usage last year", "Basic Analysis"],
    ["Plot FKK usage last 3 months", "Basic Analysis"],
        ["Lowest 3 faculty usage in the last 3 months", "Basic Analysis"],
    ["Top 3 faculty usage in the last 3 months", "Basic Analysis"],
    ["FTI usage in the last 3 months", "Basic Analysis"],
    ["Plot last hour usage of FSRD", "Basic Analysis"],
    ["What is the usage trend of FSRD in the last 3 months", "Basic Analysis"],
    ["Compare SF and FMIPA usage trends", "Basic Analysis"],
    ["Total ITB usage over the past month", "Basic Analysis"],
    ["Total ITB usage over the past year", "Basic Analysis"],
    ["FTI usage in the last 3 months", "Basic Analysis"],
    ["Plot last hour usage of FSRD", "Basic Analysis"],
    ["Lowest 3 faculty usage in the last 3 months", "Basic Analysis"],
    ["Top 3 buildings (not faculty) with highest usage last year", "Basic Analysis"],
    ["Plot FKK usage last 3 months", "Basic Analysis"],
        ["Lowest 3 faculty usage in the last 3 months", "Basic Analysis"],
    ["Top 3 faculty usage in the last 3 months", "Basic Analysis"],
    ["FTI usage in the last 3 months", "Basic Analysis"],
    ["Plot last hour usage of FSRD", "Basic Analysis"],
    ["What is the usage trend of FSRD in the last 3 months", "Basic Analysis"],
    ["Compare SF and FMIPA usage trends", "Basic Analysis"],
    ["Total ITB usage over the past month", "Basic Analysis"],
    ["Total ITB usage over the past year", "Basic Analysis"],
    ["FTI usage in the last 3 months", "Basic Analysis"],
    ["Plot last hour usage of FSRD", "Basic Analysis"],
    ["Lowest 3 faculty usage in the last 3 months", "Basic Analysis"],
    ["Top 3 buildings (not faculty) with highest usage last year", "Basic Analysis"],
    ["Plot FKK usage last 3 months", "Basic Analysis"],
        ["Lowest 3 faculty usage in the last 3 months", "Basic Analysis"],
    ["Top 3 faculty usage in the last 3 months", "Basic Analysis"],
    ["FTI usage in the last 3 months", "Basic Analysis"],
    ["Plot last hour usage of FSRD", "Basic Analysis"],
    ["What is the usage trend of FSRD in the last 3 months", "Basic Analysis"],
    ["Compare SF and FMIPA usage trends", "Basic Analysis"],
    ["Total ITB usage over the past month", "Basic Analysis"],
    ["Total ITB usage over the past year", "Basic Analysis"],
    ["FTI usage in the last 3 months", "Basic Analysis"],
    ["Plot last hour usage of FSRD", "Basic Analysis"],
    ["Lowest 3 faculty usage in the last 3 months", "Basic Analysis"],
    ["Top 3 buildings (not faculty) with highest usage last year", "Basic Analysis"],
    ["Plot FKK usage last 3 months", "Basic Analysis"],
        ["Lowest 3 faculty usage in the last 3 months", "Basic Analysis"],
    ["Top 3 faculty usage in the last 3 months", "Basic Analysis"],
    ["FTI usage in the last 3 months", "Basic Analysis"],
    ["Plot last hour usage of FSRD", "Basic Analysis"],
    ["What is the usage trend of FSRD in the last 3 months", "Basic Analysis"],
    ["Compare SF and FMIPA usage trends", "Basic Analysis"],
    ["Total ITB usage over the past month", "Basic Analysis"],
    ["Total ITB usage over the past year", "Basic Analysis"],
    ["FTI usage in the last 3 months", "Basic Analysis"],
    ["Plot last hour usage of FSRD", "Basic Analysis"],
    ["Lowest 3 faculty usage in the last 3 months", "Basic Analysis"],
    ["Top 3 buildings (not faculty) with highest usage last year", "Basic Analysis"],
    ["Plot FKK usage last 3 months", "Basic Analysis"],
        ["Lowest 3 faculty usage in the last 3 months", "Basic Analysis"],
    ["Top 3 faculty usage in the last 3 months", "Basic Analysis"],
    ["FTI usage in the last 3 months", "Basic Analysis"],
    ["Plot last hour usage of FSRD", "Basic Analysis"],
    ["What is the usage trend of FSRD in the last 3 months", "Basic Analysis"],
    ["Compare SF and FMIPA usage trends", "Basic Analysis"],
    ["Total ITB usage over the past month", "Basic Analysis"],
    ["Total ITB usage over the past year", "Basic Analysis"],
    ["FTI usage in the last 3 months", "Basic Analysis"],
    ["Plot last hour usage of FSRD", "Basic Analysis"],
    ["Lowest 3 faculty usage in the last 3 months", "Basic Analysis"],
    ["Top 3 buildings (not faculty) with highest usage last year", "Basic Analysis"],
    ["Plot FKK usage last 3 months", "Basic Analysis"],
        ["Lowest 3 faculty usage in the last 3 months", "Basic Analysis"],
    ["Top 3 faculty usage in the last 3 months", "Basic Analysis"],
    ["FTI usage in the last 3 months", "Basic Analysis"],
    ["Plot last hour usage of FSRD", "Basic Analysis"],
    ["What is the usage trend of FSRD in the last 3 months", "Basic Analysis"],
    ["Compare SF and FMIPA usage trends", "Basic Analysis"],
    ["Total ITB usage over the past month", "Basic Analysis"],
    ["Total ITB usage over the past year", "Basic Analysis"],
    ["FTI usage in the last 3 months", "Basic Analysis"],
    ["Plot last hour usage of FSRD", "Basic Analysis"],
    ["Lowest 3 faculty usage in the last 3 months", "Basic Analysis"],
    ["Top 3 buildings (not faculty) with highest usage last year", "Basic Analysis"],
    ["Plot FKK usage last 3 months", "Basic Analysis"],
        ["Lowest 3 faculty usage in the last 3 months", "Basic Analysis"],
    ["Top 3 faculty usage in the last 3 months", "Basic Analysis"],
    ["FTI usage in the last 3 months", "Basic Analysis"],
    ["Plot last hour usage of FSRD", "Basic Analysis"],
    ["What is the usage trend of FSRD in the last 3 months", "Basic Analysis"],
    ["Compare SF and FMIPA usage trends", "Basic Analysis"],
    ["Total ITB usage over the past month", "Basic Analysis"],
    ["Total ITB usage over the past year", "Basic Analysis"],
    ["FTI usage in the last 3 months", "Basic Analysis"],
    ["Plot last hour usage of FSRD", "Basic Analysis"],
    ["Lowest 3 faculty usage in the last 3 months", "Basic Analysis"],
    ["Top 3 buildings (not faculty) with highest usage last year", "Basic Analysis"],
    ["Plot FKK usage last 3 months", "Basic Analysis"],
        ["Lowest 3 faculty usage in the last 3 months", "Basic Analysis"],
    ["Top 3 faculty usage in the last 3 months", "Basic Analysis"],
    ["FTI usage in the last 3 months", "Basic Analysis"],
    ["Plot last hour usage of FSRD", "Basic Analysis"],
    ["What is the usage trend of FSRD in the last 3 months", "Basic Analysis"],
    ["Compare SF and FMIPA usage trends", "Basic Analysis"],
    ["Total ITB usage over the past month", "Basic Analysis"],
    ["Total ITB usage over the past year", "Basic Analysis"],
    ["FTI usage in the last 3 months", "Basic Analysis"],
    ["Plot last hour usage of FSRD", "Basic Analysis"],
    ["Lowest 3 faculty usage in the last 3 months", "Basic Analysis"],
    ["Top 3 buildings (not faculty) with highest usage last year", "Basic Analysis"],
    ["Plot FKK usage last 3 months", "Basic Analysis"],
        ["Lowest 3 faculty usage in the last 3 months", "Basic Analysis"],
    ["Top 3 faculty usage in the last 3 months", "Basic Analysis"],
    ["FTI usage in the last 3 months", "Basic Analysis"],
    ["Plot last hour usage of FSRD", "Basic Analysis"],
    ["What is the usage trend of FSRD in the last 3 months", "Basic Analysis"],
    ["Compare SF and FMIPA usage trends", "Basic Analysis"],
    ["Total ITB usage over the past month", "Basic Analysis"],
    ["Total ITB usage over the past year", "Basic Analysis"],
    ["FTI usage in the last 3 months", "Basic Analysis"],
    ["Plot last hour usage of FSRD", "Basic Analysis"],
    ["Lowest 3 faculty usage in the last 3 months", "Basic Analysis"],
    ["Top 3 buildings (not faculty) with highest usage last year", "Basic Analysis"],
    ["Plot FKK usage last 3 months", "Basic Analysis"],
        ["Lowest 3 faculty usage in the last 3 months", "Basic Analysis"],
    ["Top 3 faculty usage in the last 3 months", "Basic Analysis"],
    ["FTI usage in the last 3 months", "Basic Analysis"],
    ["Plot last hour usage of FSRD", "Basic Analysis"],
    ["What is the usage trend of FSRD in the last 3 months", "Basic Analysis"],
    ["Compare SF and FMIPA usage trends", "Basic Analysis"],
    ["Total ITB usage over the past month", "Basic Analysis"],
    ["Total ITB usage over the past year", "Basic Analysis"],
    ["FTI usage in the last 3 months", "Basic Analysis"],
    ["Plot last hour usage of FSRD", "Basic Analysis"],
    ["Lowest 3 faculty usage in the last 3 months", "Basic Analysis"],
    ["Top 3 buildings (not faculty) with highest usage last year", "Basic Analysis"],
    ["Plot FKK usage last 3 months", "Basic Analysis"],
        ["Lowest 3 faculty usage in the last 3 months", "Basic Analysis"],
    ["Top 3 faculty usage in the last 3 months", "Basic Analysis"],
    ["FTI usage in the last 3 months", "Basic Analysis"],
    ["Plot last hour usage of FSRD", "Basic Analysis"],
    ["What is the usage trend of FSRD in the last 3 months", "Basic Analysis"],
    ["Compare SF and FMIPA usage trends", "Basic Analysis"],
    ["Total ITB usage over the past month", "Basic Analysis"],
    ["Total ITB usage over the past year", "Basic Analysis"],
    ["FTI usage in the last 3 months", "Basic Analysis"],
    ["Plot last hour usage of FSRD", "Basic Analysis"],
    ["Lowest 3 faculty usage in the last 3 months", "Basic Analysis"],
    ["Top 3 buildings (not faculty) with highest usage last year", "Basic Analysis"],
    ["Plot FKK usage last 3 months", "Basic Analysis"],
        ["Lowest 3 faculty usage in the last 3 months", "Basic Analysis"],
    ["Top 3 faculty usage in the last 3 months", "Basic Analysis"],
    ["FTI usage in the last 3 months", "Basic Analysis"],
    ["Plot last hour usage of FSRD", "Basic Analysis"],
    ["What is the usage trend of FSRD in the last 3 months", "Basic Analysis"],
    ["Compare SF and FMIPA usage trends", "Basic Analysis"],
    ["Total ITB usage over the past month", "Basic Analysis"],
    ["Total ITB usage over the past year", "Basic Analysis"],
    ["FTI usage in the last 3 months", "Basic Analysis"],
    ["Plot last hour usage of FSRD", "Basic Analysis"],
    ["Lowest 3 faculty usage in the last 3 months", "Basic Analysis"],
    ["Top 3 buildings (not faculty) with highest usage last year", "Basic Analysis"],
    ["Plot FKK usage last 3 months", "Basic Analysis"],
        ["Lowest 3 faculty usage in the last 3 months", "Basic Analysis"],
    ["Top 3 faculty usage in the last 3 months", "Basic Analysis"],
    ["FTI usage in the last 3 months", "Basic Analysis"],
    ["Plot last hour usage of FSRD", "Basic Analysis"],
    ["What is the usage trend of FSRD in the last 3 months", "Basic Analysis"],
    ["Compare SF and FMIPA usage trends", "Basic Analysis"],
    ["Total ITB usage over the past month", "Basic Analysis"],
    ["Total ITB usage over the past year", "Basic Analysis"],
    ["FTI usage in the last 3 months", "Basic Analysis"],
    ["Plot last hour usage of FSRD", "Basic Analysis"],
    ["Lowest 3 faculty usage in the last 3 months", "Basic Analysis"],
    ["Top 3 buildings (not faculty) with highest usage last year", "Basic Analysis"],
    ["Plot FKK usage last 3 months", "Basic Analysis"],
        ["Lowest 3 faculty usage in the last 3 months", "Basic Analysis"],
    ["Top 3 faculty usage in the last 3 months", "Basic Analysis"],
    ["FTI usage in the last 3 months", "Basic Analysis"],
    ["Plot last hour usage of FSRD", "Basic Analysis"],
    ["What is the usage trend of FSRD in the last 3 months", "Basic Analysis"],
    ["Compare SF and FMIPA usage trends", "Basic Analysis"],
    ["Total ITB usage over the past month", "Basic Analysis"],
    ["Total ITB usage over the past year", "Basic Analysis"],
    ["FTI usage in the last 3 months", "Basic Analysis"],
    ["Plot last hour usage of FSRD", "Basic Analysis"],
    ["Lowest 3 faculty usage in the last 3 months", "Basic Analysis"],
    ["Top 3 buildings (not faculty) with highest usage last year", "Basic Analysis"],
    ["Plot FKK usage last 3 months", "Basic Analysis"],    ["Lowest 3 faculty usage in the last 3 months", "Basic Analysis"],
    ["Top 3 faculty usage in the last 3 months", "Basic Analysis"],
    ["FTI usage in the last 3 months", "Basic Analysis"],
    ["Plot last hour usage of FSRD", "Basic Analysis"],
    ["What is the usage trend of FSRD in the last 3 months", "Basic Analysis"],
    ["Compare SF and FMIPA usage trends", "Basic Analysis"],
    ["Total ITB usage over the past month", "Basic Analysis"],
    ["Total ITB usage over the past year", "Basic Analysis"],
    ["FTI usage in the last 3 months", "Basic Analysis"],
    ["Plot last hour usage of FSRD", "Basic Analysis"],
    ["Lowest 3 faculty usage in the last 3 months", "Basic Analysis"],
    ["Top 3 buildings (not faculty) with highest usage last year", "Basic Analysis"],
    ["Plot FKK usage last 3 months", "Basic Analysis"],
        ["Lowest 3 faculty usage in the last 3 months", "Basic Analysis"],
    ["Top 3 faculty usage in the last 3 months", "Basic Analysis"],
    ["FTI usage in the last 3 months", "Basic Analysis"],
    ["Plot last hour usage of FSRD", "Basic Analysis"],
    ["What is the usage trend of FSRD in the last 3 months", "Basic Analysis"],
    ["Compare SF and FMIPA usage trends", "Basic Analysis"],
    ["Total ITB usage over the past month", "Basic Analysis"],
    ["Total ITB usage over the past year", "Basic Analysis"],
    ["FTI usage in the last 3 months", "Basic Analysis"],
    ["Plot last hour usage of FSRD", "Basic Analysis"],
    ["Lowest 3 faculty usage in the last 3 months", "Basic Analysis"],
    ["Top 3 buildings (not faculty) with highest usage last year", "Basic Analysis"],
    ["Plot FKK usage last 3 months", "Basic Analysis"],
        ["Lowest 3 faculty usage in the last 3 months", "Basic Analysis"],
    ["Top 3 faculty usage in the last 3 months", "Basic Analysis"],
    ["FTI usage in the last 3 months", "Basic Analysis"],
    ["Plot last hour usage of FSRD", "Basic Analysis"],
    ["What is the usage trend of FSRD in the last 3 months", "Basic Analysis"],
    ["Compare SF and FMIPA usage trends", "Basic Analysis"],
    ["Total ITB usage over the past month", "Basic Analysis"],
    ["Total ITB usage over the past year", "Basic Analysis"],
    ["FTI usage in the last 3 months", "Basic Analysis"],
    ["Plot last hour usage of FSRD", "Basic Analysis"],
    ["Lowest 3 faculty usage in the last 3 months", "Basic Analysis"],
    ["Top 3 buildings (not faculty) with highest usage last year", "Basic Analysis"],
    ["Plot FKK usage last 3 months", "Basic Analysis"],
        ["Lowest 3 faculty usage in the last 3 months", "Basic Analysis"],
    ["Top 3 faculty usage in the last 3 months", "Basic Analysis"],
    ["FTI usage in the last 3 months", "Basic Analysis"],
    ["Plot last hour usage of FSRD", "Basic Analysis"],
    ["What is the usage trend of FSRD in the last 3 months", "Basic Analysis"],
    ["Compare SF and FMIPA usage trends", "Basic Analysis"],
    ["Total ITB usage over the past month", "Basic Analysis"],
    ["Total ITB usage over the past year", "Basic Analysis"],
    ["FTI usage in the last 3 months", "Basic Analysis"],
    ["Plot last hour usage of FSRD", "Basic Analysis"],
    ["Lowest 3 faculty usage in the last 3 months", "Basic Analysis"],
    ["Top 3 buildings (not faculty) with highest usage last year", "Basic Analysis"],
    ["Plot FKK usage last 3 months", "Basic Analysis"],
        ["Lowest 3 faculty usage in the last 3 months", "Basic Analysis"],
    ["Top 3 faculty usage in the last 3 months", "Basic Analysis"],
    ["FTI usage in the last 3 months", "Basic Analysis"],
    ["Plot last hour usage of FSRD", "Basic Analysis"],
    ["What is the usage trend of FSRD in the last 3 months", "Basic Analysis"],
    ["Compare SF and FMIPA usage trends", "Basic Analysis"],
    ["Total ITB usage over the past month", "Basic Analysis"],
    ["Total ITB usage over the past year", "Basic Analysis"],
    ["FTI usage in the last 3 months", "Basic Analysis"],
    ["Plot last hour usage of FSRD", "Basic Analysis"],
    ["Lowest 3 faculty usage in the last 3 months", "Basic Analysis"],
    ["Top 3 buildings (not faculty) with highest usage last year", "Basic Analysis"],
    ["Plot FKK usage last 3 months", "Basic Analysis"],
        ["Lowest 3 faculty usage in the last 3 months", "Basic Analysis"],
    ["Top 3 faculty usage in the last 3 months", "Basic Analysis"],
    ["FTI usage in the last 3 months", "Basic Analysis"],
    ["Plot last hour usage of FSRD", "Basic Analysis"],
    ["What is the usage trend of FSRD in the last 3 months", "Basic Analysis"],
    ["Compare SF and FMIPA usage trends", "Basic Analysis"],
    ["Total ITB usage over the past month", "Basic Analysis"],
    ["Total ITB usage over the past year", "Basic Analysis"],
    ["FTI usage in the last 3 months", "Basic Analysis"],
    ["Plot last hour usage of FSRD", "Basic Analysis"],
    ["Lowest 3 faculty usage in the last 3 months", "Basic Analysis"],
    ["Top 3 buildings (not faculty) with highest usage last year", "Basic Analysis"],
    ["Plot FKK usage last 3 months", "Basic Analysis"],
        ["Lowest 3 faculty usage in the last 3 months", "Basic Analysis"],
    ["Top 3 faculty usage in the last 3 months", "Basic Analysis"],
    ["FTI usage in the last 3 months", "Basic Analysis"],
    ["Plot last hour usage of FSRD", "Basic Analysis"],
    ["What is the usage trend of FSRD in the last 3 months", "Basic Analysis"],
    ["Compare SF and FMIPA usage trends", "Basic Analysis"],
    ["Total ITB usage over the past month", "Basic Analysis"],
    ["Total ITB usage over the past year", "Basic Analysis"],
    ["FTI usage in the last 3 months", "Basic Analysis"],
    ["Plot last hour usage of FSRD", "Basic Analysis"],
    ["Lowest 3 faculty usage in the last 3 months", "Basic Analysis"],
    ["Top 3 buildings (not faculty) with highest usage last year", "Basic Analysis"],
    ["Plot FKK usage last 3 months", "Basic Analysis"],
        ["Lowest 3 faculty usage in the last 3 months", "Basic Analysis"],
    ["Top 3 faculty usage in the last 3 months", "Basic Analysis"],
    ["FTI usage in the last 3 months", "Basic Analysis"],
    ["Plot last hour usage of FSRD", "Basic Analysis"],
    ["What is the usage trend of FSRD in the last 3 months", "Basic Analysis"],
    ["Compare SF and FMIPA usage trends", "Basic Analysis"],
    ["Total ITB usage over the past month", "Basic Analysis"],
    ["Total ITB usage over the past year", "Basic Analysis"],
    ["FTI usage in the last 3 months", "Basic Analysis"],
    ["Plot last hour usage of FSRD", "Basic Analysis"],
    ["Lowest 3 faculty usage in the last 3 months", "Basic Analysis"],
    ["Top 3 buildings (not faculty) with highest usage last year", "Basic Analysis"],
    ["Plot FKK usage last 3 months", "Basic Analysis"],
        ["Lowest 3 faculty usage in the last 3 months", "Basic Analysis"],
    ["Top 3 faculty usage in the last 3 months", "Basic Analysis"],
    ["FTI usage in the last 3 months", "Basic Analysis"],
    ["Plot last hour usage of FSRD", "Basic Analysis"],
    ["What is the usage trend of FSRD in the last 3 months", "Basic Analysis"],
    ["Compare SF and FMIPA usage trends", "Basic Analysis"],
    ["Total ITB usage over the past month", "Basic Analysis"],
    ["Total ITB usage over the past year", "Basic Analysis"],
    ["FTI usage in the last 3 months", "Basic Analysis"],
    ["Plot last hour usage of FSRD", "Basic Analysis"],
    ["Lowest 3 faculty usage in the last 3 months", "Basic Analysis"],
    ["Top 3 buildings (not faculty) with highest usage last year", "Basic Analysis"],
    ["Plot FKK usage last 3 months", "Basic Analysis"],

]

ASK_TEST_CASES_LINE = ASK_TEST_CASES_WEB
ASK_TEST_CASES_WHATSAPP = ASK_TEST_CASES_WEB

ASK_TEST_CASES_RESPOND_INITIAL_PROMPT = [
    ["What is ELISA", "Basic Knowledge"],
    ["What is the purpose of ELISA", "Basic Knowledge"],
    ["Bagaimana cara ELISA mengidentifikasi pemborosan energi di ITB?", "Basic Knowledge"],
    ["Fitur apa saja yang tersedia di dashboard ELISA untuk memantau konsumsi energi?", "Basic Knowledge"],
    ["Bagaimana ELISA membantu ITB dalam membandingkan penggunaan energi antar fakultas?", "Basic Knowledge"],
    ["Teknologi apa yang digunakan ELISA untuk mengumpulkan data konsumsi listrik secara real-time?", "Basic Knowledge"],
    ["Apa tujuan utama dari sistem ELISA dalam memantau konsumsi energi dan air di ITB?", "Basic Knowledge"],
    ["Bagaimana arsitektur SGAM (Smart Grid Architectural Model) digunakan dalam pengembangan ELISA?", "Basic Knowledge"],
    ["Fitur apa saja yang tersedia di dashboard ELISA untuk membandingkan penggunaan energi antar fakultas?", "Basic Knowledge"],
    ["Bagaimana data dari smart meter dikumpulkan dan diproses dalam platform Big Data ELISA?", "Basic Knowledge"],
    ["Apa saja indikator kinerja (seperti IKE dan EnPI) yang digunakan ELISA untuk mengevaluasi efisiensi energi?", "Basic Knowledge"],
    ["What is the weather like today", "Unrelevant"],
    ["What is your favorite color", "Unrelevant"],
    ["Tell me a joke", "Unrelevant"],
    ["What is the capital of France", "Unrelevant"],
    ["What is the meaning of life", "Unrelevant"],
    ["What is your name", "Unrelevant"],
    ["How are you doing today", "Unrelevant"],
    ["Berapa harga sebuah smartphone flagship terbaru tahun 2024?", "Unrelevant"],
    ["Apa resep membuat martabak manis yang enak?", "Unrelevant"],
    ["Bagaimana cara mengurus visa untuk studi di luar negeri?", "Unrelevant"],
    ["Siapa pemenang Piala Dunia FIFA 2022?", "Unrelevant"],
    ["Apa perbedaan antara kopi arabika dan robusta?", "Unrelevant"],
    ["What is the usage trend of FSRD in the last 3 months", "Basic Analysis"],
    ["Compare SF and FMIPA usage trends", "Basic Analysis"],
    ["Total ITB usage over the past month", "Basic Analysis"],
    ["Total ITB usage over the past year", "Basic Analysis"],
    ["Top 3 buildings with highest usage last year", "Basic Analysis"],
    ["Lowest 3 faculty usage in the last 3 months", "Basic Analysis"],
    ["Top 3 faculty usage in the last 3 months", "Basic Analysis"],
    ["FTI usage in the last 3 months", "Basic Analysis"],
    ["Plot last hour usage of FSRD", "Basic Analysis"],
    ["Forecast CC Barat usage during holidays", "Advanced Analysis"],
    ["Predict Labtek VI peak hours next week", "Advanced Analysis"],
    ["Average Engineering Physics Building usage during summer", "Basic Analysis"],
    ["Compare STEI usage: weekdays vs weekends", "Basic Analysis"],
    ["Forecast ITB usage for next academic year", "Advanced Analysis"],
    ["Labtek III usage trends last 3 semesters", "Advanced Analysis"],
    ["Predict FTI usage during next major event", "Advanced Analysis"],
    ["Forecast Labtek VII usage during winter break", "Advanced Analysis"],
    ["Cluster ITB buildings based on usage patterns", "Advanced Analysis"],
    ["Identify usage clusters among faculties", "Advanced Analysis"],
    ["Find anomaly clusters in weekend usage", "Advanced Analysis"],
    ["Cluster departments based on energy efficiency", "Advanced Analysis"],
]


ASK_TEST_CASES_UNRELEVANT = [
    "What is the weather like today",
    "What is your favorite color",
    "Tell me a joke",
    "What is the capital of France",
    "What is the meaning of life",
    "What is your name",
    "How are you doing today",
    "What is your favorite food",
    "What is your favorite movie",
    "What is your favorite book",
]

ASK_TEST_CASES_DATA_AVAILABILITY = [
    ["What is the usage trend of FSRD in the last 3 months", "Data Available"],
    ["Plot ITB Jakarta usage last month", "Data Not Available"],
    ["Impact of weather on energy use (correlation data)", "Data Not Available"],
    ["Plot Masjid Salman usage last month", "Data Not Available"],

    
    ["Compare SF and FMIPA usage trends", "Data Available"],
    ["Compare CC Timur and Barat peak usage", "Data Not Available"],
    ["Total ITB usage over the past month", "Data Available"],
    ["Total ITB usage over the past year", "Data Available"],
    ["Top 3 buildings with highest usage last year", "Data Available"],
    ["Lowest 3 faculty usage in the last 3 months", "Data Available"],
    ["Top 3 faculty usage in the last 3 months", "Data Available"],
    ["FTI usage in the last 3 months", "Data Available"],
    ["Last 100 years of ITB usage", "Data Not Available"],
    ["Hourly power consumption for Labtek V yesterday", "Data Available"],
    ["Monthly water consumption for SBM", "Data Not Available"],
    ["Three-phase balance analysis for Labtek VII", "Data Available"],
    ["Energy cost comparison between FTI and FTMD", "Data Available"],
    ["Power factor analysis for FMIPA buildings", "Data Available"],
    ["Identify peak usage hours for FSRD last week", "Data Available"],
    ["Water pressure trends in Jatinangor campus", "Data Available"],
    ["Pump operation status for all buildings", "Data Available"],
    ["Voltage fluctuations in Labtek III last month", "Data Available"],
    ["Energy consumption per student in each faculty", "Data Available"],
    ["Usage patterns during holidays vs regular days", "Data Available"],
    ["Predict next month's energy consumption", "Data Available"],

    ["Historical data from before 2010", "Data Not Available"],
    ["Energy usage in non-ITB buildings", "Data Not Available"],
    ["Detailed water usage per toilet", "Data Not Available"],
    ["Electrical consumption of individual appliances", "Data Not Available"],
    ["Real-time data from 10 years ago", "Data Not Available"],
    ["Energy usage of personal devices in student dormitories", "Data Not Available"],
    ["Real-time water consumption per faucet in all bathrooms", "Data Not Available"],
    ["Individual air conditioner usage in faculty offices", "Data Not Available"],
    ["Solar panel output from non-ITB installations", "Data Not Available"],
    ["Energy consumption of street lights outside campus", "Data Not Available"],
    ["Historical data from demolished buildings (pre-2015)", "Data Not Available"],
    ["Water quality metrics (pH, turbidity) in pipelines", "Data Not Available"],
    ["Electric vehicle charging station usage details", "Data Not Available"],
    ["Energy consumption of non-instrumented backup generators", "Data Not Available"],
    ["Wi-Fi router power usage across campus", "Data Not Available"],
    ["Detailed breakdown of lab equipment energy use", "Data Not Available"],
    ["Occupancy data tied to energy consumption", "Data Not Available"],
    ["Energy usage during campus-wide blackouts", "Data Not Available"],
    ["Water consumption in non-metered gardens", "Data Not Available"],
    ["Comparison with other universities' energy data", "Data Not Available"],
    ["Projected energy use for unbuilt future buildings", "Data Not Available"],
    ["Sub-metered data for individual room outlets", "Data Not Available"],
    ["Energy theft incidents and their impact", "Data Not Available"],
    ["Real-time power factor correction capacitor status", "Data Not Available"],
    ["Underground cable loss measurements", "Data Not Available"],
    ["Faculty-specific data before ELISA implementation (pre-2020)", "Data Not Available"],
    ["Energy consumption of temporary event structures", "Data Not Available"],
    ["Water usage in construction sites on campus", "Data Not Available"],
    ["Detailed harmonic spectrum analysis for all buildings", "Data Not Available"],
    ["Generator fuel consumption metrics", "Data Not Available"],
    ["Energy use during system maintenance downtime", "Data Not Available"],
    ["Building automation system setpoint changes", "Data Not Available"],
    ["Energy consumption of security systems", "Data Not Available"],
    ["Water pressure data at every floor junction", "Data Not Available"]
]

ASK_TEST_CASES_BASIC_KNOWLEDGE = [
    "What is ELISA",
    "What is the purpose of ELISA",
    "What are the applications of ELISA",
    "What is the specificity of ELISA",
    "Bagaimana cara ELISA mengidentifikasi pemborosan energi di ITB?",
    "Fitur apa saja yang tersedia di dashboard ELISA untuk memantau konsumsi energi?",
    "Bagaimana ELISA membantu ITB dalam membandingkan penggunaan energi antar fakultas?",
    "Teknologi apa yang digunakan ELISA untuk mengumpulkan data konsumsi listrik secara real-time?",
    "Apa tujuan utama dari sistem ELISA dalam memantau konsumsi energi dan air di ITB?",
    "Bagaimana arsitektur SGAM (Smart Grid Architectural Model) digunakan dalam pengembangan ELISA?",
    "Fitur apa saja yang tersedia di dashboard ELISA untuk membandingkan penggunaan energi antar fakultas?",
    "Bagaimana data dari smart meter dikumpulkan dan diproses dalam platform Big Data ELISA?",
    "Apa saja indikator kinerja (seperti IKE dan EnPI) yang digunakan ELISA untuk mengevaluasi efisiensi energi?",
]


# DATA ANALYSIS TEST CASES

ASK_TEST_CASES_BASIC_ANALYSIS = [
    "What is the usage trend of FSRD in the last 3 months",
    "Compare SF and FMIPA usage trends",
    "Total ITB usage over the past month",
    "Total ITB usage over the past year",
    "FTI usage in the last 3 months",
    "Plot last hour usage of FSRD",
    "Lowest 3 faculty usage in the last 3 months",
    "Top 3 faculty usage in the last 3 months",
    "Top 3 buildings (not faculty) with highest usage last year",
    "Plot FKK usage last 3 months"
]

ASK_TEST_CASES_ADVANCED_ANALYSIS = [
    "Compare FSRD and FTMD usage trends",
    "Forecast CC Barat usage during holidays",
    "Predict Labtek VI peak hours next week",
    "Average Engineering Physics Building usage during summer",
    "Compare STEI usage: weekdays vs weekends",
    "Forecast ITB usage for next academic year",
    "Labtek III usage trends last 3 semesters",
    "Predict FTI usage during next major event",
    "Forecast Labtek VII usage during winter break",
]




ASK_TEST_CASES_FORECAST = [
    "Forecast CC Barat usage during holidays",
    "Predict Labtek VI peak hours next week",
    "Forecast ITB usage for next academic year",
    "Predict FTI usage during next major event",
    "Forecast Labtek VII usage during winter break",
]

ASK_TEST_CASES_CLUSTERING = [
    "Compare FSRD and FTMD usage trends",
    "Plot last hour usage of FSRD",
    "Labtek III usage trends last 3 semesters",
]

ASK_TEST_CASES_PLOT = [
    "Plot last hour usage of FSRD",
    "Plot last hour usage of FSRD and FTMD",
    "Plot last hour usage of all buildings",
    "Plot last month usage of all buildings",
    "Plot last year usage of all buildings",
    "Plot last 3 months usage of all buildings",
]

ASK_TEST_CASES_DATE_CONCIOUS = [
    "Compare FSRD and FTMD usage trends",
    "Forecast CC Barat usage during holidays",
    "Predict Labtek VI peak hours next week",
    "Average Engineering Physics Building usage during summer",
    "Compare STEI usage: weekdays vs weekends",
    "Forecast ITB usage for next academic year",
    "Labtek III usage trends last 3 semesters",
    "Predict FTI usage during next major event",
    "Forecast Labtek VII usage during winter break",
]

ASK_ANALYSIS_INTERPRETER_TEST_CASES = [
]