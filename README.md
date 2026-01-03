# Easier Grammar Leads to Better Performance in Neural Code Generation

> **Paper**: *Easier Grammar Leads to Better Performance in Neural Code Generation*  
> **Keywords**: code representation, code generation, large language model

---

## Overview

This paper is a study for exploring how the parsing difficulty of code representations impacts neural code generation. Our key conjecture is:

> *The easier a code representation is to parse, the better the model's performance.*

### Motivation

Let us illustrate our motivation with an intuitive, though not necessarily rigorous, example. Consider the expression `a+b`. Both humans and machines need to understand this expression by first recognizing the `+` operator in the middle to identify it as an addition expression, then reading `a` and `b` to understand the operands being added. For humans, we can directly read the plus sign in the middle. However, for computers that process text from left to right, representing the expression as `+ a b` makes it easier to align the text with its semantics. From a formal perspective, the latter corresponds to a grammar that is easier to parse.

For large language models, this difference may affect the model's output generation in the following way. Taking the above example, when the model generates code, if it needs to compute the sum of `a` and `b` from a semantic perspective, then for the first expression (`a+b`), the model cannot directly predict the plus sign because it appears in the second position. Therefore, the model's current parameters need to be able to "remember that a plus sign should be generated in the second position" while simultaneously biasing the next token toward generating `a`. In contrast, for the second expression (`+ a b`), the model can first generate the plus sign, and then leverage the attention mechanisms associated with the plus sign to generate `a`.


---

## Key Contributions

- ✅ **Empirical Validation**: Parsing difficulty correlates with model performance, demonstrated on a Python DSL derived from MathQA. （DSL<sub>LL(1)</sub>,  DSL<sub>LL(2)</sub>, DSL<sub>LR(1)</sub> ,DSL<sub>NCFG</sub>）
- 🔄 **Automatic Transformation**: A novel algorithm, **GramTrans**, that transforms any context-free grammar into an LL(1) grammar using hierarchical conflict elimination.
- 📊 **Comprehensive Evaluation**: Two new representations 1layer and LL(1) derived from **GramTrans**, and make Experiments on Python and Java with StarCoder, DeepSeek-Coder, and Qwen2.5, outperforming grammar-rule-based and SimPy-style representations.
- 📚 **Structural Analysis**: Classification of existing representations by grammar class, reinforcing the conjecture through structural insight.


---

## Results
### 🧪 DSL Experiment Results

Experimental results on four DSL variants with increasing parsing difficulty, evaluated using pass@1 over the top 5 checkpoints.

| Language             | pass@1 Top-5 Checkpoints (%)           | Mean (%) | Std (%) |
|----------------------|-----------------------------------------|----------|----------|
| DSL<sub>LL(1)</sub>  | [81.89, 82.00, 82.00, 82.05, 82.05]     | 82.00    | 0.07     |
| DSL<sub>LL(2)</sub>  | [81.68, 81.73, 81.73, 81.78, 81.78]     | 81.74    | 0.04     |
| DSL<sub>LR(1)</sub>  | [80.99, 81.04, 81.15, 81.20, 81.31]     | 81.14    | 0.13     |
| DSL<sub>NCFG</sub>   | [80.35, 80.35, 80.40, 80.46, 80.51]     | 80.41    | 0.07     |
### 📊 Performance of Code Representations on HumanEval(+) and MBPP(+)

#### StarCoder-1B

| Representation | HumanEval | HumanEval+ | MBPP | MBPP+ | Avg |
|----------------|-----------|------------|------|--------|------|
| Python         | 64.4 (±0.7) | 60.5 (±0.8) | 66.7 (±0.4) | 57.4 (±0.7) | 62.2 (±0.1) |
| SimPy          | 66.5 (±0.7) | 62.9 (±0.8) | 66.4 (±0.6) | 57.2 (±0.7) | 63.3 (±0.1) |
| Grammar        | 68.7 (±1.1) | 64.6 (±0.9) | **69.6** (±1.1) | 58.5 (±1.0) | 65.4 (±0.7) |
| 1layer         | 70.1 (±0.7) | 64.8 (±1.0) | 69.3 (±0.9) | **59.1** (±0.4) | 65.8 (±0.1) |
| LL(1)          | **72.0** (±1.1) | **67.2** (±1.3) | 68.6 (±1.1) | 58.0 (±1.3) | **66.4** (±0.1) |

#### DeepSeek-Coder 1.3B

| Representation | HumanEval | HumanEval+ | MBPP | MBPP+ | Avg |
|----------------|-----------|------------|------|--------|------|
| Python         | 66.4 (±0.5) | 62.4 (±0.9) | 72.0 (±0.7) | 60.0 (±0.6) | 65.2 (±0.1) |
| SimPy          | 65.2 (±1.8) | 61.0 (±0.9) | 71.5 (±0.7) | 60.2 (±1.3) | 64.5 (±0.5) |
| Grammar        | 69.3 (±0.9) | 65.1 (±0.9) | **73.5** (±0.6) | **61.7** (±0.8) | 67.4 (±0.5) |
| 1layer         | 71.7 (±0.7) | 66.9 (±0.5) | 73.2 (±0.8) | 61.4 (±0.7) | **68.3** (±0.2) |
| LL(1)          | **72.3** (±1.0) | **67.8** (±1.0) | 72.6 (±0.4) | 60.3 (±0.8) | **68.3** (±0.5) |

#### Qwen2.5 1.5B

| Representation | HumanEval | HumanEval+ | MBPP | MBPP+ | Avg |
|----------------|-----------|------------|------|--------|------|
| Python         | 64.9 (±0.5) | 59.6 (±0.9) | 70.3 (±0.8) | 59.0 (±0.4) | 63.4 (±0.5) |
| SimPy          | 67.2 (±1.6) | 62.8 (±0.7) | 70.3 (±1.0) | 59.1 (±1.1) | 64.9 (±0.4) |
| Grammar        | 67.9 (±1.1) | 61.7 (±1.9) | 72.0 (±1.1) | 61.0 (±0.9) | 65.7 (±0.4) |
| 1layer         | **70.4** (±1.3) | 64.1 (±1.3) | **72.9** (±0.9) | **61.7** (±0.3) | **67.3** (±0.5) |
| LL(1)          | 69.6 (±1.8) | **64.5** (±0.7) | 72.9 (±0.7) | 61.6 (±0.5) | 67.2 (±0.4) |




### 🧮 Average Number of Training Tokens per Representation

The table below shows the average number of training tokens for each representation and their relative change compared to the original Python representation.

| Representation | StarCoder-1B | DeepSeek-Coder 1.3B | Qwen2.5 1.5B |
|----------------|---------------|----------------------|----------------|
| Python         | 192 (100.0%)  | 217 (100.0%)         | 169 (100.0%)   |
| SimPy          | 179 (92.9%)   | 196 (90.5%)          | 156 (92.1%)    |
| Grammar        | 360 (187.3%)  | 372 (172.0%)         | 347 (204.9%)   |
| 1layer         | 201 (104.3%)  | 225 (104.0%)         | 177 (104.7%)   |
| LL(1)          | 233 (120.9%)  | 263 (121.6%)         | 203 (120.0%)   |

---

### ☕ Java Results on HumanEval-X

This table reports the performance of the original Java and its 1-layer version Java_1layer on HumanEval-X, as well as the average number of training tokens used.

| Representation | DeepSeek-Coder 1.3B Score | Tokens | Qwen2.5 1.5B Score | Tokens |
|----------------|----------------------------|--------|---------------------|--------|
| Java           | 58.2 (±0.7)                | 159.2 (100.0%) | 58.5 (±0.7)         | 122.9 (100.0%) |
| Java_1layer    | 60.0 (±1.0)                | 159.3 (100.0%) | 61.0 (±0.9)         | 120.0 (97.6%)  |

---

### 🏆 Top-1 Checkpoint Performance

In addition to reporting 5-checkpoint averages, we also present the top-1 checkpoint results for each representation:

#### StarCoder-1B

| Representation | HumanEval | HumanEval+ | MBPP | MBPP+ | Avg |
|----------------|-----------|------------|------|--------|------|
| Python         | 65.2      | 61.6       | 67.2 | 58.1  | 62.3 |
| SimPy          | 67.2      | 63.6       | 66.9 | 57.9  | 63.3 |
| Grammar        | 70.1      | 65.9       | **70.9** | 59.8  | 66.0 |
| 1layer          | 71.3      | 65.9       | 70.1 | 59.5  | 66.1 |
| LL(1)         | **72.6**  | **68.3**   | 70.1 | **60.1** | **66.5** |

#### DeepSeek-Coder 1.3B

| Representation | HumanEval | HumanEval+ | MBPP | MBPP+ | Avg |
|----------------|-----------|------------|------|--------|------|
| Python         | 67.1      | 63.6       | 72.8 | 60.6  | 65.4 |
| SimPy          | 67.0      | 62.2       | 72.2 | 61.1  | 65.3 |
| Grammar        | 70.7      | 66.5       | 73.8 | 62.2 | 67.9 |
| 1layer          | 72.6      | 67.7       | **74.1** | **62.2**  | **68.7** |
| LL(1)         | **73.2**  | **68.9**   | 73.0 | 62.1  | **68.7** |

#### Qwen2.5 1.5B

| Representation | HumanEval | HumanEval+ | MBPP | MBPP+ | Avg |
|----------------|-----------|------------|------|--------|------|
| Python         | 66.5      | 61.0       | 71.4 | 59.5  | 64.1 |
| SimPy          | 68.3      | 63.4       | 71.5 | 60.1  | 65.4 |
| Grammar        | 69.5      | 64.6       | 73.3 | 62.4  | 66.3 |
| 1layer          | 71.3      | **67.1**   | **74.3** | **62.4** | **68.1** |
| LL(1)         | **72.0**  | 65.2       | 73.8 | 61.9  | 67.6 |

---

### 📐 Grammar LL(1) Conflict Number

Since parsing complexity is difficult to quantify and the number of conflicts is also not straightforward to define, we instead measure the number of conflicts by counting how many terminal symbols must be added, according to GramTrans, to transform the grammar into an LL(1) grammar.

| Representation | Conflict Number | 
|----------------|-----------|
| Python         | 42        | 
| SimPy          | 40        | 
| Grammar        | 0         |
| 1layer         | 8         |
| LL(1)          | 0         | 

---

## Case Study

Since our improvements are not based on syntax errors but rather semantic errors, it becomes difficult to intuitively explain the advantages of our method through examples, as different representations may generate completely different programs during testing, making comparison challenging. High-level semantics may directly influence code structure, causing the code shown from both ends to appear as entirely different solutions.

In our examples, we have selected several relatively similar programs to demonstrate the impact of easier-to-parse representations on the model.

### Case 1

```
#task_id: Mbpp/750
#Problem: Write a function to add the given tuple to the given list.
#         assert add_tuple([5, 6, 7], (9, 10)) == [5, 6, 7, 9, 10]
```
```
#python_solution:
def add_tuple(list1, tuple1):
    list1.append(tuple1)
    return list1
```

```
#1layer_solution(original):
def add_tuple(list1, tuple1):
    return + list1 call list(tuple1)
```
```
#1layer_solution(translated):
def add_tuple(list1, tuple1):
    return list1 + list(tuple1)
```

In this example, the task requires adding the contents of the tuple to the list. The Python version produces an incorrect answer, while the 1layer version produces the correct one.

Although the two solutions have different architectures, we can observe that the error in the Python solution stems from appending the entire tuple as a single element to the list, rather than adding its contents.

The key turning point lies in the fact that after the Python program generates `list1`, it should generate `+` rather than `append`. Despite understanding from the prompt and examples that the logic should be `+` rather than `append`, once the concrete object `list1` is generated first, the attention associated with `list1` also influences the probability distribution of the next token, causing the probability of `.append` to increase, ultimately leading to the selection of `.append`. For the 1layer version, the core logic generation aligns better with semantics. The decision about the addition operation is made earlier, making it easier for the model to determine the appropriate approach to use here.

### Case 2

```
#task_id: Mbpp/56
#Problem: Write a python function to check if a given number is one less than twice its reverse.
#         assert check(70) == False
```
```
#python_solution:
def check(n):
    reversed_n = int(str(n)[::-1])
    return n == reversed_n - 1
```

```
#1layer_solution(original):
def check(num):
    = rev_num call int(call str(num)[::NEG 1])
    return num == - * rev_num 2 1
```
```
#1layer_solution(translated):
def check(num):
    rev_num = int(str(num)[::-1])
    return num == rev_num * 2 - 1
```

The second example requires checking whether a number equals twice its reverse minus one. In this case, the answers from both representations are more similar. The Python answer is incorrect because it misses the `* 2` operation, while the 1layer answer is correct.

Similarly, before generating `reversed_n`, the Python version's program understands the problem statement and solves the reversal logic. However, when generating `reversed_n`, the model needs to simultaneously remember that the top level of the logic is a subtraction, followed by a multiplication, and that `reversed_n` and `2` are the operands of the multiplication. When mapping this to the program, it needs to predict `reversed_n` with high probability, and after generating `reversed_n`, the newly added attention should collectively increase the probability of `*` (clearly, the model fails at this step).

In contrast, the generation order of the 1layer version is closer to the logical order. When generating, the model first only needs to notice that the top level of the logic is a subtraction, and the next level is a multiplication. This may reduce the burden on parameter prediction.

---

## Repository Structure
This repository contains all the artifacts from our experiments, which span both a controlled DSL experiment and large-scale code generation tasks on Python and Java.


```
GramTrans/
├── DSL_experiment/         # Small language experiments based on MathQA DSL
│   ├── models/             # Models trained on 4 DSL languages
│   ├── data/               # MathQA test benchmarks
│   ├── output/             # Outputs
│   ├── inference.py        # Script for running model inference
│   └── test.py             # Script for running test
│
├── Python_Java_experiment/ 
│   ├── models/             # Models and Baseline Models
│   ├── data/               # MBPP HumanEval benchmarks (different representation version)
│   ├── output/             # Outputs
│   ├── inference.py        # Script for running model inference (Python)
│   ├── inference_java.py   # Script for running model inference (Java)
│   └── javatest.py         # Script for running test for Java
│
├── transform/              # transformation part
│   ├── GramTrans           # GramTrans algorithm implementation
│   ├── scripts             # Python and Java transformation
│
├── parse_environment/      # local python packages
│
├── requirements.txt       
│
└── README.md
```

---

## Getting Started

### 1. Setup Environment

```bash
conda env create -f environment.yml
conda activate GramTrans
cd parse_environment
pip install \
  tree-sitter-mathqapython/ \
  tree-sitter-mathqapythoncsg/ \
  tree-sitter-mathqapythonll1/ \
  tree-sitter-mathqapythonll2/ \
  tree-sitter-pymbhe/ \
  tree-sitter-pymbhell1/ \
  tree-sitter-javahemp/ \
  tree-sitter-javahempll/
```

### 2. Download Models
Due to the number of models involved in our experiments, we have uploaded models to Hugging Face:

🔗 https://huggingface.co/GramTrans

The repository includes:
- ✅ 4 models for the DSL experiment
- 🐍 15 models for the Python experiment
- ☕ 4 models for the Java experiment

To run evaluation, we recommend placing the downloaded models into the corresponding `models/` folder:
- DSL: `dsl_experiment/models/`
- Python/Java: `Python_Java_experiment/models/`


### 3. DSL Evaluation

#### Inference

Activate the Conda environment, check the directory to DSL_experiment and run the following command to perform inference on the MathQA dataset:

```bash
python inference.py --model_name <model_name>
```

- Models are expected to be stored in DSL_experiment/models/.
 
- Inference results will be saved to DSL_experiment/output/.



#### Evaluation

To evaluate the prediction accuracy:

```bash
python test.py --file_name <output_file_name> --language <LL1|LL2|LR1|NCFG>
```
- The file_name refers to the JSON file in the output/ directory.

- The language parameter should be one of: LL1, LL2, LR1, or NCFG.

- The script will output the number of correctly answered MathQA problems.

### 4. Python Evaluation

#### Inference

Navigate to the `Python_Java_experiment/` directory and run the following command:

```bash
python inference.py \
  --model_name <model_name> \
  --language <Python|SimPy|Grammar|1layer|LL1> \
  --benchmark <humaneval|mbpp> \
  --model_type <deepseek|qwen2.5|starcoder>
```

- Models are assumed to be stored in `Python_Java_experiment/models/`.
- The output will be saved in the `output/` directory.

#### Postprocessing

- For `Python`, `1layer`, and `LL1` representations, outputs are already in valid Python format.
- For `SimPy` and `Grammar` representations, conversion to Python is required using external tools:
  - SimPy: https://github.com/v587su/SimPy
  - Grammar: https://github.com/LIANGQINGYUAN/GrammarCoder

Please use the official scripts provided in those repositories to perform conversion.

#### Evaluation

We evaluate the generated code using [evalplus](https://github.com/OpenBMB/EvalPlus). It is already included in the environment.

Run the following command:

```bash
evalplus.evaluate --dataset <mbpp|humaneval> --samples <path_to_generated_file>
```

### 5. Java Model Evaluation

#### Inference

To run inference on Java benchmarks, execute the following command from the `Python_Java_experiment/` directory:

```bash
python inference_java.py \
  --model_name <model_name> \
  --language <Java|1layer> \
  --benchmark humaneval \
  --model_type <deepseek|qwen2.5>
```

- The models should be placed in `Python_Java_experiment/models/`.
- The output will be saved in the `output/` directory.

#### Evaluation

Java evaluation requires a JDK 17+ environment. Make sure `java` and `javac` are available in your system path.

Run the evaluation script with:

```bash
python javatest.py --filename <path_to_generated_java_file>
```

The script will compile and run the generated Java code to assess correctness based on HumanEval test cases.




## License

This project is licensed under the MIT License.