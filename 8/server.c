#include<sys/types.h>
#include<sys/stat.h>
#include<sys/fcntl.h>
#include<sys/socket.h>
#include<string.h>
#include<netinet/in.h>
#include<unistd.h>
#include<stdio.h>
#include<stdlib.h>


//initializing port numbers
#define BUFSIZE 1200
#define WINDOW 1
#define TIMEOUT 4
#define SERV_PORTNO 12000


//header structure
typedef struct hdr{

  int seq;
  int ack;
  // control=0 -- data packet , 1 -- ack packet
  short int control;	 

}hdr;


//packet structure
typedef struct mypack{
 
  hdr header; 
  char data[BUFSIZE];

}packet;



int main(){
char table[200][1000];
int vis[100],i;
int sockfd,fd,status,recbytes,currbyte,writebyte,prevbyte,numpack,sequence,acknowledge,totpack,pushid=0,pullid=0;
struct sockaddr_in saddr,paddr;
packet Tpack;

for(i=0;i<100;i++) vis[i]=100;
saddr.sin_family=AF_INET;
saddr.sin_addr.s_addr=INADDR_ANY;
saddr.sin_port=htons(SERV_PORTNO);

// create a new dgram socket
sockfd=socket(AF_INET,SOCK_DGRAM,0);
// bind  to port
while(bind(sockfd,(struct sockaddr*)&saddr,sizeof(saddr))==-1)printf("socket_bind_unsuccessful__\n"); 
printf("socket_binded__\n");

while(1){

status = sizeof(struct sockaddr);

recbytes = recvfrom(sockfd, (void*)&Tpack, sizeof(packet), 0,(struct sockaddr *)&paddr, &status);


if(Tpack.header.control==0)
{



// sequence number of packets
sequence=1; 
numpack=0;
acknowledge=0;
//recbytes=1;


while(recbytes!=0){

   if(Tpack.header.control==1){
                               // Tpack.header.ack=-1;
                                //sendto(sockfd, (void*)&Tpack, sizeof(packet), 0,(struct sockaddr *)&paddr,sizeof(struct sockaddr));
                                 break;
                               }

   if(sequence == Tpack.header.seq){
    
    acknowledge=sequence;
   
    strcpy(table[pushid],Tpack.data);

    sequence++;

  
   }

   numpack++;

   if(numpack == WINDOW){
    
    numpack=0;
    //Tpack.header.control = 1;
    Tpack.header.ack = acknowledge;

    sendto(sockfd, (void*)&Tpack, sizeof(packet), 0,(struct sockaddr *)&paddr,sizeof(struct sockaddr));
    


   }

   status=sizeof(struct sockaddr);

   
   recbytes = recvfrom(sockfd,(void*)&Tpack, sizeof(packet), 0,(struct sockaddr *)&paddr, &status);
   
   


}

close(sockfd);

vis[pushid]=1;
pushid++;


}
else if(Tpack.header.control==-1)
{
// sequence number of packets
sequence=1; 
numpack=0;
acknowledge=0;



while(recbytes!=0 ){

   if(Tpack.header.control==1){
                               // Tpack.header.ack=-1;
                                //sendto(sockfd, (void*)&Tpack, sizeof(packet), 0,(struct sockaddr *)&paddr,sizeof(struct sockaddr));
                                 break;
                               }
Tpack.header.control=pullid;

   numpack++;

   if(numpack == WINDOW){
    
    numpack=0;
    //Tpack.header.control = 1;
    Tpack.header.ack = acknowledge;

    sendto(sockfd, (void*)&Tpack, sizeof(packet), 0,(struct sockaddr *)&paddr,sizeof(struct sockaddr));
    


   }
status = sizeof(struct sockaddr);

recbytes = recvfrom(sockfd, (void*)&Tpack, sizeof(packet), 0,(struct sockaddr *)&paddr, &status);

close(sockfd);

vis[pushid]=1;
pushid++;
}
if(Tpack.header.control==0)
{



// sequence number of packets
sequence=1; 
numpack=0;
acknowledge=0;



while(1 ){

   if(Tpack.header.control==1){
                               // Tpack.header.ack=-1;
                                //sendto(sockfd, (void*)&Tpack, sizeof(packet), 0,(struct sockaddr *)&paddr,sizeof(struct sockaddr));
                                 break;
                               }

   if(sequence == Tpack.header.seq){
    
    acknowledge=sequence;
   
    strcpy(table[pushid],Tpack.data);

    sequence++;

  
   }

   numpack++;

   if(numpack == WINDOW){
    
    numpack=0;
    //Tpack.header.control = 1;
    Tpack.header.ack = acknowledge;

    sendto(sockfd, (void*)&Tpack, sizeof(packet), 0,(struct sockaddr *)&paddr,sizeof(struct sockaddr));
    


   }

   status=sizeof(struct sockaddr);

   
   recbytes = recvfrom(sockfd,(void*)&Tpack, sizeof(packet), 0,(struct sockaddr *)&paddr, &status);
   
   


}

close(sockfd);

vis[pushid]=1;
pushid++;

}
}

}
return 0;

}


