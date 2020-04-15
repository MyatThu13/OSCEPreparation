#include <stdio.h>
#include <stdlib.h>
#define password "p!g30n"
#define lame "password"

checkpw (){
char pw[600];
	printf("Please enter the password: ");
	gets (pw);
	if (strcmp(pw, lame) == 0)
		printf("Oh come on now you ankle biter!\n");
	else if (strcmp(pw, password) == 0)
		granted();
	else
		printf("Access Denied!\n");
	
	return 0;
}

granted(){
	printf("Access Granted\n");
	return 0;
}

int main(int argc, char *argv[])
{
	if(argc >1){
		printf("There is no help menu or usage information.\n");
		exit(1);}
	checkpw();
	return 0;
}