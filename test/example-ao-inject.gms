
**ao list asset
**ao param asset 'parameter.capacity.capacity'
**ao map asset 'type'

$ontext
The model can be temporally decomposed in a few ways.
block denotes a subset of time that should be solved together.  This allows a user to change from solving
    a 4 hour block of time to a month at a time.  The amount of time that can be solved together
    depends on the complexitity of the model.
ch(time) is used to denote the time that should be solved in the current 
$offtext

set 
    time                  "Time index of model. Currently assumed to be hourly.";

alias (time,t);     

set
*   Date time map
    datetime_comp         "Datetime components used to map a time index to a real datetime." 
                            /year,month,day,hour,minute,second/
    year                  "Years possible in the simulat" /y2018*y2028/
    month                 "Months of the year" /m1*m12/
    m2t(month,time)       "Map month to time"

*   Solve subset of time
    ch(time)              "These time elements are included in the current solve (includes look ahead)." 
    ch_store(time)        "These time elements are saved after the current solve (excludes look back/ahead)"
    ch_all(time)         "These time elements include both the look ahead and look back period"

*   Solve in larger window usings look ahead, look back
    ch_window(time,t)       "This set maps a single time element to include its lookahead window"
    ch_back_window(time,t)  "This set maps a single time element to include its lookback window"
    lookbacktime(time,t)    "Look back time exclusive of current time" 
    lookaheadtime(time,t)   "Look ahead time exclusive of current time" 

*   Solve many subsets in blocks
    block                           "A block represents a chunk of time to solve together"
    check_block(block)              "Blocks to solve in single gams run"
    block_time(block,time)          "Maps blocks to time elements"
    block_window(block,time)        "Map blocks to time with look ahead"
    block_back_window(block,time)    "Map blocks to time with look back"
    ch_all_time(time,t)             "All time elements to check in gams run"
    run_time(time)                  "Time (excluding lookback/ahead) included in all of run"
    run_time_window(time)           "Time (including lookahead) included in all of run"
    run_time_all(time)           "Time (including lookback/ahead) included in all of run"
    run_time_first(time)            "First time period of run"
    run_time_last(time)             "Last time period of run";
