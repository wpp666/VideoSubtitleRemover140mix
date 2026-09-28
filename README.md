# Video Subtitle Remover v1.4.0 + CUDA(GPU 版)

基于开源项目 [YaoFANGUK/video-subtitle-remover](https://github.com/YaoFANGUK/video-subtitle-remover) 的 v1.4.0 源码,内置嵌入式 Python + CUDA 构建方案,使 **Windows + NVIDIA 显卡** 环境下可享受 v1.4.0 的新界面与功能,同时让去字幕核心(修补 / OCR / 帧插值)真正跑在 GPU 上。

> 官方 v1.4.0 只提供 CPU 安装包;本仓库把 GPU 能力以「嵌入式 Python + CUDA torch」的方式补回,保留 v1.4.0 完整源码。

---

## 为什么有这个仓库

- 官方最近发布 v1.4.0 只打包了 **CPU 版**(CUDA 加速在 requirements 中被注释)。
- 但 v1.4.0 源码本身完整支持 CUDA(`backend/tools/hardware_accelerator.py` 会检测 `torch.cuda.is_available()`)。
- 因此只要换用 **CUDA 版 torch**,即得到「新功能 + GPU 加速」的完整组合。
- 本仓库基于 **嵌入式 Python 3.12.10**,整套绿色便携、不污染系统注册表、不占系统 Python。

---

## 环境要求

| 项目 | 要求 |
|---|---|
| 系统 | Windows 10/11 x64 |
| NVIDIA 显卡 | 需支持 CUDA 12.8(30 系/40 系等),推荐显存 ≥ 6GB |
| 驱动 | 支持 CUDA 12.8 即可(R520+),无需额外装 CUDA Toolkit |
| 磁盘 | 至少 10GB 可用空间 |

---

## 快速开始

### 1. 构建环境(仅第一次)

```bat
python setup_cuda_env.py
```

脚本会自动:
1. 下载并解压 **嵌入式 Python 3.12.10**
2. 安装 pip 到环境内
3. 安装 v1.4.0 全部核心依赖(paddleocr 3.4 + paddlepaddle 3.2.2 + PySide6 等)
4. 安装 **CUDA 版 torch 2.7.0+cu128** 与 torchvision(约 3GB,耗时较长)
5. 自动校验 GPU 识别

### 2. 启动

```bat
start_official_cuda.bat
```

或在资源管理器中双击 `start_official_cuda.bat`。

> 首次使用某个功能时,程序会自动下载对应的 OCR / 修补模型权重到 `backend/models/`,需联网,首次会等待片刻。

---

## 目录结构

```
├── backend/               # 核心逻辑(OCR / 修补 / 场景检测 / 硬件加速)
├── ui/                    # PySide6 Fluent 界面
├── design/                # 图标等资源
├── config/  test/         # 配置与测试
├── gui.py                 # 程序入口
├── requirements.txt       # v1.4.0 官方依赖清单
├── setup_cuda_env.py      # 一键构建嵌入式 Python + CUDA 环境
└── start_official_cuda.bat# Windows 启动脚本
```

> 本仓库刻意**不包含**:Python 解释器与 site-package 二进制、torch 权重、模型权重、ffmpeg 可执行文件。它们由 `setup_cuda_env.py` 构建 / 首次运行自动下载,以保持仓库轻量。

---

## 工作原理(硬件加速)

`backend/tools/hardware_accelerator.py` 启动时会探测:

- **CUDA** → `torch.cuda.is_available()` → 设备 `cuda:0`(NVIDIA)
- **DirectML** → `torch_directml`(Windows 通用 GPU)
- **MPS** → Apple 芯片

装好 CUDA 版 torch 后,程序自动以 GPU 模式运行,修补(ProPainter/STTN/LAMA)与帧插值走 CUDA。

---

## 常见问题

**Q: 启动后如何确认在用 GPU?**
A: 界面「设置」中查看「硬件加速」是否开启;或在终端观察 `Creating video... ` 时是否有 `cuda:0` 字样。

**Q: 显卡显存较小(6GB)跑得动吗?**
A: 可以,系统内存需 ≥ 16GB,模型按需分块加载。

**Q: 能换更新的 torch 吗?**
A: 可以,将 `setup_cuda_env.py` 里的 `torch==2.7.0` 改为其它 cu128 版本即可(保持 torchvision 版本同步)。

---

## 许可证

遵循上游项目 [YaoFANGUK/video-subtitle-remover](https://github.com/YaoFANGUK/video-subtitle-remover) 的许可证。