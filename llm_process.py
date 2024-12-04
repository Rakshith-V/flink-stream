import torch
from langchain import HuggingFacePipeline
from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationConfig, pipeline

def process_prompt(data):

    MODEL_NAME = "TheBloke/Llama-2-13b-Chat-GPTQ"
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, use_fast=True)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME, torch_dtype=torch.float16, trust_remote_code=True, device_map="auto"
    )
    generation_config = GenerationConfig.from_pretrained(MODEL_NAME)
    generation_config.max_new_tokens = 1024
    generation_config.temperature = 0.0001
    generation_config.top_p = 0.95
    generation_config.do_sample = True
    generation_config.repetition_penalty = 1.15

    text_pipeline = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        return_full_text=True,
        generation_config=generation_config,
    )
    llm = HuggingFacePipeline(pipeline=text_pipeline, model_kwargs={"temperature": 0})

    table_header = "event_time,event_type,product_id,category_id,category_code,brand,price,user_id,user_session\n"
    table_rows = ""
    for event in data:
        row = "{event_time},{event_type},{product_id},{category_id},{category_code},{brand},{price},{user_id},<user_session_placeholder>\n".format(
            event_time=event.get("event_time", ""),
            event_type=event.get("event_type", ""),
            product_id=event.get("product_id", ""),
            category_id=event.get("category_id", ""),
            category_code=event.get("category_code", ""),
            brand=event.get("brand", ""),
            price=event.get("price", ""),
            user_id=event.get("user_id", ""),
        )
        table_rows += row

    # Construct the prompt
    prompt = (
        "Consider the following table of user events:\n\n"
        f"{table_header}{table_rows}\n"
        "Based on this data, suggest one single product or row which has the highest chance of being purchased."
    )
    result = llm(prompt)
    return result