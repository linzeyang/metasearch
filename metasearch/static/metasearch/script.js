function onReady() {
    $( "#input_query" ).focus( onFocusInputQuery );

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
            $( "#checkboxes input[type='checkbox']" ).first().focus();
            return false;
        }
        else if( numOfChecked === 1 )
        {
            if( $( "#select_aggr" ).val() === "true" )
            {
                alert('Select at least two search engines for aggregated results!');
                $( "#checkboxes input[type='checkbox']" ).first().focus();
                return false;
            }
            else
            {
                return true;
            }
        }
        else
        {
            return true;
        }
    }
};