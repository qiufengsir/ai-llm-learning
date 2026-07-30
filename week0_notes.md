# 第 0 周学习笔记：环境搭建到底做了什么

> 目的：把"傻嘟嘟替我跑通的环境"变成"我自己能讲清、能重做"的知识。
> 对应计划：《三个月AI学习计划》"第 0 周：前置环境与账号"。

---

## 一、这一周到底在干嘛（先建立大局观）

Week 0 **不学任何 AI 知识**，它是一道"前置工序"：在正式开课（Week 1）之前，把开发环境装好、平台账号注册好、最后跑通一次推理验证。

逻辑很朴素：学 AI/LLM 时最崩溃的不是知识难，而是环境出问题（装不上包、GPU 不识别、模型下载不了）。这些问题如果在 Week 1 才遇到，会浪费大量时间。所以 Week 0 先把这些都搞定，**最后的 `pipeline("text-generation")` 验证就是"毕业考试"**——跑通 = 全链路（Python + PyTorch + transformers + 模型下载）都 OK。

---

## 二、环境清单：每个工具是干嘛的

| 工具 | 是什么 | 为什么需要 | 验证命令 |
|------|--------|-----------|---------|
| **Python + venv** | AI/ML 通用语言；venv 是项目级依赖隔离 | 每个项目独立依赖空间，避免版本冲突 | `python --version` |
| **Git** | 代码版本管理 | 记录改动、协作、回退；作品集靠它提交 | `git --version` |
| **CUDA 驱动** | NVIDIA GPU 并行计算平台 | 深度学习训练/推理加速（CPU 慢几十倍） | `nvidia-smi`（看到卡） |
| **Docker** | 应用+依赖打包成容器 | 生产部署必会，避免"我电脑能跑、服务器报错" | `docker --version` |
| **HuggingFace** | AI 界"GitHub"，托管开源模型/数据集 | 后续每周都要下载/加载模型 | `huggingface-cli whoami` |
| **GitHub** | 代码托管 | 作品集容器 + 协作展示 | `git push` 成功 |
| **pipeline 验证** | transformers 高级 API，一行加载模型做生成 | 验证全链路通了 | 见下 |

---

## 三、我们实际执行的步骤（可复现）

### 步骤 1：创建 Python 虚拟环境（隔离依赖）
```bash
# 在 AI 学习项目目录下建 venv（用 Python 3.11，ML 社区标准版本）
python -m venv C:\Users\user\ai-llm-learning\venv
```
- **为什么要 venv**：系统的 Python 可能被其他软件占用，直接 `pip install` 会污染全局。venv 给本项目一个干净独立的"房间"。
- **为什么选 3.11**：torch 官方对 3.11 支持最充分（踩坑后从 3.13 降下来的，见第四节）。

### 步骤 2：在 venv 内安装核心依赖
```bash
C:\Users\user\ai-llm-learning\venv\Scripts\pip.exe install torch transformers
```
- `torch` = PyTorch，深度学习框架底层
- `transformers` = HuggingFace 的模型加载/推理库

### 步骤 3：配置 Git 身份（否则 commit 报错）
```bash
git config --global user.name "qiufengsir"
git config --global user.email "15196771992@139.com"
```

### 步骤 4：生成 SSH 密钥并连 GitHub
```bash
# 生成密钥对（私钥留本机，公钥给 GitHub）
ssh-keygen -t ed25519 -C "15196771992@139.com" -f C:\Users\user\.ssh\id_ed25519 -N ""
# 把 C:\Users\user\.ssh\id_ed25519.pub 的内容粘贴到 https://github.com/settings/ssh/new
ssh-keyscan -H github.com >> C:\Users\user\.ssh\known_hosts   # 避免 host key 报错
ssh -T git@github.com   # 验证，看到 "successfully authenticated" 即通
```

### 步骤 5：初始化本地仓库并推送
```bash
cd C:\Users\user\ai-llm-learning
git init
git remote add origin git@github.com:qiufengsir/ai-llm-learning.git
git add .gitignore verify_week0.py
git commit -m "Week0: env setup + pipeline verification script"
git branch -M main
git push -u origin main
```

### 步骤 6：跑通推理验证（毕业考试）
```bash
cd C:\Users\user\ai-llm-learning
.\venv\Scripts\python.exe verify_week0.py
```
- 输出 `GENERATED: ...` + `PIPELINE_OK` = 通关。
- 首次运行会下载 gpt2 模型（约 500MB）。

---

## 四、你亲自踩过的坑（这是真经验，比成功更重要）

### 坑 1：PowerShell 禁止运行 .ps1 → `activate` 失败 → `ModuleNotFoundError: torch`
- **现象**：`.\venv\Scripts\activate` 报 "无法加载...禁止运行脚本"；随后 `python` 用了系统 Python（没 torch）。
- **根因**：Windows 默认 PowerShell 执行策略不允许跑 `.ps1` 脚本。
- **解法（二选一）**：
  1. **不激活，直接调 venv 的 python**（推荐）：
     ```powershell
     .\venv\Scripts\python.exe verify_week0.py
     ```
  2. 或放开执行策略（仅当前用户）：`Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`，之后 `.\venv\Scripts\activate` 就能用。

### 坑 2：.bat 文件中文乱码 → 双击报错
- **现象**：双击 `run_verify.bat` 报一堆乱码命令（"櫒""閫€鍑虹爜"）。
- **根因**：`.bat` 用 UTF-8 存了中文，但 `cmd` 默认按 GBK 读，中文变乱码被当成命令执行。
- **解法**：批处理文件**只用纯英文/ASCII**（已重写 `run_verify.bat`）。

### 坑 3（我的环境，与你无关）：agent 沙箱加载不了 torch 原生库
- 我这边执行命令的沙箱环境对 torch 的 C++ 扩展段错误（多版本×多 Python 全崩，但 numpy 正常）。这是**我运行环境的限制，不是你机器的问题**。所以验证脚本最终在你真机跑通——这是正确的。

---

## 五、怎么自己从零重做（复习用，遮住上面自己写）

1. `python -m venv <项目路径>\venv`
2. `<venv>\Scripts\pip.exe install torch transformers`
3. `git config --global user.name/email` 配置
4. `ssh-keygen` 生成密钥 → 公钥贴 GitHub → `ssh -T git@github.com` 验证
5. `git init` → `remote add` → `add/commit/push`
6. `.\venv\Scripts\python.exe verify_week0.py` 跑通

---

## 六、与计划 checklist 的差距（待办，不是已完成）

| 计划要求（第 378 行） | 现状 | 处理 |
|----------------------|------|------|
| `torch.cuda.is_available()` 应为 **True** | 当前 **False**（venv 是 CPU 版 torch） | 你真机有 RTX 5060 Ti（Blackwell 架构），需装 **CUDA 版 torch ≥ 2.8** 才能激活 GPU。Week 0 的 pipeline 用 CPU 能过，但计划期望 GPU 通 → **留到用 GPU 时再做** |
| vLLM 安装 | 未装 | vLLM 是周 3 部署工具且吃 GPU，现在 CPU 装没意义 → **推迟到周 3** |

> 结论：Week 0 的"跑通推理"目标达成；"GPU 验证"和"vLLM"是后续周次的事，不阻塞当前进度。

---

## 七、下一步：Week 1（原理 + PyTorch 最小必要集）

计划周 1-2：Transformer 原理 + PyTorch（理解级）。
- Karpathy《micrograd》+《Let's build GPT》建立直觉
- PyTorch 最小集：Tensor / autograd / nn.Module / 训练循环 / DataLoader
- **交付物**：亲手训练字符级 mini-GPT + 200 字《我理解的注意力机制》

从这一周起，**代码由你写，我陪练**。
