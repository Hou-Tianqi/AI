# AI
## 可以深度自定义的欸！拿个.gguf文件过来就能用的欸！
现在我们假设你已经有了一个.gguf的文件（ai.py里的model列表里）
models文件夹我不会上传，因为它太大了，你可以自己去找一个，比如[魔塔](https://www.modelscope.cn/)或者[Hugging Face](https://huggingface.co/)

在根目录下新建一个名叫modles的文件夹，把.gguf文件放进去，然后到ai.py里的第7行，改成你自己文件的名字，然后到第10行，改成model\[0\]

默认是开启性能测试的，每一次对话都会输出Tokens/s。
有4套调教，默认、日常、写作、代码，默认是代码模式
各种参数和系统Prompt都可以自己调

附带有两个功能：markdown转HTML，LaTeX公式渲染成矢量图，因为AI的回答里经常出现这些东西

如果你现在没有选好一个模型的话，我推荐一个对硬件要求小的，拿来就能用：[Qwen3.5-4B-GGUF](https://www.modelscope.cn/models/unsloth/Qwen3.5-4B-GGUF/files)
也可以在这里面选一个：
[千问3.5系列](https://www.modelscope.cn/models?name=Qwen3.5-GGUF&page=1&tabKey=task)