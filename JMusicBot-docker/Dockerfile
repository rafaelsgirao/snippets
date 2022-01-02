FROM openjdk:11
# Note: get this jar yourself, place it here
# https://github.com/jagrosh/MusicBot/releases/
COPY ./JMusicBot.jar /musicbot
WORKDIR /musicbot
RUN adduser jmusicbot --no-create-home --quiet --disabled-login --gecos ""
#RUN addgroup -S jmusicbot && adduser -S jmusicbot -G jmusicbot
RUN chown -R jmusicbot:jmusicbot /musicbot
VOLUME ["/config"]
USER jmusicbot
CMD ["java", "-Dconfig=/config/config.txt", "-Dnogui=true", "-jar", "JMusicBot.jar"]
