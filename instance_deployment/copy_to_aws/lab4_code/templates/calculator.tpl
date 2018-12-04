<!DOCTYPE HTML>
<html lang="en-US">

<head>

    <!-- Code By Saleh Ibne Omar, used HTML5 CSS3 JS BOOTSTRAP3 -->
    <!-- reference from "https://code.sololearn.com/Ww9mr0y2h0QG/#html" -->
    <meta charset="UTF-8">
    <title>Waldoge Calculator</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap-theme.min.css" integrity="sha384-rHyoN1iRsVXV4nD0JutlnGaslCJuC7uwjduW9SVrLvRYooPp2bWYgmgJQIXwl/Sp" crossorigin="anonymous">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
    <link rel="stylesheet" href="/assets/css/calculator.css">
</head>

<body>
    <a href="/" id="home-button" class="btn btn-primary">Home</a>
    <h1>Waldoge Calculator</h1>
    <div class="container">
        <div class="row saleh">
            <div class=" col-xs-12  col-sm-offset-4 col-sm-12  col-md-offset-3 col-md-6  col-lg-offset-3 col-lg-6  ">
                <form name="form" class="well calcontainer col-xs-12  col-sm-offset-4 col-sm-12  col-md-offset-3 col-md-6  col-lg-offset-3 col-lg-6">

                    <!-- panel for the calc -->
                    <input class=" form-control " id="panel" name="panel" value={{calculation_result}} disabled)><br/>
                    
                    <!-- User Input Buttons for the calc -->
                    <input class="form-group btn btn-default bttn" type="button" name="bttn7" value="7" onclick="calC(bttn7.value);">
                    <input class="form-group btn btn-default bttn" type="button" name="bttn8" value="8" onclick="calC(bttn8.value);">
                    <input class="form-group btn btn-default bttn" type="button" name="bttn9" value="9" onclick="calC(bttn9.value);">
                    <input class="form-group btn btn-danger bttn" type="button" name="bttnplus" value="+" onclick="calC(bttnplus.value);"><br/>
                    <input class="form-group btn btn-default bttn" type="button" name="bttn4" value="4" onclick="calC(bttn4.value);">
                    <input class="form-group btn btn-default bttn" type="button" name="bttn5" value="5" onclick="calC(bttn5.value);">
                    <input class="form-group btn btn-default bttn" type="button" name="bttn6" value="6" onclick="calC(bttn6.value);">
                    <input class="form-group btn btn-danger bttn" type="button" name="bttnminus" value="-" onclick="calC(bttnminus.value);"><br/>
                    <input class="form-group btn btn-default bttn" type="button" name="bttn1" value="1" onclick="calC(bttn1.value);">
                    <input class="form-group btn btn-default bttn" type="button" name="bttn2" value="2" onclick="calC(bttn2.value);">
                    <input class="form-group btn btn-default bttn" type="button" name="bttn3" value="3" onclick="calC(bttn3.value);">
                    <input class="form-group btn btn-danger bttn" type="button" name="bttnmulti" value="*" onclick="calC(bttnmulti.value);"><br/>
                    <input class="form-group btn btn-default bttn" type="button" name="bttndot" value="." onclick="calC(bttndot.value);">
                    <input class="form-group btn btn-default bttn" type="button" name="bttn0" value="0" onclick="calC(bttn0.value);">
                    <input class="form-group btn btn-danger bttn" type="button" name="bttnmod" value="%" onclick="calC(bttnmod.value);">
                    <input class="form-group btn btn-danger bttn" type="button" name="bttndiv" value="/" onclick="calC(bttndiv.value);"><br/>

                    <!-- calling new reset function -->
                    <input class="form-group btn btn-info bttn bttne" type="button" name="bttnclear" value="CE" onclick="CE();">
                    <input class="form-group btn btn-success bttn bttne" type="button" name="bttnEQL" value="=" onclick="panel.value=eval(panel.value);">

                </form>                    
            </div>
        </div>
    </div>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"></script>

    <!-- my own JS -->
    <script src="/assets/js/calculator.js"></script>
</body>

</html>