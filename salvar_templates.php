<?php

function salvarTemplate($nm_arquivo, $texto){
    $path = '/home/00937325465/familiai/acompanhaig/templates/';
    $myfile = fopen($path . $nm_arquivo, "w") or die("Unable to open file " . $nm_arquivo);
    fwrite($myfile, $texto);
}

$template1 = $_POST["template1"];
salvarTemplate("template_basico.html", $template1);

header('Location: http://10.32.64.91/acompanhaig/');

?>

