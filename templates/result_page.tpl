<!DOCTYPE html>

<html>

<header>
    <meta http-equiv="Content-type" content="text/html"; charset="UTF-8">
    <link rel="icon" href="./assets/image/icon.ico">
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
    % if len(words_count) > 1:
    <div class="column">    
        <table id="results">
            <tr>
                <th>Words Breakdown</th>
            <tr>
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
    
    % if history:
    <div class="column">
        <table id="history">
            <tr>
                <th>Search History</th>
            <tr>
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