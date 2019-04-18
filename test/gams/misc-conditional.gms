
$if set forward_run $include %gamsfolder%em_init_forward.inc

$if set load_scale p_set_t(time,load)=%load_scale%*p_set_t(time,load);

$if %modeltype% == 'ce' $include %gamsfolder%ce_init.inc
