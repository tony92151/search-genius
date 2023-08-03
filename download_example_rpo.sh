mkdir -p ./repo
git clone https://github.com/langchain-ai/langchain.git --branch v0.0.240 ./repo/langchain

cd ./repo/langchain/libs/langchain
ctags -R .