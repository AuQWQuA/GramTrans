import json
from vllm import LLM, SamplingParams
import re
import random
import numpy as np
import os
import torch
import argparse
from parsegrammar import parsell1, parsell, parse2ll1, parse2ll


argparser = argparse.ArgumentParser()
argparser.add_argument("--model_name", type=str, default="DeepSeek_Python")
argparser.add_argument("--language", type=str, default="SimPy")
argparser.add_argument("--benchmark", type=str, default="humaneval")
argparser.add_argument("--model_type", type=str, default="starcoder")
args = argparser.parse_args()

random.seed(42)
np.random.seed(42)
torch.manual_seed(42)
torch.cuda.manual_seed_all(42)

model_name = args.model_name
language = args.language
benchmark = args.benchmark
model_type = args.model_type

model_path = f"models/{model_name}"

llm = LLM(
    model=model_path, 
    tensor_parallel_size=1,     
    max_model_len=2048,
    gpu_memory_utilization=0.8,
    trust_remote_code=True
)
sampling_params = SamplingParams(
    temperature=0,  
    top_p=1.0,    
    max_tokens=500,  
    seed=42,
    n=1,         
    stop=["```"]
)


def converse_output(output, language):
    if language == "1layer":
        return parsell1(output)
    elif language == "LL1":
        return parsell(output)
    else:
        return output
        
if language not in ["Grammar", "SimPy"]:
    if benchmark == "humaneval":
        with open("data/humaneval-python.jsonl", "r") as f:
            datas = [json.loads(line) for line in f]
        if model_type == "deepseek" or model_type == "qwen":
            if language == "1layer":
                prompts = ["Please finish the following function. ```ll1\n" + parse2ll1(d['prompt']) for d in datas]
            elif language == "LL1":
                prompts = ["Please finish the following function. ```ll1\n" + parse2ll(d['prompt'])[:-7] for d in datas]
            else:
                prompts = ["Please finish the following function. ```python\n" + d['prompt'] for d in datas]
        else:
            if language == "1layer":
                prompts = ["Please finish the following function.\n" + d['prompt'] + "please writ your code here\n```ll1\n" for d in datas]
            elif language == "LL1":
                prompts = ["Please finish the following function.\n" + d['prompt'] + "please writ your code here\n```ll1\n" for d in datas]
            else:
                prompts = ["Please finish the following function.\n" +  d['prompt'] + "please writ your code here\n```python\n" for d in datas]

        outputs = llm.generate(prompts, sampling_params=sampling_params)

        if model_type == "deepseek" or model_type == "qwen":        
            with open(f"output/{model_name}_{benchmark}.jsonl", "w") as f:
                for i, output in enumerate(outputs):
                    if language == "1layer":
                        code = parse2ll1(datas[i]['prompt']) + output.outputs[0].text
                    elif language == "LL1":
                        code = parse2ll(datas[i]['prompt'])[:-7] + output.outputs[0].text
                    else:
                        code = datas[i]['prompt'] + output.outputs[0].text
                    f.write(json.dumps({
                        "task_id": datas[i]["task_id"].replace("Python", "HumanEval"),
                        "solution": converse_output(code, language),
                        "origin_solution": code
                    }) + "\n")
        else:
            with open(f"output/{model_name}_{benchmark}.jsonl", "w") as f:
                for i, output in enumerate(outputs):
                    f.write(json.dumps({
                        "task_id": datas[i]["task_id"].replace("Python", "HumanEval"),
                        "solution": converse_output(output.outputs[0].text, language),
                        "origin_solution": output.outputs[0].text
                    }) + "\n")

    elif benchmark == "mbpp":

        with open("data/mbpp_eval_plus.jsonl", "r") as f:
            datas = [json.loads(line) for line in f]

        if language == "1layer":
            prompts = [d['prompt'] + '\nYour code should satisfy following tests' + parse2ll1(d['test'].replace("assert", "")) + "Please write your code here:\n ```ll1\n" for d in datas]
        elif language == "LL1":
            prompts = [d['prompt'] + '\nYour code should satisfy following tests' + parse2ll(d['test'].replace("assert", "")) + "Please write your code here:\n ```ll1\n" for d in datas]
        else:
            prompts = [d['prompt'] + '\nYour code should satisfy following tests' + d['test'] + "Please write your code here:\n ```python\n" for d in datas]

        outputs = llm.generate(prompts, sampling_params=sampling_params)

        with open(f"output/{model_name}_{benchmark}.jsonl", "w") as f:
            for i, output in enumerate(outputs):
                f.write(json.dumps({
                    "task_id": datas[i]["task_id"],
                    "solution": converse_output(output.outputs[0].text, language),
                    "origin_solution": output.outputs[0].text,
                }) + "\n")
elif language == "Grammar":
    if benchmark == "humaneval":
        if model_type == "deepseek" or model_type == "qwen":
            with open("data/humaneval-python-grammar.jsonl", "r") as f:
                datas = [json.loads(line) for line in f]

            prompts = ["Please finish the following function. ```grammar\n" + d['prompt2'] for d in datas]

            outputs = llm.generate(prompts, sampling_params=sampling_params)


            with open(f"output/{model_name}_{benchmark}.jsonl", "w") as f:
                for i, output in enumerate(outputs):
                    f.write(json.dumps({
                        "task_id": datas[i]["task_id"].replace("Python", "HumanEval"),
                        "origin_solution": datas[i]['prompt2'] + output.outputs[0].text,
                    }) + "\n")
        else:
            with open("/share/zhangzhao12/lllr/data/humaneval/humaneval-python-grammar.jsonl", "r") as f:
                datas = [json.loads(line) for line in f]
            prompts = ["Please finish the following function.\n" + d['prompt'] + "please writ your code here\n```grammar\n" for d in datas]

            outputs = llm.generate(prompts, sampling_params=sampling_params)


            with open(f"output/{model_name}_{benchmark}.jsonl", "w") as f:
                for i, output in enumerate(outputs):
                    f.write(json.dumps({
                        "task_id": datas[i]["task_id"].replace("Python", "HumanEval"),
                        "origin_solution": output.outputs[0].text,
                    }) + "\n")
    elif benchmark == "mbpp":
        with open("data/mbpp_eval_plus.jsonl", "r") as f:
            datas = [json.loads(line) for line in f]
        
        prompts = [d['prompt'] + '\nYour code should satisfy following tests' + d['test'] + "Please write your code here:\n ```grammar\n" for d in datas]

        outputs = llm.generate(prompts, sampling_params=sampling_params)

        with open(f"output/{model_name}_{benchmark}.jsonl", "w") as f:
            for i, output in enumerate(outputs):
                f.write(json.dumps({
                    "task_id": datas[i]["task_id"],
                    "origin_solution": output.outputs[0].text,
                }) + "\n")

elif language == "SimPy":
    if benchmark == "humaneval":
        if model_type == "deepseek" or model_type == "qwen":
            with open("data/humaneval-python-spy.jsonl", "r") as f:
                datas = [json.loads(line) for line in f]
            
            prompts = ["Please finish the following function. ```spy\n" + d['prompt'] for d in datas]

            outputs = llm.generate(prompts, sampling_params=sampling_params)


            with open(f"output/{model_name}_{benchmark}.jsonl", "w") as f:
                for i, output in enumerate(outputs):
                    f.write(json.dumps({
                        "task_id": datas[i]["task_id"].replace("Python", "HumanEval"),
                        "origin_solution": datas[i]['prompt'] + output.outputs[0].text,
                    }) + "\n")
        else:
            with open("data/humaneval-python.jsonl", "r") as f:
                datas = [json.loads(line) for line in f]
            
            prompts = ["Please finish the following function.\n" + d['prompt'] + "please writ your code here\n```spy\n"  for d in datas]
            outputs = llm.generate(prompts, sampling_params=sampling_params)
            with open(f"output/{model_name}_{benchmark}.jsonl", "w") as f:
                for i, output in enumerate(outputs):
                    f.write(json.dumps({
                        "task_id": datas[i]["task_id"].replace("Python", "HumanEval"),
                        "origin_solution": output.outputs[0].text,
                    }) + "\n")            
    elif benchmark == "mbpp":
        with open("data/mbpp_eval_plus.jsonl", "r") as f:
            datas = [json.loads(line) for line in f]
        
        prompts = [d['prompt'] + '\nYour code should satisfy following tests' + d['test'] + "Please write your code here:\n ```spy\n" for d in datas]

        outputs = llm.generate(prompts, sampling_params=sampling_params)

        with open(f"output/{model_name}_{benchmark}.jsonl", "w") as f:
            for i, output in enumerate(outputs):
                f.write(json.dumps({
                    "task_id": datas[i]["task_id"],
                    "origin_solution": output.outputs[0].text,
                }) + "\n")


