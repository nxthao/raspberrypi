<?php
    if (isset($_POST['button']))
    {
        system("gpio mode 7 out");
        system("gpio write 7 1");
    }
    else if (isset($_POST['btn']))
    {
        system("gpio write 7 0");
    }
?>

<?php
    if (isset($_POST['button2']))
    {
        system("gpio mode 0 out");
        system("gpio write 0 1");
    }
    else if (isset($_POST['btn2']))
    {
        system("gpio write 0 0");
    }
?>
<html>
<body>
<header>
<h1 
class="Title"> 
dieu khien led
</h1>
<h1 
 class="Title"> 
</h1>
<h1 
 class="Title"> Thảo
</h1>
<h1 
 class="Title"> Điều khiển thiết bị đơn giản
</h1>
</header>
    <form method="post">
    <p>
        <button name="button">Bật Đèn Trạm 1</button> <button name="btn">Tắt Đèn Trạm 1</button>
    </p>
    <p>
        <button name="button2">Bật Đèn Trạm 2</button> <button name="btn2">Tắt Đèn Trạm 2</button>
    </p>
    </form>
</body>
</html>

<html>
<head>
<style>
body {
background-color: #b6ff00;
font-family: 'Times New Roman';
text-align: center;
}
div {
font-family:'Times New Roman';
text-align: center;
}
#h1 { font-size: x-large;
#background-color: #0ff;
#color: #0026ff;
#}
h2 { font-size: larger;
background-color: #b6ff00;
color: #f00;
}
</style>
<meta charset="utf-8" />
<title> 
dieu khien led
</title>
</body>
</html>
