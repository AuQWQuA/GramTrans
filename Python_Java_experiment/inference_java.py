import json
from vllm import LLM, SamplingParams
import re
import random
import tempfile
import numpy as np
import os
import torch
import argparse
from parsegrammarjava import parse2ll, parsell

argparser = argparse.ArgumentParser()
argparser.add_argument("--model_name", type=str, default="DeepSeek_1layer_Java")
argparser.add_argument("--language", type=str, default="java")
argparser.add_argument("--benchmark", type=str, default="humaneval")
argparser.add_argument("--model_type", type=str, default="deepseek")
args = argparser.parse_args()

random.seed(42)
np.random.seed(42)
torch.manual_seed(42)

model_name = args.model_name
language = args.language
benchmark = args.benchmark
model_type = args.model_type

model_path = f"models/{model_name}"

llm = LLM(model=model_path, trust_remote_code=True)


sampling_params = SamplingParams(
    temperature=0,  
    top_p=1.0,    
    max_tokens=500,  
    seed=42,
    n=1,         
    stop=["```"]
)

if benchmark == "humaneval":    
    with open("data/humaneval-java-prompt.jsonl", "r") as f:
        datas = [json.loads(line) for line in f.readlines()]


if language == "1layer":
    prompts = [d['prompt3'] for d in datas]
else:
    prompts = [d['prompt2'] for d in datas]

outputs = llm.generate(prompts, sampling_params=sampling_params)


with open(f"output/{model_name}_{benchmark}.jsonl", "w") as f:
    for i, output in enumerate(outputs):
        if language == "1layer":
            code = parsell(datas[i]['prompt_ll'] + output.outputs[0].text)
        else:
            code = datas[i]['prompt'] + output.outputs[0].text
        f.write(json.dumps({
            "task_id": datas[i]["task_id"],
            "solution":  code + "\n" + datas[i]['test'],
            "origin_solution":  output.outputs[0].text,
        }) + "\n")
