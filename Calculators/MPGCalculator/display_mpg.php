<?php
    // Get the data from the form in index.html.
    $miles = $_POST['miles'];
    $gallons = $_POST['gallons'];
    
    // Calculate the miles per gallon.
    $mpg = $miles / $gallons;
?>

<!DOCTYPE html>
<html lang="en">

<!-- Timothy C Stockton II -->

<head>
    <title>TCSII | MPG Calculator </title>
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
            <a href="index.html">Back</a>&nbsp;
        </nav>
    </header>

    <main class="center" id="main">
        <h1>MPG Calculator</h1>
        <br />
        <label>Miles Driven: </label>
        <span><?php echo $miles; ?></span><br>
        <br />
        <label>Gallons Used: </label>
        <span><?php echo $gallons; ?></span><br>
        <br />
        <label>Miles Per Gallon (MPG): </label>
        <span><?php echo $mpg; ?></span><br>
        <br />
    </main>

    <footer id="footer" class="center">
        <nav id="bottom-nav">
            <a href="../index.html">Home</a>&nbsp;
            <a href="index.html">Back</a>
        </nav>
        <p>Copyright &copy; 2020-2023 Timothy Stockton</p>
        <p>Contact Me: <a href="mailto:timstocktonii@gmail.com">here</a></p>
    </footer>

    <script>
    </script>

</body>

</html>