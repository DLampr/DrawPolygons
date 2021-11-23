# DrawPolygons
This little program handles files of txts with coordinates for polygons and outputs a shapefile with all the polygons drawn. 
All the coordinates in the txts must be in order for the polygon to be drawn correctly.

It has three functions.
-loadTxts asks for the folder where all the txts are in. Then creates a list with the paths of all the txts.
-check_Txts checks if all the coordinates can convert to float and if not raises an error. It shows in which particular file (txt) the
 error occured and specifically in which row of the file so that we can correct it.
 
 Change a value in the example txts like this --> 4,4a66561.12,4268072.93 to see what happens (you can also see the error picture).

-DrawPolygons (if no ValueError is raised) takes the list of txt paths and outputs a shapefile with all the polygons (from all the txts)
 in it. It also creates two additional columns with the area of each polygon and the filename of each polygon. This could be useful 
 if all the txts where named after a unique code number which could also be a foreign key for another table or info.
 
The program was inspired as a use case for hundreds of txts created in the Greek Cadastre e-service "Θέαση ορθοφωτογραφιών" which could
be named after a specific unique code number ("κωδικός ιδιοκτησίας") and linked to every other available information.
