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
        <td>No.</td>
        <td>Keywords</td>
    </tr>
% for number in range(history.qsize()):
    <tr>
        <td>{{number+1}}</td>
        <td>{{history.get()}}</td>
    </tr>
% end
</table>