# Hemera MVP

一个基于 [Hemera Indexer](https://github.com/HemeraProtocol/hemera-indexer) 的轻量级 MVP 实现。

## 项目简介

本项目是 Hemera Protocol 官方索引器的精简版本，旨在提供核心索引功能的最小可行产品（MVP）实现。通过简化架构和功能，让开发者能够快速理解和部署区块链数据索引服务。

## 主要特性

- 🚀 **轻量级架构** - 精简的代码结构，易于理解和维护
- 📊 **核心索引功能** - 保留了最重要的区块链数据索引能力
- 🔧 **简化配置** - 最小化配置要求，快速启动
- 🎯 **专注核心** - 移除了复杂的企业级功能，专注于核心索引逻辑

## 系统要求

- Python 3.8+
- PostgreSQL 12+
- Redis (可选)
- 足够的存储空间用于区块链数据

## 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/gududefengzhong/hemera_mvp.git
cd hemera_mvp
```

### 2. 安装依赖

```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
```

### 3. 配置数据库

```bash
# 创建数据库
createdb hemera_mvp

# 运行数据库迁移
python manage.py migrate
```

### 4. 配置环境变量

创建 `.env` 文件：

```bash
cp .env.example .env
```

编辑 `.env` 文件，配置以下参数：

```env
# 数据库配置
DATABASE_URL=postgresql://user:password@localhost:5432/hemera_mvp

# RPC 节点配置
ETH_RPC_URL=https://your-ethereum-rpc-endpoint

# 索引配置
START_BLOCK=0
BATCH_SIZE=100
```

### 5. 启动索引器

```bash
python main.py
```

## 配置说明

### 基础配置

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `DATABASE_URL` | PostgreSQL 连接字符串 | 必填 |
| `ETH_RPC_URL` | 以太坊 RPC 节点地址 | 必填 |
| `START_BLOCK` | 开始索引的区块高度 | 0 |
| `BATCH_SIZE` | 批处理大小 | 100 |
| `LOG_LEVEL` | 日志级别 | INFO |

### 高级配置

详细配置选项请参考 `config/settings.py` 文件。

## 项目结构

```
hemera_mvp/
├── config/           # 配置文件
├── indexer/          # 核心索引逻辑
├── models/           # 数据模型
├── utils/            # 工具函数
├── tests/            # 测试文件
├── main.py          # 主入口
└── requirements.txt # 依赖列表
```

## API 使用

### 查询区块数据

```python
from hemera_mvp import BlockIndexer

indexer = BlockIndexer()
block_data = indexer.get_block(block_number=12345)
```

### 查询交易数据

```python
tx_data = indexer.get_transaction(tx_hash="0x...")
```

## 与原项目的区别

| 特性 | Hemera Indexer | Hemera MVP |
|------|----------------|------------|
| 多链支持 | ✅ | ❌ (仅支持以太坊) |
| 企业级特性 | ✅ | ❌ |
| 复杂查询 | ✅ | 部分支持 |
| 性能优化 | 高度优化 | 基础优化 |
| 代码复杂度 | 高 | 低 |

## 开发指南

### 运行测试

```bash
pytest tests/
```

### 代码风格

```bash
# 格式化代码
black .

# 检查代码风格
flake8 .
```

## 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建您的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的修改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启一个 Pull Request

## 路线图

- [ ] 支持更多区块链网络
- [ ] 添加 WebSocket 支持
- [ ] 优化索引性能
- [ ] 添加更多查询接口
- [ ] 完善文档

## 许可证

本项目基于 [Apache License 2.0](LICENSE) 开源。

## 致谢

- 感谢 [Hemera Protocol](https://github.com/HemeraProtocol) 团队的优秀工作
- 本项目是学习和理解 Hemera Indexer 的简化实现

## 联系方式

- 作者：gududefengzhong
- 项目地址：https://github.com/gududefengzhong/hemera_mvp
- Issues：https://github.com/gududefengzhong/hemera_mvp/issues

---

**注意**：这是一个 MVP 版本，不建议在生产环境中使用。如需生产级别的索引器，请使用官方的 [Hemera Indexer](https://github.com/HemeraProtocol/hemera-indexer)。
