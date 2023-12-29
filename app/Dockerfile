FROM openjdk:11-jre-slim

WORKDIR /metabase

COPY ./dados_to_web.db /metabase

RUN apt-get update && apt-get install -y wget

RUN wget -O metabase.jar https://downloads.metabase.com/v0.48.0/metabase.jar

EXPOSE 3000

# Comando para iniciar o Metabase
CMD ["java", "-jar", "metabase.jar"]
