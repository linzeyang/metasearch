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
    var query = document.form1.query;
    var bing = document.form1.bing, blekko = document.form1.blekko, entweb = document.form1.entweb;
    var aggr = document.form1.aggr
    
    if(query.value == '')
    {
        alert("Query cannot be empty!");
        query.focus();
        return false;
    }
    else
    {
        if(!bing.checked && !blekko.checked && !entweb.checked)
        {
            alert("Select at least one search engine!");
            bing.focus();
            return false;
        }
        else if((aggr.value == 'true') && ((!bing.checked && !blekko.checked) || (!blekko.checked && !entweb.checked) || (!bing.checked && !entweb.checked)))
        {
            alert('Select at least two search engines for aggregated results!');
            aggr.focus();
            return false;
        }
        else
        {
            return true;
        }
    }
};