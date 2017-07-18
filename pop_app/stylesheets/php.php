<?php
$link_title = array("link 1", "link 2", "link 3", "link 4");
$link_page = array("page1.php", "page2.php", "page3.php", "page4.php");
$count=0;
?>
<ul class="tabs">


<?php
foreach($link_page as $link)
{
if(basename($_SERVER['SCRIPT_NAME']) == $link)
{
$active=' class="liSelected"';
}
else
{
$active='';
}
echo '<li '.$active.'><a href="'.$link.'">'.$link_title[$count].'</a></li>';
$count++;
}
?>
 </ul>