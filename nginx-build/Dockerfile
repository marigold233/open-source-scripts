FROM centos:6.6

ADD https://ghproxy.com/https://raw.githubusercontent.com/marigold233/scripts-test/main/CentOS-Base.repo /etc/yum.repos.d/CentOS-Base.repo
RUN yum install -y gcc gcc-c++ make tar perl wget \
    && yum clean all
COPY nginx-builder.sh /nginx-builder.sh
RUN chmod u+x /nginx-builder.sh
ENTRYPOINT [ "/nginx-builder.sh" ]

