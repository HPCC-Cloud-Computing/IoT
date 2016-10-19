FROM jamesdbloom/docker-java7-maven:latest

COPY org.eclipse.om2m /usr/src/org.eclipse.om2m

COPY ./org.eclipse.om2m.sample.ipe.test_2 /usr/src/workspace

COPY ./start-cse.sh /usr/src

COPY ./start-mn-cse.sh /usr/src

WORKDIR /usr/src/

#COPY docker-entrypoint.sh /

#RUN chmod +x /docker-entrypoint.sh

#ENTRYPOINT ["/docker-entrypoint.sh"]

#CMD ["start_cse"]


