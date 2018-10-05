<!DOCTYPE html>

<html>

<header>
    <meta http-equiv="Content-type" content="text/html"; charset="UTF-8">
    <title>Our Search Engine. </title>
    <link rel="stylesheet" type="text/css" href="./assets/css/result_page.css">
</header>

<body>

<div class="search_bar">
<form id="search_form" action="/" method="post" >
    <input id="input_box" name="keywords" type="text" placeholder=" Where's waldoge? ">            
    <input id="search_button" value="Waldoge Search" type="submit">
</form>

</div>


<h1> <a id="font1">Search for <a id="keyword_font">"{{keywords}}"  </h1>


<div class="row">
    <div class="column">
       <h2>Words Breakdown</h2>
        % if len(words_count) > 1:
        <table id=”results”>
            <tr id="tr1">
                <td id="td1">Word</td>
                <td id="td2">Count</td>
            </tr>
            % for word in words_count:
            <tr id="tr2">
                <td id="td1">{{word}}</td>
                <td id="td2">{{words_count[word]}}</td>
            </tr>
            %end
        </table>
        %end
    </div>

    
    <div class="column">
    % if history:
        <h2> Search History</h2>
        <table id=”history_table”>
            <tr id="tr1">
                <td id="td1">Keywords</td>
                
                <td id="td2">Times Searched</td>
            </tr>
            % for entry in history:
            <tr id="tr2">
                <td id="td1">{{entry[0]}}</td>
                
                <td id="td2">{{entry[1][0]}}</td>
            </tr>
            %end
        </table>
        %end
    </div>
    

</div>

</body>

</html>