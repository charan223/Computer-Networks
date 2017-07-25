#include<sys/types.h>
#include<sys/socket.h>
#include<string.h>
#include<netinet/in.h>
#include<unistd.h>
#include<stdio.h>
#include<stdlib.h>

#define LEN 5 

int main(){


int sockfd,newsockfd,status,portno=12000,recbytes,id,sb,i,mi;
struct sockaddr_in saddr,caddr,tempaddr;

char buf[1000];
char file[10][30];
char ip[10][30];


strcpy(file[0],"6.pdf");
strcpy(file[1],"vid.mp4");
strcpy(file[2],"1.c");
strcpy(file[3],"2.pdf");
strcpy(file[4],"1.pdf");




strcpy(ip[0],"10.5.18.101");
strcpy(ip[1],"10.5.18.101");
strcpy(ip[2],"10.102.73.237");
strcpy(ip[3],"10.102.73.237");
strcpy(ip[4],"10.102.73.237");




saddr.sin_family=AF_INET;
saddr.sin_addr.s_addr=INADDR_ANY;
saddr.sin_port=htons(portno);


sockfd=socket(AF_INET,SOCK_DGRAM,0);


while(bind(sockfd,(struct sockaddr*)&saddr,sizeof(saddr))==-1)printf("socket_bind_unsuccessful__\n");


printf("socket_binded__\n");


while(1){

        printf("listening\n");

       // memset(&(caddr),0,sizeof(caddr));
 
       // memset(buf,0,1000*sizeof(char));

        status=sizeof(struct sockaddr);
         

        recbytes=recvfrom(sockfd,buf,sizeof(buf),0,(struct sockaddr*)&caddr,&status);


 id=fork();

 if (id==0){

        if(recbytes==0){
	           printf("connection_closed_from _client__unable_to_receive\n");
                        }
        else{
     
            buf[recbytes]='\0';
       
                 for(mi=0;mi<LEN;mi++){

                         if(strcmp(buf,file[mi])==0){
            
                  i=0;
                 sb=sendto(sockfd,ip[mi],strlen(ip[mi]),0,(struct sockaddr*)&caddr,status);
                 if(sb==-1)printf("couldn't_send_response\n");
                 while(sb==-1){

                       sb=sendto(sockfd,ip[mi],strlen(ip[mi]),0,(struct sockaddr*)&caddr,status);                             

                       i=i+1;
                       if(i>5000)break;
                              }
                 if(sb!=-1)printf("response_sent\n");
                           break;
                    
                                    }


                           }


              


              if(mi==LEN){
                         printf("file_destip_not_found\n");
                           }
                 }

    exit(0);

}



}

return 0;
}
