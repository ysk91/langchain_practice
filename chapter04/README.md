## RAG

### 基本的な流れ

1. Document loader: データソースからドキュメントを読み込む
1. Document transformer: ドキュメントを変換する
1. Embedding model: ドキュメントをベクトル化する
1. Vector store: ベクトル化したドキュメントの保存先
1. Retriever: 入力のテキストと関連するドキュメントを検索する

### Chroma

- ローカルで使用可能なVector store
- LangChainでは、以下のVector storeが使用可能
  - Chroma
  - Faiss
  - ElasticSearch
  - Redis
