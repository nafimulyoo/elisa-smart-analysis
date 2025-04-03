TEST_URL = "http://localhost:8000"

# TEST ANALYSIS CONFIG
TEST_FACULTY = "FTI"  
TEST_BUILDING = "LABTEK VI"  
TEST_FLOOR = ""  
TEST_PAST_DATE = "2025-03-01" 
TEST_PAST_DATE_END_HEATMAP = "2025-03-07"  
TEST_PAST_MONTH = "2025-02"

ASK_TEST_CASES_WEB = [
    "What is ELISA",
    "Compare FSRD and FTMD usage trends",
    "Top 3 buildings with highest usage last year",
    "Compare usage during exams",
    "Forecast CC Barat usage during holidays",
    "Predict Labtek VI peak hours next week",
    "Average Engineering Physics Building usage during summer",
    "Compare STEI usage: weekdays vs weekends",
    "Forecast ITB usage for next academic year",
    "Labtek III usage trends last 3 semesters",
    "Predict FTI usage during next major event",
    "Compare CC Timur and Barat peak usage",
    "Total ITB usage over the past decade",
    "Forecast Labtek VII usage during winter break",
    "Compare SF and FMIPA usage trends"
]

ASK_TEST_CASES_LINE = ASK_TEST_CASES_WEB
ASK_TEST_CASES_WHATSAPP = ASK_TEST_CASES_WEB

ASK_TEST_CASES_RESPOND_INITIAL_PROMPT = [
    ["What is ELISA", "Basic Knowledge"],
    ["What is the purpose of ELISA", "Basic Knowledge"],
    ["What are the steps in ELISA", "Basic Knowledge"],
    ["What are the types of ELISA", "Basic Knowledge"],
    ["What is the difference between direct and indirect ELISA", "Basic Knowledge"],
    ["What is the difference between sandwich and competitive ELISA", "Basic Knowledge"],
    ["What are the advantages of ELISA", "Basic Knowledge"],
    ["What are the limitations of ELISA", "Basic Knowledge"],
    ["What are the applications of ELISA", "Basic Knowledge"],
    ["What is the specificity of ELISA", "Basic Knowledge"],
    ["What is the weather like today", "Unrelevant"],
    ["What is your favorite color", "Unrelevant"],
    ["Tell me a joke", "Unrelevant"],
    ["What is the capital of France", "Unrelevant"],
    ["What is the meaning of life", "Unrelevant"],
    ["What is your name", "Unrelevant"],
    ["How are you doing today", "Unrelevant"],
    ["What is your favorite food", "Unrelevant"],
    ["What is your favorite movie", "Unrelevant"],
    ["What is your favorite book", "Unrelevant"],
    ["What is the usage trend of FSRD in the last 3 months", "Basic Analysis"],
    ["Compare SF and FMIPA usage trends", "Basic Analysis"],
    ["Compare CC Timur and Barat peak usage", "Basic Analysis"],
    ["Total ITB usage over the past month", "Basic Analysis"],
    ["Total ITB usage over the past year", "Basic Analysis"],
    ["Top 3 buildings with highest usage last year", "Basic Analysis"],
    ["Lowest 3 faculty usage in the last 3 months", "Basic Analysis"],
    ["Top 3 faculty usage in the last 3 months", "Basic Analysis"],
    ["FTI usage in the last 3 months", "Basic Analysis"],
    ["Plot last hour usage of FSRD", "Basic Analysis"],
    ["Forecast CC Barat usage during holidays", "Advanced Analysis"],
    ["Predict Labtek VI peak hours next week", "Advanced Analysis"],
    ["Average Engineering Physics Building usage during summer", "Advanced Analysis"],
    ["Compare STEI usage: weekdays vs weekends", "Advanced Analysis"],
    ["Forecast ITB usage for next academic year", "Advanced Analysis"],
    ["Labtek III usage trends last 3 semesters", "Advanced Analysis"],
    ["Predict FTI usage during next major event", "Advanced Analysis"],
    ["Forecast Labtek VII usage during winter break", "Advanced Analysis"],
]


ASK_TEST_CASES_BASIC_KNOWLEDGE = [
    "What is ELISA",
    "What is the purpose of ELISA",
    "What are the steps in ELISA",
    "What are the types of ELISA",
    "What is the difference between direct and indirect ELISA",
    "What is the difference between sandwich and competitive ELISA",
    "What are the advantages of ELISA",
    "What are the limitations of ELISA",
    "What are the applications of ELISA",
    "What is the specificity of ELISA",
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
ASK_TEST_CASES_BASIC_ANALYSIS = [
    "What is the usage trend of FSRD in the last 3 months",
    "Compare SF and FMIPA usage trends",
    "Compare CC Timur and Barat peak usage",
    "Total ITB usage over the past month",
    "Total ITB usage over the past year",
    "Top 3 buildings with highest usage last year",
    "Lowest 3 faculty usage in the last 3 months",
    "Top 3 faculty usage in the last 3 months",
    "FTI usage in the last 3 months",
    "Plot last hour usage of FSRD",
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


    # "Compare SF and FMIPA usage trends",
    # "Compare CC Timur and Barat peak usage",
    # "Total ITB usage over the past month",
    # "Total ITB usage over the past year",
    # "Top 3 buildings with highest usage last year",
    # "Lowest 3 faculty usage in the last 3 months",
    # "Top 3 faculty usage in the last 3 months",
    # "FTI usage in the last 3 months",
    # "Plot last hour usage of FSRD",
ASK_TEST_CASES_DATA_AVAILABILITY = [
    ["What is the usage trend of FSRD in the last 3 months", "Data Available"],
    ["Compare SF and FMIPA usage trends", "Data Available"],
    ["Compare CC Timur and Barat peak usage", "Data Available"],
    ["Total ITB usage over the past month", "Data Available"],
    ["Total ITB usage over the past year", "Data Available"],
    ["Top 3 buildings with highest usage last year", "Data Available"],
    ["Lowest 3 faculty usage in the last 3 months", "Data Available"],
    ["Top 3 faculty usage in the last 3 months", "Data Available"],
    ["FTI usage in the last 3 months", "Data Available"],
    # data not available test case!
    ["Plot ITB Jakarta usage last month", "Data Not Available"],
    ["Last 100 years of ITB usage", "Data Not Available"],
    ["Plot Masjid Salman usage last month", "Data Not Available"],
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