set -e
export environment=$1
PATH=$PWD/venv/bin:/usr/local/bin:$PATH
echo Running npm install to install serverless if needed

npm install
echo Running serverless deploy to deploy package to AWS Lambda
./node_modules/serverless/bin/serverless deploy --stage test
