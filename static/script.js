function onReady() {
    $( "#input_query" ).focus( onFocusInputQuery );

    $( "#button_search" ).button();
    $( "#button_search" ).click( validate );
};

function onFocusInputQuery( event )
{
    $( "#input_query" ).val("");
};

function validate( event )
{
    var $inputQuery = $( "#input_query" );
    
    if( $inputQuery.val() === '' )
    {
        alert( "Query cannot be empty!" );
        $inputQuery.focus();
        return false;
    }
    else
    {
        var numOfChecked = $( "#checkboxes :checked" ).length;

        if( numOfChecked === 0 )
        {
            alert( "Select at least one search engine!" );
            $( "#box_bing" ).focus();
            return false;
        }
        else if( numOfChecked === 1 )
        {
            alert('Select at least two search engines for aggregated results!');
            $( "#select_aggr" ).focus();
            return false;
        }
        else
        {
            return true;
        }
    }
};