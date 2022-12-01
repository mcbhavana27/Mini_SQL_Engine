echo "\n\n select * from table1;"
sh 2019101100.sh "select * from table1;"

echo "\n\n select A,C,E from table1,table2;"	
sh 2019101100.sh "select A,C,E from table1,table2;"							

echo "\n\n select sum(B) from table1;" 							
sh 2019101100.sh "select sum(B) from table1;" 							

echo "\n\n select avg(E) from table2;" 								
sh 2019101100.sh "select avg(E) from table2;" 								

echo "\n\n select distinct A,B from table1;"							
sh 2019101100.sh "select distinct A,B from table1;"							
echo "\n\n select distinct A,B,F from table1,table2;"  					
sh 2019101100.sh "select distinct A,B,F from table1,table2;"  					

echo "\n\n select A,B from table1 where A< 0 and B <=300;" 				
sh 2019101100.sh "select A,B from table1 where  A< 0 and B <=300;"


echo "\n\n select A,E from table1,table2 where A >300 or B < 14;" 			
sh 2019101100.sh "select A,E from table1,table2 where A >300 or B < 14;" 			

echo "\n\n select A,min(B),avg(E) from table1,table2 group by A;" 					
sh 2019101100.sh "select A,min(B),avg(E) from table1,table2 group by A;" 	


echo "\n\n select C from table1 group by C;" 						
sh 2019101100.sh "select C from table1 group by C;" 						

echo "\n\n select A from table1 order by A DESC;" 					
sh 2019101100.sh "select A from table1 order by A DESC;"


echo "\n\n select A,E from table1,table2 order by A ASC;" 				
sh 2019101100.sh "select A,E from table1,table2 order by A ASC;" 				

echo "\n\n select A,min(C) from table1,table2 group by A order by COUNT(B);" 				
sh 2019101100.sh "select A,min(C) from table1,table2 group by A order by COUNT(B);" 				


echo "\n\n select A,min(C) from table1,table2 group by A order by COUNT(B) DESC" 				
sh 2019101100.sh "select A,min(C) from table1,table2 group by A order by COUNT(B) DESC;" 				



echo "\n\n select distinct A,min(C) from table1,table2 group by A order by COUNT(B);" 				
sh 2019101100.sh "select distinct A,min(C) from table1,table2 group by A order by COUNT(B);" 				


echo "\n\n select distinct A,min(C) from table1,table2 group by A order by COUNT(B) DESC" 				
sh 2019101100.sh "select distinct A,min(C) from table1,table2 group by A order by COUNT(B) DESC" 				



echo "\n\n select A,sum(B) from table1 where A < 5 group by A order by A;" 		
sh 2019101100.sh "select A,sum(B) from table1 where A < 5 group by A order by A;" 		

error handling:
echo "\n\n select * from table4;" 					
sh 2019101100.sh "select * from table4;" 					
echo "\n\n select e from table1;"			
sh 2019101100.sh "select e from table1;"			
echo "\n\n select A,sum(B) from table1;"			
sh 2019101100.sh "select A,sum(B) from table1;"			
echo "\n\n select A,B from table1 were a < 5;" 			
sh 2019101100.sh "select A,B from table1 were a < 5;" 			
echo "\n\n select A,B from table1 group by a;" 
sh 2019101100.sh "select A,B from table1 group by a;"