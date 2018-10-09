<!DOCTYPE html>

<html>

<header>
    <meta http-equiv="Content-type" content="text/html"; charset="UTF-8">
    <link rel="icon" href="./assets/image/icon.ico">
    <title>{{keywords}} - Waldoge Search</title>
    <link rel="stylesheet" type="text/css" href="./assets/css/result_page.css">
</header>

<body>
    <!-- form with a input box and a search button -->
    <div class="search_bar">
        <form id="search_form" action="/" method="post" >
            <input id="input_box" name="keywords" type="text" placeholder=" Here he is! Type here to do another search. ">            
            <input id="search_button" value="Waldoge Search" type="submit">
        </form>
    </div>

    <h1> <a id="font1">Search for <a id="keyword_font">"{{keywords}}"  </h1>

    <div class="row">        
        <!-- if a phrase is submitted, list the number od keywords in the pharse and 
            the number of apperances for each keyword in the pharse 
        -->
        % if len(words_count) > 1 or next(iter(words_count.values())) > 1:
        <div class="column">    
            <table id="results">
                <tr>
                    <th id="th1" colspan="2" style="font-size:20px">Words Breakdown</th>
                </tr> 
                <tr>
                    <th>Word</th>
                    <th>Count</th>
                </tr>
                % for word in words_count:
                <tr>
                    <td>{{word}}</td>
                    <td>{{words_count[word]}}</td>
                </tr>
                %end
            </table>
        </div>
        %end

        <!--Display the top 20 keywords on the query page, 
            and the total number of times that these words have been searched.
        -->
        % if history:
        <div class="column">                
            <table id="history">
                <tr>
                    <th colspan="2" style="font-size:20px">Search History</th>
                </tr>
                <tr>
                    <th>Keywords</th>
                    <th>Times Searched</th>
                </tr>
                % for entry in history:
                <tr>
                    <td>{{entry[0]}}</td>                
                    <td>{{entry[1][0]}}</td>
                </tr>
                %end
            </table>    
        </div>
        %end
    </div>
</body>

</html>