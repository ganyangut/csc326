<header>
    <h1>Search for "{{keywords}}"</h1>
</header>

<table id=”results”>
    <tr>
        <td>Word</td>
        <td>Count</td>
    </tr>
% for word in words_count:
    <tr>
        <td>{{word}}</td>
        <td>{{words_count[word]}}</td>
    </tr>
% end
</table>

<header>
    <h2>Search history:</h2>
</header>

<table id=”history”>
    <tr>
        <td>Keywords</td>
        <td>Times Searched</td>
    </tr>
% for entry in history:
    <tr>
        <td>{{entry[0]}}</td>
        <td>{{entry[1][0]}}</td>
    </tr>
% end
</table>