<?php
	// get the data from the form
	$investment = $_POST['investment'];
	$interest_rate = $_POST['interest_rate'];
	$years = $_POST['years'];

	// validate investment entry
	if ( empty($investment) ) {
		$error_message = 'Investment is a required field.';
	} else if ( !is_numeric($investment) ) {
		$error_message = 'Investment must be a valid number.';
	} else if ( $investment <= 0 ) {
		$error_message = 'Investment must be greater than zero.';
	// validate interest rate entry
	} else if ( empty($interest_rate) ) {
		$error_message = 'Interest rate is a required field.';
	} else if ( !is_numeric($interest_rate) ) {
		$error_message = 'Interest rate must be a valid number.';
	} else if ( $interest_rate <= 0 ) {
		$error_message = 'Interest rate must be greater than zero.';
	// set error message to empty string if no invalid entries
	} else {
		$error_message = '';
	}

	// if an error message exists, go to the index page
	if ($error_message != '') {
		include('index.php');
		exit(); }

	// calculate the future value
	$future_value = $investment;
	for ($i = 1; $i <= $years; $i++) {
		$future_value =	($future_value + ($future_value * $interest_rate * .01));
	}

	// apply currency and percent formatting
	$investment_f = '$'.number_format($investment, 2);
	$yearly_rate_f = $interest_rate.'%';
	$future_value_f = '$'.number_format($future_value, 2);
?>

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
        <label>Investment Amount:</label>
		<span><?php echo $investment_f; ?></span>
        <br>
        <br>
        <label>Yearly Interest Rate:</label>
		<span><?php echo $yearly_rate_f ; ?></span>
        <br>
        <br>
        <label>Number of Years:</label>
		<span><?php echo $years; ?></span>
        <br>
        <br>
        <label>Future Value:</label>
		<span><?php echo $future_value_f ; ?></span>
        <br>
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