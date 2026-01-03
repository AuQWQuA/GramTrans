import json
from vllm import LLM, SamplingParams
import random
import numpy as np
import os
import torch
import argparse


argparser = argparse.ArgumentParser()
argparser.add_argument("--model_name", type=str, default="DSL_LL1")
args = argparser.parse_args()

random.seed(42)
np.random.seed(42)
torch.manual_seed(42)

model_name = args.model_name
model_path = f"./models/{model_name}"  

llm = LLM(model=model_path)

sampling_params = SamplingParams(
    temperature=0,  
    top_p=0.95,      
    max_tokens=200,  
    n=1,             
    stop=["<|endoftext|>"]
)

with open("./data/test.jsonl", "r") as f:
    datas = [json.loads(line) for line in f]

prompts = ["Please write a python code to solve the problem.\n" + d["prompt"] + "\n Please write your code here:\n" for d in datas]

outputs = llm.generate(prompts, sampling_params=sampling_params)


with open(f"./output/{model_name}.jsonl", "w") as f:
    for i, output in enumerate(outputs):
        f.write(json.dumps({
            "prompt": datas[i]["prompt"],
            "output": output.outputs[0].text,
            "answer": datas[i]["answer"],
            "code": datas[i]["code"]
        }) + "\n")


