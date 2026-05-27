# 기존의 FROM openjdk:17-jdk-slim 줄을 아래로 교체합니다.
FROM eclipse-temurin:17-jdk-alpine

WORKDIR /app
# 빌드된 jar 파일을 컨테이너로 복사 (빌드를 먼저 수행해야 합니다)
COPY build/libs/*-SNAPSHOT.jar app.jar
ENTRYPOINT ["java", "-jar", "app.jar"]