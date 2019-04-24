
<html>

<body>

<?php

    /* Insira aqui a pasta que deseja salvar o arquivo. Ex: imagens */

    $uploaddir = '/home/00937325465/familiai/acompanhaig/arquivos/zip/';

    $files = glob($uploaddir.'*'); // get all file names
    foreach($files as $file){ // iterate files
      if(is_file($file))
        unlink($file); // delete file
    }

    $uploadfile1 = $uploaddir . "1.zip";

    if (move_uploaded_file($_FILES['arquivo1']['tmp_name'], $uploadfile1)){  
        echo "Arquivo 1 Enviado";
    }  
    else {
        echo "Houve um problema no upload do arquivo 1.";
    }
header('Location: http://10.32.64.91/acompanhaig/');
?>

</body>

</html>

