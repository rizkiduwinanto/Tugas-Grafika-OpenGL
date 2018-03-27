make:
	g++ Car1.cpp -o grafika9 -lGL -lGLU -lglut -Wall
	g++ Car2.cpp -o grafika9 -lGL -lGLU -lglut -Wall -lGLEW

run :
	./grafika9

clean :
	rm -rf grafika9
