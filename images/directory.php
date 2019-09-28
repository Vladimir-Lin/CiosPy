<?php

$REALROLE = "tutors" ;

function RoleDIR($FILENAME)
{
  global $REALROLE                   ;
  return "/{$REALROLE}/" . $FILENAME ;
}

function sameDIR($FILENAME)
{
  return dirname(__FILE__) . "/" . $FILENAME ;
}

function phpDIR($FILENAME)
{
  return dirname(__FILE__) . "/../php/" . $FILENAME ;
}

?>
