<!DOCTYPE html>
<html lang="en">

<!-- Timothy C Stockton II -->

<head>
    <title>TCSII | Future Value </title>
    <meta charset="utf-8">
    <link rel="stylesheet" href="CSS/layout.css">
    <link rel="stylesheet" href="CSS/style.css">
    <link rel="icon" href="Images/favicon.png" type="image/x-icon">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
    </style>
</head>

<body>

    <header id="header" class="center">
        <nav id="top-nav">
            <a href="../index.html">Home</a>&nbsp;
            <a href="../Login/index.html">Login</a>&nbsp;
            <a href="https://pandemica.online" target="blank">Pandemica Online</a>&nbsp;
            <a href="../JavaScriptCalculator/index.html">JavaScript Calculator</a>&nbsp;
            <a href="../TemperatureConverter/index.html">Temperature Converter</a>&nbsp;
            <a href="../ProductDiscount/index.html">Product Discount</a>&nbsp;
            <a href="index.php">Future Value</a>&nbsp;
            <a href="../MPGCalculator/index.html">MPG Calculator</a>&nbsp;
            <a href="../RandomQuoteMachine/index.html">Random Quote Machine</a>&nbsp;
            <a href="../DrumMachine/index.html">Drum Machine</a>&nbsp;
            <a href="../MarkdownPreviewer/index.html">Markdown Previewer</a>&nbsp;
            <a href="../SurveyForm/index.html">Survey</a>
        </nav>
    </header>

    <main class="center" id="main">
        <h1>Future Value Calculator</h1>
        <br>
        <?php if (!empty($error_message)) { ?>
            <p class="error"><?php echo $error_message; ?></p>
        <?php } ?>
        <form action="display_results.php" method="post">
            <div id="data">
                <label>Investment Amount:</label>
                <input type="text" name="investment" style="color:black;"/>
                <br>
                <br>
                <label>Yearly Interest Rate:</label>
                <input type="text" name="interest_rate" style="color:black;"/>
                <br>
                <br>
                <label>Number of Years:</label>
                <input type="text" name="years" style="color:black;"/>
                <br>
            </div>
            <br>
            <div id="buttons">
                <label>&nbsp;</label>
                <input type="submit" value="Calculate" style="color:black;"/>
                <br />
            </div>
        </form>
        <br>
    </main>

    <footer id="footer" class="center">
        <nav id="bottom-nav">
            <a href="../index.html">Home</a>&nbsp;
            <a href="../Login/index.html">Login</a>&nbsp;
            <a href="https://pandemica.online" target="blank">Pandemica Online</a>&nbsp;
            <a href="../JavaScriptCalculator/index.html">JavaScript Calculator</a>&nbsp;
            <a href="../TemperatureConverter/index.html">Temperature Converter</a>&nbsp;
            <a href="../ProductDiscount/index.html">Product Discount</a>&nbsp;
            <a href="index.php">Future Value</a>&nbsp;
            <a href="../MPGCalculator/index.html">MPG Calculator</a>&nbsp;
            <a href="../RandomQuoteMachine/index.html">Random Quote Machine</a>&nbsp;
            <a href="../DrumMachine/index.html">Drum Machine</a>&nbsp;
            <a href="../MarkdownPreviewer/index.html">Markdown Previewer</a>&nbsp;
            <a href="../SurveyForm/index.html">Survey</a>
        </nav>
        <p>Copyright &copy; 2020-2023 Timothy Stockton</p>
        <p>Contact Me: <a href="mailto:timstocktonii@gmail.com">here</a></p>
    </footer>

    <script>
    </script>


</body>

</html>