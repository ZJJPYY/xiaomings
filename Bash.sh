# 1. 建立 Git 追踪
git init

# 2. 纳入版本控制暂存区
git add main.py requirements.txt

# 3. 提交变更并附着工程化描述
git commit -m "feat: implement dual-agent adversarial review pipeline for legal contracts"

# 4. 主干分支对齐
git branch -M main

# 5. 绑定远端锚点 (必须替换为你创建的空仓库地址)
git remote add origin https://github.com/YourUsername/JurisMAS.git

# 6. 推送至远端主干
git push -u origin main