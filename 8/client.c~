#include<sys/types.h>
#include<sys/stat.h>
#include<sys/fcntl.h>
#include<sys/socket.h>
#include<string.h>
#include<netinet/in.h>
#include<unistd.h>
#include<stdio.h>
#include<stdlib.h>

#define BUFSIZE 1200
#define WINDOW 1
#define TIMEOUT 4
#define CLI_PORTNO 13000
#define SERV_PORTNO 12000
#define SERV_IP "127.0.0.1"


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



int sockfd,fd,status,recbytes,readbyte,numpack,sequence,acknowledge,i,id;
char message[1024],ipaddr[100],password[100];
struct sockaddr_in saddr,paddr;
struct timeval tv;
fd_set readfds;
packet Tpack;



int action;
printf("1 for push 2 for pull 0 for exit\n");
scanf("%d",&action);
				tv.tv_sec = TIMEOUT;

				saddr.sin_family=AF_INET;
				saddr.sin_addr.s_addr=INADDR_ANY;
				saddr.sin_port=htons(CLI_PORTNO);

				paddr.sin_family=AF_INET;
				paddr.sin_addr.s_addr=inet_addr(SERV_IP);
				paddr.sin_port=htons(SERV_PORTNO);

while(1)
{

if(action==1)
{

				printf("Give the ipaddr\n");
				scanf("%s",ipaddr);



				sockfd=socket(AF_INET,SOCK_DGRAM,0); // create a new dgram socket
				while(bind(sockfd,(struct sockaddr*)&saddr,sizeof(saddr))==-1)printf("socket_bind_unsuccessful__\n"); // bind  to port
				printf("socket_binded__\n");

				numpack=0; // number of packets sent
				sequence=1; // sequence number of packets
				acknowledge=0;


				printf("Enter the message\n");
				scanf("%s",message);
				strcpy(Tpack.data,message);
				Tpack.data[strlen(message)]='\0';
				strcat(message,": :");
				strcat(message,ipaddr);
				//PKBOF[1] = 0;

				//fd = open(filename,O_RDONLY); // open file
				//readbyte = read(fd,Tpack.data,BUFSIZE);

				//printf("here\n");
				//readbyte=strlen(Tpack.data);
				while(acknowledge!=1){


				//printf("totpack_%d\n",totpack);
				// construct a packet and send w packets

				Tpack.header.seq = sequence;
				Tpack.header.control = 0; // indicate a data packet

				sendto(sockfd,(void*)&Tpack, sizeof(Tpack) , 0,(struct sockaddr *)&paddr, sizeof(struct sockaddr));

				numpack++;
				
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
						sequence=1;
					  strcpy(Tpack.data,message);
					}
					else if(i == sockfd){
					 // if receive ack update seq num accordingly
					 status = sizeof(struct sockaddr);
					 recvfrom(sockfd,(void*)&Tpack, sizeof(Tpack) , 0,(struct sockaddr *)&paddr,&status );
					 acknowledge = Tpack.header.ack;
					 
						if(acknowledge==-1)break;
					// if acknowledge = totpack proceed asusual
					  else
					  {
					  sequence=1;
					  strcpy(Tpack.data,message);
					  }
					}
				}

				}
				readbyte=1;
				while(readbyte!=0){
				
				Tpack.header.control=1;
				sendto(sockfd,(void*)&Tpack, sizeof(Tpack) , 0,(struct sockaddr *)&paddr, sizeof(struct sockaddr));
				status=sizeof(struct sockaddr);
				readbyte=recvfrom(sockfd,(void*)&Tpack, sizeof(Tpack) , 0,(struct sockaddr *)&paddr, &status);

}

				close(sockfd);



}
else if(action==2)
{

	if(id==-1)	{
	Tpack.header.control=-1;

	sockfd=socket(AF_INET,SOCK_DGRAM,0); // create a new dgram socket
				while(bind(sockfd,(struct sockaddr*)&saddr,sizeof(saddr))==-1)printf("socket_bind_unsuccessful__\n"); // bind  to port
				printf("socket_binded__\n");

				numpack=0; // number of packets sent
				sequence=1; // sequence number of packets
				acknowledge=0;


				//printf("here\n");
				//readbyte=strlen(Tpack.data);
				while(acknowledge!=-1){
					Tpack.header.control=-1;
					Tpack.header.seq=1;
				sendto(sockfd,(void*)&Tpack, sizeof(Tpack) , 0,(struct sockaddr *)&paddr, sizeof(struct sockaddr));

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
						//sequence=1;

					}
					else if(i == sockfd){
					 // if receive ack update seq num accordingly
					 status = sizeof(struct sockaddr);
					 recvfrom(sockfd,(void*)&Tpack, sizeof(Tpack) , 0,(struct sockaddr *)&paddr,&status );
					 acknowledge = Tpack.header.ack;
					 
						if(acknowledge==1)break;
				


					}





				}
				   				id=Tpack.header.control;
				readbyte=1;
				while(readbyte!=0){
				
				Tpack.header.control=1;
				sendto(sockfd,(void*)&Tpack, sizeof(Tpack) , 0,(struct sockaddr *)&paddr, sizeof(struct sockaddr));
				status=sizeof(struct sockaddr);
				readbyte=recvfrom(sockfd,(void*)&Tpack, sizeof(Tpack) , 0,(struct sockaddr *)&paddr, &status);

}

				close(sockfd);

	printf("logging %d\n",id);

	
	
	}
	
}
else if(action==0)
return 0;
else continue;

}




return 0;

}


