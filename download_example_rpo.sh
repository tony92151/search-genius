
if [ ! -d "./repo" ]; then
    mkdir -p ./repo
fi

# if filder ./repo/langchain not exists, clone it else do nothing
if [ ! -d "./repo/langchain" ]; then
    git clone https://github.com/langchain-ai/langchain.git --branch v0.0.330 ./repo/langchain 
fi

cd ./repo/langchain/libs/langchain

# if os is darwin (mac) do this
if [[ "$OSTYPE" == "darwin"* ]]; then
    # find whether /opt/homebrew/Cellar/universal-ctags/*/bin/ctags exists
    export ctags_=$(find /opt/homebrew/Cellar/universal-ctags -name ctags)
    # if ctags_ exists, use it
    if [[ -n "$ctags_" ]]; then
        echo Use $ctags_
        $ctags_ -R .
    else
        echo "ctags not found, please install ctags"
    fi  
else
    ctags -R .
fi