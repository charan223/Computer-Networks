#include<sys/types.h>
#include<sys/socket.h>
#include<string.h>
#include<netinet/in.h>
#include<stdio.h>
#include<stdlib.h>
#include<fcntl.h>
#include<sys/stat.h>
#include<unistd.h>

#define SERVER_IP "10.146.5.34"
#define SERVER_PORT 12000

int main(){


int sockfd,newsockfd,status,recbytes,fd;
struct sockaddr_in serv_addr,peer_addr;

char buf[1000],file[1000];
strcpy(file,"FIS_Server.c");

serv_addr.sin_family=AF_INET;
serv_addr.sin_addr.s_addr=inet_addr(SERVER_IP);
serv_addr.sin_port=htons(SERVER_PORT);


sockfd=socket(AF_INET,SOCK_DGRAM,0);

//printf("sending_file_name\n");

while(sendto(sockfd,file,strlen(file),0,(struct sockaddr*)&serv_addr,sizeof(struct sockaddr))==-1)printf("send_error\n");

//printf("sending_file_name\n");

status=sizeof(serv_addr);

recbytes=recvfrom(sockfd,buf,1000,0,(struct sockaddr*)&serv_addr,&status);

//printf("sending_file_name\n");

if(recbytes==0){

    printf("connection_closed_by_server\n");
}
else{

fd=open("newfile.c",O_WRONLY|O_TRUNC|O_CREAT,S_IRWXU);
write(fd,buf,recbytes);

while(recbytes!=0){

status=sizeof(peer_addr);
recbytes=recvfrom(sockfd,buf,1000,0,(struct sockaddr*)&serv_addr,&status);
write(fd,buf,recbytes);

}


printf("download_successful\n");
close(sockfd);
close(fd);

}


return 0;
}