<html>
    <head>
        <title>Brevet Times</title>
    </head>

    <body>
        <h1>Brevet Times</h1>
	
        <ul>
            <?php
            $all = file_get_contents('http://laptop-service/listAll');
            $obj = json_decode($all);
	    $listAllOpen = $obj->open_time;
	    $listAllClose = $obj->close_time;
            //echo "listAll var: ";
            echo "listAll-Open Times:\n";
            foreach ($listAllOpen as $opentime) {
		echo "<li>$opentime</li>";
	    }
		
	    echo "listAll-Close Times:\n";
            foreach ($listAllOpen as $closetime) {
                echo "<li>$closetime</li>";
            }
	     
               


	    $all_json = file_get_contents('http://laptop-service/listAll/json');
	    $obj1 = json_decode($all_json);
            $AlljsonOpen = $obj1->open_time;
            $AlljsonClose = $obj1->close_time;
            
           
	    echo "listAll/json-Open Times:\n";
            foreach ($AlljsonOpen as $opentime1) {
		echo "<li>$opentime1</li>";
	    }

            echo "listAll/json-Close Times:\n";
            foreach ($AlljsonOpen as $closetime1) {
                echo "<li>$opentime1</li>";
            }


	    
            $open_json = file_get_contents('http://laptop-service/listOpenOnly/json');
            $obj3 = json_decode($open_json);
            $OPENjson = $obj3->open_time;

	    echo "listOpenOnly/json- Open Times:\n";
            foreach ($OPENjson as $opentime3) {
		echo "<li>$opentime3</li>";
	    }
	  
	    


            $close_json = file_get_contents('http://laptop-service/listCloseOnly/json');
	    $obj4 = json_decode($close_json);
            $CLOSEjson = $obj4->close_time;

	    echo "listCloseOnly/json -Close Times:";
            foreach ($CLOSEjson as $closetime3) {
		echo "<li>$closetime3</li>";
	    }
	
	    echo "listAll/csv:\n";
            echo file_get_contents('http://laptop-service/listAll/csv');

	    echo "\nlistOpenOnly/csv-Open Times:\n";
	    echo file_get_contents('http://laptop-service/listOpenOnly/csv');
	    echo "\n";
	  

	    echo "\nlistCloseOnly/csv-Close Times:\n";
	    echo file_get_contents('http://laptop-service/listCloseOnly/csv');
	    echo "\n";
	
            ?>
        </ul>
    </body>
</html>
