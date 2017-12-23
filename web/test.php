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
<html>
<body>
    <form method="post">
    <p>
        <button name="button">On</button>
    </p>
    <p>
        <button name="btn">Off</button>
    </p>
    </form>
</body>
</html>

