<!DOCTYPE html>

<html>

<header>
    <meta http-equiv="Content-type" content="text/html"; charset="UTF-8">
    <link rel="icon" href="./assets/image/icon.ico">
    <title>{{keywords}} - Waldoge Search</title>
    <link rel="stylesheet" type="text/css" href="./assets/css/result_page.css">
     <link rel="stylesheet" type="text/css" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css">
    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js" integrity="sha384-ZMP7rVo3mIykV+2+9J3UJ46jBk0WLaUAdn689aCwoqbBJiSnjAK/l8WvCWPIPm49" crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/js/bootstrap.min.js" integrity="sha384-ChfqqxuZUCnJSK3+MXmPNIyE6ZbWh2IMqE241rYiqJxyMiZ6OW/JmZQ5stwEULTy" crossorigin="anonymous"></script>
</header>

<body>
    <!-- if user has not logged in, display the log_in button -->
    % if login == False:
    <form id="login_form" action="/login/result" method="get">
        <input id="login_button" class="btn btn-info btn-lg" value="Log in" type="submit">
    </form>
    <!-- if user has logged in, display the user email, user name... -->
    %else:
    <form id="login_form">
        <button id="user_email" type="button" class="btn btn-info btn-lg" 
                data-toggle="modal" data-target="#logout_modal">{{user_email}}</button>
    </form>
    %end

    <!-- form with a input box and a search button -->
    <div class="search_bar">
        <form id="search_form" action="/" method="post" >
            <input id="input_box" name="keywords" type="text" placeholder=" Here he is! Type here to do another search. ">            
            <input id="search_button" value="Waldoge Search" type="submit">

            %if login and history:
                %length=len(history)
                %print "length: "+repr(length)
            <table id="topSearchedTable">
                <tr>
                    <th colspan="{{length}}" style="font-size:20px">Top Searched Words</th>
                </tr> 
                <tr>
                %for entry in history:
                    %print entry[0]
                    <th>{{entry[0]}}</th>
                %end
                </tr>
            </table>
             %end

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
        % if login and history:
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

    %if login:
     <!-- log out modal --> 
    <form action="/logout" method="get">
    <div class="modal" id="logout_modal" tabindex="-1" role="dialog">
    <div class="modal-dialog" role="document">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title">{{user_email}}</h5>
        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
          <span aria-hidden="true">&times;</span>
        </button>
      </div>
      <div class="modal-body">
        <p>{{user_email}}</p>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
        <button type="submit" class="btn btn-primary">Sign out</button>
      </div>
    </div>
    </div>
    </div>
    </form>
    %end
</body>

</html>