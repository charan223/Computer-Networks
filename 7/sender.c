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
#define RECV_PORTNO 13000
#define SEND_PORTNO 12000
#define RECV_IP "10.5.18.101"


typedef struct hdr
{
   int seq;
   int ack;
  short int control;
 
}hdr;



typedef struct mypack{
 
  hdr header; 
  char data[BUFSIZE];

}packet;



int main(){

int PKBOF[12];
int sockfd,fd,status,recbytes,currbyte,readbyte,prevbyte,numpack,sequence,acknowledge,totpack,i;
char filename[100];
struct sockaddr_in saddr,paddr;
struct timeval tv;
fd_set readfds;
packet Tpack;


scanf("%s",filename); // send filename



tv.tv_sec = TIMEOUT;

saddr.sin_family=AF_INET;
saddr.sin_addr.s_addr=INADDR_ANY;
saddr.sin_port=htons(SEND_PORTNO);

paddr.sin_family=AF_INET;
paddr.sin_addr.s_addr=inet_addr(RECV_IP);
paddr.sin_port=htons(RECV_PORTNO);



sockfd=socket(AF_INET,SOCK_DGRAM,0); // create a new dgram socket
while(bind(sockfd,(struct sockaddr*)&saddr,sizeof(saddr))==-1)printf("socket_bind_unsuccessful__\n"); // bind  to port
printf("socket_binded__\n");

totpack=0;
numpack=0; // number of packets sent
prevbyte=0; // prev start from 0th byte
sequence=1; // sequence number of packets
acknowledge=0;
currbyte=0;


//PKBOF[1] = 0;

fd = open(filename,O_RDONLY); // open file
readbyte = read(fd,Tpack.data,BUFSIZE);

//printf("here\n");

while(acknowledge!=-1){


printf("totpack_%d\n",totpack);
// construct a packet and send w packets

Tpack.header.seq = sequence;
Tpack.header.control = 0; // indicate a data packet

PKBOF[numpack+1]=currbyte;

currbyte+=readbyte; // start from currbyte th byte
sequence++;

//printf("%s\n",Tpack.data );
sendto(sockfd,(void*)&Tpack, sizeof(Tpack) , 0,(struct sockaddr *)&paddr, sizeof(struct sockaddr));

numpack++;
totpack++;



//PKBOF[numpack + 1] = currbyte;

// wait for ack after sending w packets

if(numpack == WINDOW){

    numpack=0;

    FD_ZERO(&readfds);
    FD_SET(sockfd,&readfds);
    select(sockfd+1, &readfds, NULL,NULL, &tv);
    
    for(i=1; i< sockfd+1; i++){ //i=1 beacuse we ignore STDIN

      if(FD_ISSET(i,&readfds))break;

    }

    if(i == sockfd+1){
      // if no ack till timeout -- resend from previous packet window
      // timeout happened
      // send from prev window-- totpack-WINDOW th packet
    	printf("TIMEOUT\n");
      totpack-=WINDOW;
      currbyte = prevbyte;
      sequence=totpack+1;
      //seek file to prev byte and proceed;
      lseek(fd,prevbyte,SEEK_SET);

    }
    else if(i == sockfd){
     // if receive ack update seq num accordingly
     status = sizeof(struct sockaddr);
     recvfrom(sockfd,(void*)&Tpack, sizeof(Tpack) , 0,(struct sockaddr *)&paddr,&status );
     acknowledge = Tpack.header.ack;
     
        if(acknowledge==-1)break;
    // if acknowledge = totpack proceed asusual
    // else send from packet acknowledge + 1

      if(totpack == acknowledge){
               
               prevbyte = currbyte;

      }

      else if(totpack != acknowledge){

           totpack = acknowledge;

           numpack = (totpack%WINDOW);

           prevbyte = PKBOF[numpack+1];
           currbyte = prevbyte; 
           sequence=totpack+1;
           // seek file to prevbyte and proceed
          lseek(fd,prevbyte,SEEK_SET);

      }

    printf("ack_recvd=%d seqsending=%d\n",acknowledge,sequence);


    }

    

}




readbyte = read(fd,Tpack.data,BUFSIZE);
if (readbyte<BUFSIZE)Tpack.data[readbyte]='\0';

if(readbyte == 0 ){
Tpack.header.control=1;
sendto(sockfd,(void*)&Tpack, sizeof(Tpack) , 0,(struct sockaddr *)&paddr, sizeof(struct sockaddr));
}


if(readbyte==-1)break;
printf("readbyte=%d\n",readbyte );


}



close(sockfd);
close(fd);

return 0;

}


