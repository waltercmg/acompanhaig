<?php
setlocale(LC_CTYPE, "en_US.UTF-8");
$command = escapeshellcmd('/usr/bin/python2.7 /home/00937325465/familiai/acompanhaig/Principal.py');
$output = shell_exec($command);
header('Location: http://10.32.64.91/acompanhaig/html/');
?>
