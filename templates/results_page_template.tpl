<!DOCTYPE html>

<html>
<header>
     <meta http-equiv="Content-type" content="text/html"; charset="UTF-8">
    <title>Our Search Engine. </title>
    <link rel="stylesheet" type="text/css" href="./assets/css/homepage.css">

</header>

<body>

<div id="content">
        <h1> <font id="font1">Search for </font> <font id="keyword_font">"{{keywords}}" </font> </h1>

% if len(words_count) > 1:
<table id=”results”>
    <tr id="tr1">
        <td id="td1">Word</td>
        <td id="td2">Count</td>
    </tr>
% for word in words_count:
    <tr id="tr2">
        <td id="td1">{{word}}</td>
        <td id="td1">{{words_count[word]}}</td>
    </tr>
%end
</table>
%end

<div id="search_history">

<h2>Search history:</h2>
<table id=”history_table”>
    <tr>
        <td>Keywords</td>
        <td></td>
        <td>Times Searched</td>
    </tr>
% for entry in history:
    <tr>
        <td>{{entry[0]}}</td>
        <td></td>
        <td>{{entry[1][0]}}</td>
    </tr>
%end
</table>
</div>

</body>
</html>