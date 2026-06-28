from llama_cpp import Llama
import tool
import time

global ctext,tmpt,top_p,max_tokens,condition,llm

model = ["./models/Qwen3-1.7B-Q4_K_M.gguf","./models/Qwen3.5-0.8B-Q4_K_M.gguf"]


print("模型加载完成！")
print("模型回答中的<think>…………</think>是深度思考的思维链")

ctext = [{"role": "system", "content": "你是一个AI助手，回答要简洁，避免废话。"}]
temperature = {"默认":{"max_tokens":512,"top_p":0.85,"tmpt":0.4},"日常":{"max_tokens":256,"top_p":0.75,"tmpt":0.4},"写作":{"max_tokens":1500,"top_p":0.8,"tmpt":0.5},"代码":{"max_tokens":None,"top_p":0.9,"tmpt":0.2}}
condition = "代码"
max_tokens = temperature[condition]["max_tokens"]
tmpt = temperature[condition]["tmpt"]
top_p = temperature[condition]["top_p"]
n_ctx = 4096
if condition == "日常":
    ctext[0]["content"] += "/no_think"
if condition == "代码":
    n_ctx = 8192
if condition == "写作":
    n_ctx = 6000

llm = Llama(
    model_path=model[0], #这里是你选择model列表的第几项，一般来说填0就行
    n_ctx=n_ctx,
    n_threads=4, #设置为你的CPU物理核心数，注意，是物理核心数，比如我的i5 11320H是4核心8线程，所以设为4
    n_gpu_layers=0, #如果有英伟达的显卡的话可以调高，用GPU加速
    use_mlock=True,
    verbose=False,
    last_n_tokens_size=64,
)

def generate_response(msg, max_tokens=512, temperature=0.4, top_p=0.8):
    start = None
    output = llm.create_chat_completion(
        messages=msg,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        stream=True,
        repeat_penalty=1.1,
    )
    for chunk in output:
        if start == None:
            start = time.time()
        if "choices" in chunk and len(chunk["choices"]) > 0:
            delta = chunk["choices"][0].get("delta", {})
            if "content" in delta:
                yield delta["content"]
    token_count = llm.n_tokens
    end = time.time()
    how_long = end - start
    if token_count > 1 and how_long > 0:
        print()
        print(f"Tokens/s：{(token_count-1) / how_long}")


def talk(msg):
    global ctext
    ctext.append({"role":"user","content":msg})
    while len(ctext) > 11:
        ctext = [ctext[0]] + ctext[-10:]
    full_answer = ""
    for chunk in generate_response(msg=ctext, temperature=tmpt, max_tokens=max_tokens, top_p=top_p):
        print(chunk, end="", flush=True)
        full_answer += chunk
    print()
    ctext.append({"role":"assistant","content":full_answer})

    with open(".md","w",encoding="utf-8") as f:
        f.write(full_answer)
    tool.MD_to_HTML()
    return full_answer

def main():
    while True:
        pmt = input(">")
        if pmt == "MD_TO_HTML":
            tool.MD_to_HTML()
            continue
        if pmt == "LaTeX":
            LaTex = input("LaTeX:")
            tool.render_from_text(LaTex,"./")
            continue
        talk(pmt)

if __name__ == "__main__":
    main()