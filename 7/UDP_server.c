#include<sys/types.h>
#include<sys/stat.h>
#include<sys/fcntl.h>
#include<sys/socket.h>
#include<string.h>
#include<netinet/in.h>
#include<stdio.h>

int main(){


int sockfd,newsockfd,status,portno=12000,recbytes,file,rb;
struct sockaddr_in saddr,caddr;

char filename[1000],buf[1000];


saddr.sin_family=AF_INET;
saddr.sin_addr.s_addr=INADDR_ANY;
saddr.sin_port=htons(portno);


sockfd=socket(AF_INET,SOCK_DGRAM,0);


while(bind(sockfd,(struct sockaddr*)&saddr,sizeof(saddr))==-1)printf("socket_bind_unsuccessful__\n");


printf("socket_binded__\n");


while(1){

newsockfd=sockfd;

status=sizeof(caddr);

recbytes=recvfrom(newsockfd,filename,1000,0,(struct sockaddr*)&caddr,&status);

//printf("receiving\n");

if(recbytes==0){
	printf("connection_closed_by_peer_client\n");
               }
else{
     
     filename[recbytes]='\0';
     
     file=open(filename,O_RDONLY);
     
     printf("%s received\n",filename );

     rb=read(file,buf,1000);
     
     sendto(newsockfd,buf,rb,0,(struct sockaddr*)&caddr,sizeof(struct sockaddr));
     
     while(rb!=0){
         
         rb=read(file,buf,1000);
     
         sendto(newsockfd,buf,rb,0,(struct sockaddr*)&caddr,sizeof(struct sockaddr));

     }
    
    printf("file_sent_successfully\n");
    
    }

}


return 0;
}