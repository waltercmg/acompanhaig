<head>
    <meta charset="UTF-8">
</head>
<body>


<?php

function getConteudoTemplate($nm_template){
    $path = "/home/00937325465/familiai/acompanhaig/templates/".$nm_template;
    $arq = fopen($path, "r") or die("Não foi possivel abrir arquivo!");
    $conteudo = fread($arq,filesize($path));
    fclose($arq);
    return $conteudo;
}
?>
<form action="salvar_templates.php" method="POST">
        Template básico:<br> 
        <textarea rows=30 cols=80 name="template1"/><?=htmlspecialchars(getConteudoTemplate("template_basico.html"))?></textarea><br>
        <br>
        <input type="submit" value="Enviar"/> 
    </form>   
<br><br>
<a href="index.php">Menu</a>

</body>


