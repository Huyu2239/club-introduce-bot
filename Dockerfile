FROM python:3.11-alpine

# codeというディレクトリを作成し、そこを作業フォルダとする
WORKDIR /code

#デバッグモードON
ENV FLASK_ENV: 'development'   

# alpineのおまじない
RUN apk add --no-cache gcc musl-dev linux-headers

# requirements.txtをcode内に移動
COPY requirements.txt requirements.txt
# requirements.txtの中のライブラリをinstallする
RUN pip install -U pip==23.3.1
RUN pip install -r requirements.txt

# すべてのファイルをcode内にマウントする。
COPY . .

# $PORTを指定しないと動かないので注意
CMD gunicorn -b 0.0.0.0:$PORT app:app --log-file=-
