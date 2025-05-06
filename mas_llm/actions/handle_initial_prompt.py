from model.model import InitialPromptHandlerResult

from fastapi import HTTPException
from mas_llm.actions.respond_initial_prompt import RespondInitialPrompt
from mas_llm.actions.ask_about_elisa import AskAboutElisa
from mas_llm.actions.ask_data_availability import AskDataAvailability

from metagpt.logs import logger

async def handleInitialPrompt(message):
    ask_about_elisa = AskAboutElisa()
    ask_data_availability = AskDataAvailability()
    respond_initial_prompt = RespondInitialPrompt()
    max_retry = 3
    
    agent_response = InitialPromptHandlerResult(type="", message="")

    logger.info(f"🔍 InitialPromptHandler (Respond Initial)- Checking prompt..")
    initial_result = await respond_initial_prompt.run(message)

    while max_retry > 0:
        if initial_result.type not in ["Basic Analysis", "Advanced Analysis", "Unrelevant", "Basic Knowledge Answerable", "Basic Knowledge Unaswerable"]:
            logger.info(f"⚠️ InitialPromptHandler (Respond Initial) - Result: {initial_result}, retrying..")
            initial_result = await respond_initial_prompt.run(message)
            max_retry -= 1
        else:
            break
    
    if initial_result.type not in ["Basic Analysis", "Advanced Analysis", "Unrelevant", "Basic Knowledge Answerable", "Basic Knowledge Unaswerable"]:
        logger.info(f"🔴 InitialPromptHandler - Failed, Result: {initial_result}")
        raise HTTPException(status_code=400, detail="Prompt validation failed")
    
    logger.info(f"🟢 InitialPromptHandler (Respond Initial) -  Type: {initial_result.type}, Message: {initial_result.message}")
    

    if initial_result.type == "Unrelevant":
        agent_response.type = "Final Answer"
        agent_response.message = initial_result.message

        return initial_result
    
    if initial_result.type == "Basic Knowledge Answerable":
        agent_response.type = "Final Answer"
        agent_response.message = initial_result.message

        return agent_response

    if initial_result.type == "Basic Knowledge Unaswerable":
        logger.info(f"🔍 InitialPromptHandler (Ask ELISA)- Asking about ELISA..")
        ask_elisa_result = await ask_about_elisa.run(message)
        agent_response.type = "Final Answer"
        agent_response.message = ask_elisa_result

        logger.info(f"🟢 InitialPromptHandler (Ask ELISA) -  Type: \"Final Answer\", Message: {ask_elisa_result}")

        return agent_response
    
    # if initial_result.type == "Basic Analysis" or initial_result.type == "Advanced Analysis":
    logger.info(f"🔍 InitialPromptHandler (Check Data) - Checking data availability..")
    data_availability = await ask_data_availability.run(message)
    
    if data_availability.type == "Data Available":
        agent_response.type = initial_result.type
        agent_response.message =  message
        logger.info(f"🟢 InitialPromptHandler (Check Data) - Data available")

    else:
        agent_response.type = "Final Answer"
        agent_response.message = data_availability.message

        logger.info(f"⚠️ InitialPromptHandler (Check Data) - Data not available")
    

    return agent_response
    
    