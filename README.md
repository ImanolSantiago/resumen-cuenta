# Resumen de cuenta
## Descripción
### Base del proyecto
El proyecto busca ser una base, y un buen ejemplo de como desarrollar un proyecto de AWS. Contemplando el desarrollo y "emualcion" local, su deploy a AWS, como describir la arquitectura mediante CloudFormation. El testing correspondiente mediante, Flake8 y Pytest, como correrlos automaticamente mediante GitHub Actions. Y el flujo e implementacion del CI/CD.

### Requerimientos tecnicos de la aplicacion
A partir de un archivo .csv (con el DNI del usuario, y un periodo de tiempo) que se carga en un bucket de S3, se debe generar un PDF con la lista de movimientos bancarios del usuario en el periodo de tiempo dado y enviar dicho PDF por mail al usuario correspondiente.

## Ejecutar el proyecto


## Nomenclatura:
Iaas: Infrastructure as a service
AWS CLI: Command Line Interface https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-welcome.html 
AWS SAM: Serverless Application Model   https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html
CloudFormation: Plantilla que describe la infraestructura de nuestro proyecto en forma de codigo.https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-whatis-howdoesitwork.html


Contexto
AWS CLI: Basicamente nos permite interactuar con los servicios de AWS pero desde una consola en vez de consola web de AWS.

AWS SAM: Basicamente nos permite atraves de un archivo de Cloudformation tanto simular localmente (mediante Docker) como desplegar nuestra infraestructura.

Como construir una plantilla de CloudFormaion: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-specification.html