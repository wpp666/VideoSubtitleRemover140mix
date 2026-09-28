# -*- coding: utf-8 -*-
"""
v1.4.0 + CUDA 一键构建脚本
用法:  python setup_cuda_env.py
在编译机/目标机上重建与本仓库一致的嵌入式 Python + CUDA(torch cu128)运行环境。
产物: 当前的 python312.* / Lib / Scripts(嵌入式环境),可直接配合 start_official_cuda.bat 启动。
"""
import os, sys, subprocess, zipfile, urllib.request, io

ROOT = os.path.dirname(os.path.abspath(__file__))
PY_VER = "3.12.10"
EMBED_URL = f"https://www.python.org/ftp/python/{PY_VER}/python-{PY_VER}-embed-amd64.zip"
GETPIP_URL = "https://bootstrap.pypa.io/get-pip.py"
TORCH_INDEX = "https://download.pytorch.org/whl/cu128"

def sh(cmd, **kw):
    print(">", " ".join(cmd) if isinstance(cmd, list) else cmd)
    subprocess.check_call(cmd, **kw)

def setup_embed_python():
    """1) 下载并解压嵌入式 Python(若已存在则跳过)"""
    if os.path.exists(os.path.join(ROOT, "python.exe")):
        print("[skip] python.exe 已存在")
        return
    print("[1/5] 下载嵌入式 Python", PY_VER)
    req = urllib.request.Request(EMBED_URL, headers={"User-Agent": "Mozilla/5.0"})
    data = urllib.request.urlopen(req, timeout=120).read()
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        z.extractall(ROOT)
    # 打开 site 支持并添加依赖目录
    pth = os.path.join(ROOT, f"python{PY_VER.split('.')[0]}{PY_VER.split('.')[1]}._pth")
    if os.path.exists(pth):
        with open(pth, "w", encoding="utf-8") as f:
            f.write(f"python{PY_VER.split('.')[0]}{PY_VER.split('.')[1]}.zip\n.\n./Lib\n./Lib/site-packages\n./DLLs\nimport site\n")
    os.makedirs(os.path.join(ROOT, "Lib", "site-packages"), exist_ok=True)
    os.makedirs(os.path.join(ROOT, "DLLs"), exist_ok=True)
    print("[1/5] 嵌入式 Python 就绪")

def install_pip():
    """2) 安装 pip 到环境内"""
    print("[2/5] 安装 pip")
    py = os.path.join(ROOT, "python.exe")
    req = urllib.request.Request(GETPIP_URL, headers={"User-Agent": "Mozilla/5.0"})
    urllib.request.urlretrieve(GETPIP_URL, os.path.join(ROOT, "get-pip.py"))
    subprocess.check_call([py, os.path.join(ROOT, "get-pip.py"), "--no-warn-script-location"],
                          cwd=ROOT)

def pip_install(args):
    py = os.path.join(ROOT, "python.exe")
    subprocess.check_call([py, "-m", "pip", "install", *args, "--no-warn-script-location"], cwd=ROOT)

def install_deps():
    """3) 安装 v1.4.0 requirements(以库形式继承, 模型权重由首次运行自动下载)"""
    print("[3/5] 安装 v1.4.0 核心依赖")
    pip_install([
        "filesplit==3.0.2", "opencv-python==4.11.0.86", "scikit-image==0.25.2",
        "tqdm==4.67.1", "pyside6-fluent-widgets==1.7.7", "numpy==2.2.5",
        "av==17.0.0", "einops==0.8.1", "paddleocr==3.4.0", "matplotlib", "Pillow",
        "scipy", "requests", "darkdetect", "je-showinfilemanager==1.1.6a4",
        "paddlepaddle==3.2.2",
    ])

def install_torch_cuda():
    """4) 安装 CUDA 版 torch + torchvision(核心 GPU 加速)"""
    print("[4/5] 安装 torch/torchvision (cu128, 约 3GB, 耗时较长)")
    py = os.path.join(ROOT, "python.exe")
    subprocess.check_call([py, "-m", "pip", "install", "torch==2.7.0",
                           "--index-url", TORCH_INDEX, "--no-warn-script-location"], cwd=ROOT)
    subprocess.check_call([py, "-m", "pip", "install", "torchvision==0.22.0",
                           "--index-url", TORCH_INDEX, "--no-warn-script-location"], cwd=ROOT)

def verify():
    """5) 校验 GPU 识别"""
    print("[5/5] 校验 CUDA")
    py = os.path.join(ROOT, "python.exe")
    code = ("import torch;print('torch',torch.__version__);"
            "print('has_cuda',torch.cuda.is_available());"
            "print('device',torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'N/A')")
    subprocess.check_call([py, "-c", code], cwd=ROOT)
    print("全部完成! 双击 start_official_cuda.bat 启动。首次使用会自动下载 OCR/修补模型。")

if __name__ == "__main__":
    setup_embed_python()
    install_pip()
    install_deps()
    install_torch_cuda()
    verify()