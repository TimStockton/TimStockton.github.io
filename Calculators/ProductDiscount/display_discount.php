<?php
    // Get the data from the form in index.html.
    $product_description = $_POST['product_description'];
    $list_price = $_POST['list_price'];
    $discount_percent = $_POST['discount_percent'];

    
    // Calculate the discount.
    $discount = $list_price * $discount_percent * .01;
    $discounted_price = $list_price - $discount;

    // Apply currency formatting to the dollar and percent amounts.
    $list_price_formatted = "$".number_format($list_price, 2);
    $discount_percent_formatted = number_format($discount_percent, 1)."%";
    $discount_formatted = "$".number_format($discount, 2);
    $discount_price_formatted = "$".number_format($discounted_price, 2);
    $product_description_escaped = htmlspecialchars($product_description);
?>

<!DOCTYPE html>
<html>

<head>
    <title>TCSII | Product Discount </title>
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
        <nav>
            <a href="../index.html">Home</a>&nbsp;
            <a href="index.html">Back</a>
        </nav>
    </header>

    <main class="center" id="main">
        <h1>Product Discount Calculator</h1>
        <br>
        <label>Product Description: </label>
        <span><?php echo $product_description_escaped; ?></span><br>
        <br>
        <label>List Price: </label>
        <span><?php echo $list_price_formatted; ?></span><br>
        <br>
        <label>Standard Discount: </label>
        <span><?php echo $discount_percent_formatted; ?></span><br>
        <br>
        <label>Discount Amount: </label>
        <span><?php echo $discount_formatted; ?></span><br>
        <br>
        <label>Discounted Price: </label>
        <span><?php echo $discount_price_formatted; ?></span><br>
        <br>
    </main>

    <footer id="footer" class="center">
        <nav id="bottom-nav">
            <a href="../index.html">Home</a>&nbsp;
            <a href="index.html">Back</a>
        </nav>
        <p>Copyright &copy; 2020-2023 Timothy Stockton</p>
        <p>Contact Me: <a href="mailto:timstocktonii@gmail.com">here</a></p>
    </footer>

</body>
</html>