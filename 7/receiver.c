#include<sys/types.h>
#include<sys/stat.h>
#include<sys/fcntl.h>
#include<sys/socket.h>
#include<string.h>
#include<netinet/in.h>
#include<unistd.h>
#include<stdio.h>
#include<stdlib.h>

#define BUFSIZE 512
#define WINDOW 10
#define TIMEOUT 4
#define PORTNO 13000

typedef struct hdr{

  int seq;
  int ack;
  short int control;	 // control=0 -- data packet , 1 -- ack packet

}hdr;



typedef struct mypack{
 
  hdr header; 
  char data[BUFSIZE];

}packet;



int main(){

int sockfd,fd,status,recbytes,currbyte,writebyte,prevbyte,numpack,sequence,acknowledge,totpack;
struct sockaddr_in saddr,paddr;
packet Tpack;

saddr.sin_family=AF_INET;
saddr.sin_addr.s_addr=INADDR_ANY;
saddr.sin_port=htons(PORTNO);


sockfd=socket(AF_INET,SOCK_DGRAM,0); // create a new dgram socket
while(bind(sockfd,(struct sockaddr*)&saddr,sizeof(saddr))==-1)printf("socket_bind_unsuccessful__\n"); // bind  to port
printf("socket_binded__\n");



status = sizeof(struct sockaddr);

recbytes = recvfrom(sockfd, (void*)&Tpack, sizeof(packet), 0,(struct sockaddr *)&paddr, &status);

//printf("here\n");

sequence=1; // sequence number of packets
numpack=0;
acknowledge=0;

fd = open("downloaded.txt",O_WRONLY|O_TRUNC|O_CREAT,S_IRWXU); // open file


//printf("here1\n");

while(recbytes !=0 ){

   if(Tpack.header.control==1){
                                Tpack.header.ack=-1;
                                sendto(sockfd, (void*)&Tpack, sizeof(packet), 0,(struct sockaddr *)&paddr,sizeof(struct sockaddr));
                                 break;
                               }

   if(sequence == Tpack.header.seq){
    
    acknowledge=sequence;
   
   // printf("%s\n",Tpack.data );

    write(fd,Tpack.data,strlen(Tpack.data));

    sequence++;

  
   }

   numpack++;

   if(numpack == WINDOW){
    
    numpack=0;
    //Tpack.header.control = 1;
    Tpack.header.ack = acknowledge;

    sendto(sockfd, (void*)&Tpack, sizeof(packet), 0,(struct sockaddr *)&paddr,sizeof(struct sockaddr));
    
    printf("ack=%d next_seq_%d\n",acknowledge, sequence);

   }

   status=sizeof(struct sockaddr);

   
   recbytes = recvfrom(sockfd,(void*)&Tpack, sizeof(packet), 0,(struct sockaddr *)&paddr, &status);
   
   
   printf("recbytes=%d\n",recbytes);

}

close(sockfd);
close(fd);


return 0;

}


