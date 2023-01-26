#include <iostream>
#include <conio.h>
#include <windows.h>
using namespace std;

bool gameOver;
const int width = 30, height = 20;

int snakX, snakY;
int eggX, eggY, score = 0;
int tailX[100], tailY[100];
int nTail;

enum eDirection{
	STOP = 0,
	LEFT,
	RIGHT,
	UP,
	DOWN
};
eDirection dir;

void getNewEggs(){
	
	do{
		eggX = rand() % width;
	}while( eggX == 0 );

	do{
		eggY = rand() % height;
	}while( eggY == 0 );
}

void setup(){
	gameOver = false;
	dir = STOP;
	snakX = width /2;	//	Initially, Snake is in middle
	snakY = height /2;
	getNewEggs();
}

void draw(){

	// system( "cls" );
	//	Overrites the text in console
	SetConsoleCursorPosition(GetStdHandle(STD_OUTPUT_HANDLE), {0,0}); 

	for (int row = 0; row < height; ++row){
		cout << "#";
		
		for (int col = 1; col < width -1; ++col){
			if( row == 0 || row == height -1 )
				cout << "#";

			else if( row == snakY && col == snakX )
				cout << "<";

			else if( row == eggY && col == eggX )
				cout << "e";

			else{
				bool tag = true;

				for (int k = 0; k < nTail; ++k){
					
					if( tailX[ k ] == col && tailY[ k ] == row ){
						cout << "o";
						tag = false;
					}
				}

				if( tag )
					cout << " ";
			}
		}

		cout << "#" << endl;
	}
	cout << "Score: " << score << endl;

	cout << "snakX: " << snakX << ", " << "snakY: " << snakY << endl;
	cout << "eggX: " << eggX << ", " << "eggY: " << eggY << endl<< endl;
	// cout << "tailX: ";
 //    for( int i = 0; i < nTail; i++ )
 //        cout << tailX[ i ] << ", " ;
 //    cout << endl;
 //    cout << "tailY: ";
 //    for( int i = 0; i < nTail; i++ )
 //        cout << tailY[ i ] << ", ";
 //    cout << endl;
}

void input(){

	if( _kbhit() ){	//	Checks if keyboard key is pressed or not

		switch( _getch() )	//	returns the ASCII val of pressed key
		{
			case 'w':	dir = UP;
						break;

			case 'a':	dir = LEFT;
						break;

			case 's':	dir = DOWN;
						break;

			case 'd':	dir = RIGHT;
						break;

			case 'q':	gameOver = true;
						break;
		}
	}
}

void logic(){

//  Shift the co-ordinates of tail & add new head at 0,0

    for( int i = nTail -1; i >= 0; i-- ){
        tailX[ i +1 ] = tailX[ i ];
        tailY[ i +1 ] = tailY[ i ];
    }
    tailX[0] = snakX;
    tailY[0] = snakY;

//	Snake's direction of movement
	switch( dir )
	{
		case LEFT:	snakX--;
					break;

		case RIGHT:	snakX++;
					break;

		case UP:	snakY--;
					break;

		case DOWN:	snakY++;
					break;

		default:
        			break;
	}

//	GameOver if Snake hits a wall
/*
	if( snakX < 0 || snakX > width || snakY < 0 || snakY > height )
		gameOver = true;
*/

//	Magical Boundaries
	if( snakX < 0 )				snakX = width -1;
	if( snakX >= width )		snakX = 0;
	
	if( snakY < 0 )				snakY = height -1;
	if( snakY >= height )		snakY = 0;

//	Snake Captures an EGG
	if( snakX == eggX && snakY == eggY ){

		score += 1;
		nTail++;
		getNewEggs();
	}

//	Snake eats itself
	for (int i = 0; i < nTail; ++i)	{
		
		if( tailX[ i ] == snakX && tailY[ i ] == snakY ){
			draw();
			gameOver = true;
		}
	}
}

int main(int argc, char const *argv[]){
	
	setup();
	while( !gameOver ){

		draw();
		input();
		logic();
		Sleep( 100 );	//	Speed of snake
		// gameOver = true;
	}

	return 0;
}


