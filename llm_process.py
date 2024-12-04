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
    result = llm(
        "consider the following table and suggest me 1 single product or row which has more chances of getting bought based on ant time stat: event_time event_type product_id category_id category_code brand price user_id user_session 2019-11-01 00:00:00 UTC view 1003461 2053013555631882655 electronics.smartphone xiaomi 489.07 520088904 4d3b30da-a5e4-49df-b1a8-ba5943f1dd33 2019-11-01 00:00:00 UTC view 5000088 2053013566100866035 appliances.sewing_machine janome 293.65 530496790 8e5f4f83-366c-4f70-860e-ca7417414283 2019-11-01 00:00:01 UTC view 17302664 2053013553853497655 creed 28.31 561587266 755422e7-9040-477b-9bd2-6a6e8fd97387 2019-11-01 00:00:01 UTC view 3601530 2053013563810775923 appliances.kitchen.washer lg 712.87 518085591 3bfb58cd-7892-48cc-8020-2f17e6de6e7f consider this table values and suggest me a product which has more chances of getting bought"
    )
    print(result)