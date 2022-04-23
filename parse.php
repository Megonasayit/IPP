<?php
ini_set('display_errors','stderr');
$order = 0;
$header = false;

//help
if ($argc > 1){
    if($argv[1] == "--help"){
        echo("Help:\nparser.php <inputFile\n");
        exit(0);
    }
}
//regex for variable, label and symbol
define("VAR","/^(LF|GF|TF)@[a-zA-Z_\-#$&%*!?][a-zA-Z_\-#$&%*!?$0-9]*$/");
define("LABEL", "/^[a-zA-Z_\-#$&%*!?][a-zA-Z_\-#$&%*!?$0-9]+$/");
define("SYMB", "/(^int@[+-]?[0-9]+$)|(^bool@(true|false)$)|(^nil@nil$)|(^string@(((\\\\[0-9][0-9][0-9])+)|([^#\\\\\s])+)*$)|(^(LF|GF|TF)@[a-zA-Z_\-#$&%*!?][a-zA-Z_\-#$&%*!?$0-9]*$)/");

//while cycle that goes through whole code
while($line = fgets(STDIN)){
    //replacing multiple spaces with one
    $line = preg_replace('/[\t ]+/',' ', $line);
    //checking for comment in code and deleting it
    if(strpos($line, "#")){
        if(preg_match("/[\s+]#/", $line)){
            $line = substr($line, 0, strpos($line, "#")-1);
        }else{
            $line = substr($line, 0, strpos($line, "#"));
        }
    }
    //checking for empty lines
    if(preg_match("/^[\s+]$/", $line) || $line[0] == "#" || (strpos($line, "#") &&preg_match("/^\s$/", $line[0]))){
        continue;
    }
    
    //splitting line to split
    $split = explode(' ', trim($line, "\n"));

    //checking for header
    if($header == false){
        if(preg_match("/^([\t ]*).IPPCODE21([\t ]*)$/", trim(strtoupper($line), ' '))){
            echo("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n");
            echo("<program language=\"IPPcode21\">\n");
            $header = true;
        }else{
            exit(21);
        }
    }else{
        if(strtoupper($split[0]) == "READ"){
            if(count($split) == 3){
                $value[1] = $split[1];
                $value[2] = $split[2];
                $type[1] = "var";
                $type[2] = "type";
            }
        }else{
            for($i = 1; $i < count($split); $i++){
                $cnt = 0;
                $cnt = strpos($split[$i], "@");
                $type[$i] = substr($split[$i], 0, $cnt);
                if($cnt != 0){
                    $cnt++;
                }
                $value[$i] = substr($split[$i], $cnt, strlen($split[$i]));

                if($type[$i] == 'GF' || $type[$i] == 'LF' || $type[$i] == 'TF'){
                    $type[$i] = "var";
                    $value[$i] = $split[$i];
                }else if($type[$i] == ""){
                    $type[$i] = "label";
                }
            }
        }

        //commands switch
        switch(strtoupper($split[0])){
            case 'CREATEFRAME':
            case 'PUSHFRAME':
            case 'POPFRAME':
            case 'RETURN':
            case 'BREAK':
                if(count($split) == 1){
                    echo("\t<instruction order=\"$order\" opcode=\"".strtoupper($split[0])."\">")."\n";
                    echo("\t</instruction>\n");
                }else{
                    exit(23);
                }
                break;
            case 'DEFVAR':
            case 'POPS':
                if(count($split) == 2){
                    echo("\t<instruction order=\"$order\" opcode=\"".strtoupper($split[0])."\">")."\n";
                    if(preg_match(constant("VAR"), $split[1])){
                        $value[1] = htmlspecialchars($value[1], ENT_XML1, 'UTF-8');
                        echo("\t\t<arg1 type=\"".$type[1]."\">".$value[1]."</arg1>")."\n";
                    }else{
                        exit(23);
                    }
                    echo("\t</instruction>\n");
                }else{
                    exit(23);
                }
                break;
            case 'ADD':
            case 'SUB':
            case 'MUL':
            case 'IDIV':
            case 'LT':
            case 'GT':
            case 'EQ':
            case 'AND':
            case 'OR':
            case 'STRI2INT':
            case 'CONCAT':
            case 'GETCHAR':
            case 'SETCHAR':
                if(count($split) == 4){
                    echo("\t<instruction order=\"$order\" opcode=\"".strtoupper($split[0])."\">")."\n";
                    if(preg_match(constant("VAR"), $split[1])){
                        $value[1] = htmlspecialchars($value[1], ENT_XML1, 'UTF-8');
                        echo("\t\t<arg1 type=\"".$type[1]."\">".$value[1]."</arg1>")."\n";
                    }else{
                        exit(23);
                    }
                    if(preg_match(constant("SYMB"), $split[2])){
                        $value[2] = htmlspecialchars($value[2], ENT_XML1, 'UTF-8'); 
                        echo("\t\t<arg2 type=\"".$type[2]."\">".$value[2]."</arg2>")."\n";
                    }else{
                        exit(23);
                    }
                    if(preg_match(constant("SYMB"), $split[3])){
                        $value[3] = htmlspecialchars($value[3], ENT_XML1, 'UTF-8'); 
                        echo("\t\t<arg3 type=\"".$type[3]."\">".$value[3]."</arg3>")."\n";
                    }else{
                        exit(23);
                    }
                    echo("\t</instruction>\n");
                }else{
                    exit(23);
                }
                break;
            case 'INT2CHAR':
            case 'MOVE':
            case 'STRLEN':
            case 'NOT':
            case 'TYPE':
                if(count($split) == 3){
                    echo("\t<instruction order=\"$order\" opcode=\"".strtoupper($split[0])."\">")."\n";
                    if(preg_match(constant("VAR"), $split[1])){
                        $value[1] = htmlspecialchars($value[1], ENT_XML1, 'UTF-8');
                        echo("\t\t<arg1 type=\"".$type[1]."\">".$value[1]."</arg1>")."\n";
                    }else{
                        exit(23);
                    }
                    if(preg_match(constant("SYMB"), $split[2])){
                        $value[2] = htmlspecialchars($value[2], ENT_XML1, 'UTF-8'); 
                        echo("\t\t<arg2 type=\"".$type[2]."\">".$value[2]."</arg2>")."\n";
                    }else{
                        exit(23);
                    }
                    echo("\t</instruction>\n");
                }else{
                    exit(23);
                }
                break;
            case 'READ':
                if(count($split) == 3){
                    echo("\t<instruction order=\"$order\" opcode=\"".strtoupper($split[0])."\">")."\n";
                    if(preg_match(constant("VAR"), $split[1])){
                        $value[1] = htmlspecialchars($value[1], ENT_XML1, 'UTF-8');
                        echo("\t\t<arg1 type=\"".$type[1]."\">".$value[1]."</arg1>")."\n";  
                    }else{
                        exit(23);
                    }
                    if(preg_match("/^(int|bool|string)$/", $split[2])){
                        $value[2] = htmlspecialchars($value[2], ENT_XML1, 'UTF-8');
                        echo("\t\t<arg2 type=\"".$type[2]."\">".$value[2]."</arg2>")."\n";
                    }else{
                        exit(23);
                    }
                    echo("\t</instruction>\n");
                }else{
                    exit(23);
                }
                break;
            case 'LABEL':
            case 'JUMP':
            case 'CALL':
                if(count($split) == 2){
                    echo("\t<instruction order=\"$order\" opcode=\"".strtoupper($split[0])."\">")."\n";
                    if(preg_match(constant("LABEL"), $split[1])){
                        $value[1] = htmlspecialchars($value[1], ENT_XML1, 'UTF-8');
                        echo("\t\t<arg1 type=\"".$type[1]."\">".$value[1]."</arg1>")."\n";              
                    }else{
                        exit(23);
                    }
                    echo("\t</instruction>\n");
                }else{
                    exit(23);
                }
                break;
            case 'JUMPIFEQ':
            case 'JUMPIFNEQ':
                if(count($split) == 4){
                    echo("\t<instruction order=\"$order\" opcode=\"".strtoupper($split[0])."\">")."\n";
                    if(preg_match(constant("LABEL"), $split[1])){
                        $value[1] = htmlspecialchars($value[1], ENT_XML1, 'UTF-8');
                        echo("\t\t<arg1 type=\"".$type[1]."\">".$value[1]."</arg1>")."\n";
                    }else{
                        exit(23);
                    }
                    if(preg_match(constant("SYMB"), $split[2])){
                        $value[2] = htmlspecialchars($value[2], ENT_XML1, 'UTF-8'); 
                        echo("\t\t<arg2 type=\"".$type[2]."\">".$value[2]."</arg2>")."\n";
                    }else{
                        exit(23);
                    }
                    if(preg_match(constant("SYMB"), $split[3])){
                        $value[3] = htmlspecialchars($value[3], ENT_XML1, 'UTF-8'); 
                        echo("\t\t<arg3 type=\"".$type[3]."\">".$value[3]."</arg3>")."\n";
                    }else{
                        exit(23);
                    }
                    echo("\t</instruction>\n");
                }else{
                    exit(23);
                }
                break;
            case 'PUSHS':
            case 'WRITE':
            case 'EXIT':
            case 'DPRINT':
                if(count($split) == 2){
                    echo("\t<instruction order=\"$order\" opcode=\"".strtoupper($split[0])."\">")."\n";
                    if(preg_match(constant("SYMB"), $split[1])){
                        $value[1] = htmlspecialchars($value[1], ENT_XML1, 'UTF-8');             
                        echo("\t\t<arg1 type=\"".$type[1]."\">".$value[1]."</arg1>")."\n";    
                    }else{
                        exit(23);
                    }
                    echo("\t</instruction>\n");
                }else{
                    exit(23);
                }
                break;
            default:
                if(preg_match("/^#/", $split[0])){
                    $order--;
                }else{
                    exit(22);
                }
                break;
        }
    }
    $order++;
}
if($header == false){
    exit(21);
}
echo("</program>\n");

?>