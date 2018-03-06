# Serveless (Lambda + API Gateway + ACM + ROUTE 53 + RDS)

## Requisitos:
* Conta na AWS
* Credenciais de acesso da API
* AWS CLI instalado
* python
* pip
* virtualenv

Instalar AWS CLI
```bash
$ pip install awscli --upgrade --user
```

@TODO
Adicionar credenciais da AWS API

Crie a instancia RDS
```bash
$ aws rds create-db-instance \
    --db-instance-identifier NomeDaInstancia \
    --db-instance-class db.t2.micro \
    --engine MySQL \
    --allocated-storage 5 \
    --no-publicly-accessible \
    --db-name DbName \
    --master-username DbUserName \
    --master-user-password DbPassword \
    --backup-retention-period 3
```

Para ter o endpoint da instancia (mostrará mais de uma linha caso tenha outras instâncias criadas)
```bash
$ aws rds describe-db-instances --query "DBInstances[*].Endpoint.Address"
```

@TODO
Criar certificado

@TODO
Para ter o arn do certificado

@TODO
Criar entrada no Route 53


Clone o projeto
```bash
$ git clone https://github.com/Gamboua/lambda_flask_zappa.git
```

Altere o arquivo de configuração com as variáveis do banco
```bash
$ vim rds_config.py
    + host='nomedainstancia.us-east-1.rds.amazonaws.com'
    + base='DbName'
    + user='DbUserName'
    + pswd='DbPassword'
```

Crie um virtualenv
```bash
$ virtualenv .env
$ source .env/bin/activate
```

Instale o requirements
```bash
$ pip install -r requirements.txt
```

Inicie o zappa
```bash
$ zappa init

Welcome to Zappa!

Zappa is a system for running server-less Python web applications on AWS Lambda and AWS API Gateway.
This `init` command will help you create and configure your new Zappa deployment.
Let's get started!

Your Zappa configuration can support multiple production stages, like 'dev', 'staging', and 'production'.
What do you want to call this environment (default 'dev'): dev

AWS Lambda and API Gateway are only available in certain regions. Let's check to make sure you have a profile set up in one that will work.
Okay, using profile default!

Your Zappa deployments will need to be uploaded to a private S3 bucket.
If you don't have a bucket yet, we'll create one for you too.
What do you want call your bucket? (default 'zappa-jki6aho7x'): project-zappa-beta

It looks like this is a Flask application.
What's the modular path to your app's function?
This will likely be something like 'your_module.app'.
We discovered: app.app
Where is your app's function? (default 'app.app'): app.app

You can optionally deploy to all available regions in order to provide fast global service.
If you are using Zappa for the first time, you probably don't want to do this!
Would you like to deploy this application globally? (default 'n') [y/n/(p)rimary]: n

Okay, here's your zappa_settings.json:

{
    "dev": {
        "app_function": "app.app", 
        "aws_region": "us-east-1", 
        "profile_name": "default", 
        "project_name": "flask-lambda", 
        "runtime": "python2.7", 
        "s3_bucket": "project-zappa-beta"
    }
Adicione a entrada certificate_arn e domain
    + "certificate_arn": "arn:aws:acm:us-east-1:1231230:certificate/6asdasdasda",
    + "domain": "nomedodominio.com.br"

}

Does this look okay? (default 'y') [y/n]: y

Enjoy!,
 ~ Team Zappa!
```

Adicione a entrada certificate_arn e domain
$ vim zappa_settings.json
    + "certificate_arn": "arn:aws:acm:us-east-1:1231230:certificate/6asdasdasda",
    + "domain": "nomedodominio.com.br"

Faça o deploy
```bash
$ zappa deploy dev
```

Pegar o id d APIG
```bash
$ aws apigateway get-rest-apis --query "items[0].id"
```

Adicione entrada no base path do APIG
```bash
$ aws apigateway create-base-path-mapping --domain-name api.pimentagabriel.com.br --rest-api-id ApiId --stage dev
```
